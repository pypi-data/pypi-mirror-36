import collections
import functools
import logging
from datetime import datetime

from requests_oauthlib import OAuth2Session
import django.contrib.auth
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import utc

from .models import OAuthToken
from . import signals

log = logging.getLogger(__name__)

ClientSettings = collections.namedtuple(
    'ClientSettings',
    'client secret url_base url_authorize url_token url_userinfo url_logout')


@functools.lru_cache(maxsize=1)
def blender_id_oauth_settings() -> ClientSettings:
    """Container for Blender ID OAuth Client settings."""
    from urllib.parse import urljoin

    url_base = settings.BLENDER_ID['BASE_URL']
    return ClientSettings(
        client=settings.BLENDER_ID['OAUTH_CLIENT'],
        secret=settings.BLENDER_ID['OAUTH_SECRET'],
        url_base=url_base,
        url_authorize=urljoin(url_base, 'oauth/authorize'),
        url_token=urljoin(url_base, 'oauth/token'),
        url_userinfo=urljoin(url_base, 'api/me'),
        url_logout=urljoin(url_base, 'logout'),
    )


def login_view(request):
    """Login the user by redirecting to Blender ID.

    If the user was visting a page that required login, its url will be saved in
    the session and made available after login through a redirect.
    """
    blender_id_oauth = blender_id_oauth_settings()
    redirect_uri = request.build_absolute_uri(reverse('oauth:callback'))
    bid = OAuth2Session(blender_id_oauth.client, redirect_uri=redirect_uri)
    authorization_url, state = bid.authorization_url(blender_id_oauth.url_authorize)

    # State is used to prevent CSRF.
    request.session['oauth_state'] = state
    request.session['next_after_login'] = (request.GET.get('next') or
                                           request.META.get('HTTP_REFERER'))
    return redirect(authorization_url)


@transaction.atomic()
def callback_view(request):
    blender_id_oauth = blender_id_oauth_settings()
    redirect_uri = request.build_absolute_uri(reverse('oauth:callback'))
    bid = OAuth2Session(blender_id_oauth.client,
                        state=request.session['oauth_state'],
                        redirect_uri=redirect_uri)
    token = bid.fetch_token(blender_id_oauth.url_token, client_secret=blender_id_oauth.secret,
                            authorization_response=request.build_absolute_uri())

    bid = OAuth2Session(blender_id_oauth.client, token=token)
    user_oauth = bid.get(blender_id_oauth.url_userinfo).json()

    # Look for oauth_id
    oauth_id = user_oauth['id']

    try:
        user = User.objects.get(oauth_tokens__oauth_user_id=oauth_id)
    except ObjectDoesNotExist:
        # Create a new user for the given oauth_user_id
        # TODO handle nickname or email conflict
        user = User.objects.create_user(user_oauth['nickname'], user_oauth['email'],
                                        User.objects.make_random_password())
        user.save()
        signals.user_created.send(sender=user, instance=user, oauth_info=user_oauth)

        # Convert access_token expiry time into datetime.
        # FIXME: big fat assumption this is a UTC timestamp, look it up in the standard.
        expires_at = datetime.fromtimestamp(token['expires_at'], tz=utc)

        # Store the OAuth token, associated with the newly created User
        OAuthToken.objects.create(
            user=user,
            provider='blender-id',
            oauth_user_id=oauth_id,
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            expires_at=expires_at)

    django.contrib.auth.login(request, user)

    next_after_login = request.session.pop('next_after_login', None)
    if next_after_login:
        log.debug('Redirecting user to %s', next_after_login)
        return redirect(next_after_login)

    return redirect(settings.LOGIN_REDIRECT_URL)


def logout_view(request):
    """Logout from My Data, and then from Blender ID.

    This helps perceiving My Data as part of Blender ID.
    """
    blender_id_oauth = blender_id_oauth_settings()
    django.contrib.auth.logout(request)
    return redirect(blender_id_oauth.url_logout)
