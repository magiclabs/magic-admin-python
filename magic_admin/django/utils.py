from django.contrib.auth import logout as django_logout

from magic_admin.magic import Magic
from magic_admin.utils.logging import log_debug


def logout(request):
    user = request.user

    if not user.is_anonymous and user.public_address:
        Magic().User.logout_by_public_address(user.public_address)
        log_debug('Log out user from Magic')

    django_logout(request)
