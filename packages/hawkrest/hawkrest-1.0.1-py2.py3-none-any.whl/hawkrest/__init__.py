import logging
import sys
import traceback

from django.conf import settings
from django.core.cache import cache

try:
    from django.utils.module_loading import import_string
except ImportError:
    # compatibility with django < 1.7
    from django.utils.module_loading import import_by_path
    import_string = import_by_path

from mohawk import Receiver
from mohawk.exc import BadHeaderValue, HawkFail, TokenExpired
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from hawkrest.util import get_auth_header, is_hawk_request


log = logging.getLogger(__name__)
# Number of seconds until a Hawk message expires.
default_message_expiration = 60


def default_credentials_lookup(cr_id):
    if cr_id not in settings.HAWK_CREDENTIALS:
        raise LookupError('No Hawk ID of {id}'.format(id=cr_id))
    return settings.HAWK_CREDENTIALS[cr_id]


def default_user_lookup(request, credentials):
    return HawkAuthenticatedUser(), None


class HawkAuthentication(BaseAuthentication):

    def hawk_credentials_lookup(self, cr_id):
        lookup = default_credentials_lookup
        lookup_name = getattr(
            settings,
            'HAWK_CREDENTIALS_LOOKUP',
            None)
        if lookup_name:
            log.debug('Using custom credentials lookup from: {}'
                .format(lookup_name))
            lookup = import_string(lookup_name)
        return lookup(cr_id)

    def hawk_user_lookup(self, request, credentials):
        lookup = default_user_lookup
        lookup_name = getattr(
            settings,
            'HAWK_USER_LOOKUP',
            None)
        if lookup_name:
            log.debug('Using custom user lookup from: {}'
                .format(lookup_name))
            lookup = import_string(lookup_name)
        return lookup(request, credentials)

    def authenticate(self, request):
        # In case there is an exception, tell others that the view passed
        # through Hawk authorization. The META dict is used because
        # middleware may not get an identical request object.
        # A dot-separated key is to work around potential environ var
        # pollution of META.
        request.META['hawk.receiver'] = None

        http_authorization = get_auth_header(request)
        if not http_authorization:
            log.debug('no authorization header in request')
            return None
        elif not is_hawk_request(request):
            log.debug('ignoring non-Hawk authorization header: {} '
                      .format(http_authorization))
            return None

        try:
            receiver = Receiver(
                lambda cr_id: self.hawk_credentials_lookup(cr_id),
                http_authorization,
                request.build_absolute_uri(),
                request.method,
                content=request.body,
                seen_nonce=(seen_nonce
                            if getattr(settings, 'USE_CACHE_FOR_HAWK_NONCE',
                                       True)
                            else None),
                content_type=request.META.get('CONTENT_TYPE', ''),
                timestamp_skew_in_seconds=getattr(settings,
                                                  'HAWK_MESSAGE_EXPIRATION',
                                                  default_message_expiration))
        except HawkFail as e:
            etype, val, tb = sys.exc_info()
            log.debug(traceback.format_exc())
            log.warning('access denied: {etype.__name__}: {val}'
                        .format(etype=etype, val=val))
            # The exception message is sent to the client as part of the
            # 401 response, so we're intentionally vague about the original
            # exception type/value, to avoid assisting attackers.
            msg = 'Hawk authentication failed'
            if isinstance(e, BadHeaderValue):
                msg += ': The request header was malformed'
            elif isinstance(e, TokenExpired):
                msg += ': The token has expired. Is your system clock correct?'
            raise AuthenticationFailed(msg)

        # Pass our receiver object to the middleware so the request header
        # doesn't need to be parsed again.
        request.META['hawk.receiver'] = receiver
        return self.hawk_user_lookup(request, receiver.resource.credentials)

    def authenticate_header(self, request):
        return 'Hawk'

    # Added for Django compatibility, allowing use of this class as a
    # normal Django authentication backend as well (for views outside
    # Django Rest Framework)
    def get_user(self, user_id):
        return HawkAuthenticatedUser()


class HawkAuthenticatedUser(object):
    """
    A real-ish user like AbstractBaseUser but not a real Django model.

    This passes the DRF is_authenticated permission check but it may cause
    other problems. If you need to work with a real Django model user
    you might need to subclass HawkAuthentication.
    """
    is_active = True

    def get_full_name(self):
        return str(self.__class__.__name__)

    def get_short_name(self):
        return str(self.__class__.__name__)

    def get_username(self):
        return str(self.__class__.__name__)

    def clean(self):
        # There's nothing to clean, since the name is `self.__class__.__name__`.
        pass

    def save(self, *args, **kwargs):
        raise NotImplementedError()

    def natural_key(self):
        return str(self.__class__.__name__)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, password):
        raise NotImplementedError()

    def check_password(self, password):
        raise NotImplementedError()

    def set_unusable_password(self):
        pass

    def has_usable_password(self):
        return False

    def get_session_auth_hash(self):
        raise NotImplementedError()

    # -----------------------------------------------
    # These methods are in older Django versions only:
    # -----------------------------------------------

    def get_previous_by_last_login(self, *args, **kw):
        raise NotImplementedError()

    def get_next_by_last_login(self, *args, **kw):
        raise NotImplementedError()


def seen_nonce(id, nonce, timestamp):
    """
    Returns True if the Hawk nonce has been seen already.
    """
    key = '{id}:{n}:{ts}'.format(id=id, n=nonce, ts=timestamp)
    if cache.get(key):
        log.warning('replay attack? already processed nonce {k}'
                    .format(k=key))
        return True
    else:
        log.debug('caching nonce {k}'.format(k=key))
        cache.set(key, True,
                  # We only need the nonce until the message itself expires.
                  # This also adds a little bit of padding.
                  timeout=getattr(settings, 'HAWK_MESSAGE_EXPIRATION',
                                  default_message_expiration) + 5)
        return False
