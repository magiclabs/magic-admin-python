from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from magic_admin.django.config import MagicAuthBackendMode
from magic_admin.django.exceptions import (
    MissingAuthorizationHeader,
    MissingUserEmailInput,
    PublicAddressDoesNotExist,
    UnsupportedAuthMode,
    UserEmailMissmatch,
)
from magic_admin.error import (
    DIDTokenError,
    APIConnectionError,
    RateLimitingError,
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    APIError,
)

from magic_admin.utils.http import get_identity_token_from_header
from magic_admin.magic import Magic
from magic_admin.utils.logging import (
    log_debug,
    log_info,
)


user_model = get_user_model()


class MagicAuthBackend(ModelBackend):

    @staticmethod
    def _load_user_from_email(email):
        log_debug('Loading user by email.', email=email)
        try:
            return user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None

    @staticmethod
    def _validate_identity_token_and_load_user(
        identity_token,
        email,
        public_address,
    ):
        try:
            Magic().Token.validate(identity_token)
        except (
                DIDTokenError,
                APIConnectionError,
                RateLimitingError,
                BadRequestError,
                AuthenticationError,
                ForbiddenError,
                APIError,
        ) as e:
            log_debug(
                'DID Token failed validation. No user is to be retrieved.',
                error_class=e.__class__.__name__,
            )
            raise e
            return None

        try:
            user = user_model.get_by_public_address(public_address)
        except user_model.DoesNotExist:
            raise PublicAddressDoesNotExist()

        if user.email != email:
            raise UserEmailMissmatch()

        return user

    def user_can_authenticate(self, user):
        if user is None:
            return False

        return super().user_can_authenticate(user)

    def _update_user_with_public_address(self, user, public_address):
        if self.user_can_authenticate(user):
            user.update_user_with_public_address(
                user_id=None,
                public_address=public_address,
                user_obj=user,
            )

    def _handle_phantom_auth(self, request, email):
        identity_token = get_identity_token_from_header(request)
        if identity_token is None:
            raise MissingAuthorizationHeader()

        public_address = Magic().Token.get_public_address(identity_token)

        try:
            user = self._validate_identity_token_and_load_user(
                identity_token,
                email,
                public_address,
            )
        except PublicAddressDoesNotExist:
            user = self._load_user_from_email(email)
            if user is None:
                log_debug(
                    'User is not authenticated. No user found with the given email.',
                    email=email,
                )
                Magic().User.logout_by_public_address(public_address)
                return

            self._update_user_with_public_address(user, public_address)
        except UserEmailMissmatch as e:
            log_debug(
                'User is not authenticated. User email does not match for the '
                'public address.',
                email=email,
                public_address=public_address,
                error_class=e.__class__.__name__,
            )
            Magic().User.logout_by_public_address(public_address)
            return

        if self.user_can_authenticate(user):
            log_info('User authenticated with DID Token.')
            return user

    def authenticate(
        self,
        request,
        user_email=None,
        mode=MagicAuthBackendMode.MAGIC,
    ):
        if not user_email:
            raise MissingUserEmailInput()

        user_email = user_model.objects.normalize_email(user_email)

        if mode == MagicAuthBackendMode.MAGIC:
            return self._handle_phantom_auth(request, user_email)
        else:
            raise UnsupportedAuthMode()
