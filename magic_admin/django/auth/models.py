from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MagicUserMixin(models.Model):

    public_address = models.CharField(
        _('public address'),
        max_length=128,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        default=None,
    )

    class Meta:
        abstract = True

    @classmethod
    def get_by_public_address(cls, public_address):
        return cls.objects.get(public_address=public_address)

    def update_user_with_public_address(
        self,
        user_id,
        public_address,
        user_obj=None,
    ):
        if user_obj is None:
            user_obj = self.objects.get(pk=user_id)

        if user_obj.public_address == public_address:
            return user_obj

        user_obj.public_address = public_address
        user_obj.save(update_fields=['public_address'])

        return user_obj


class MagicAnonymousUser(AnonymousUser):
    pass
