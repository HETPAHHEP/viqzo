from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from core.enums import Limits
from links.models import UserGroup


def check_user_groups_amount(user):
    if (
        UserGroup.objects.filter(owner_id=user).count()
        >= Limits.MAX_GROUPS_AMOUNT
    ):
        raise ValidationError(
            {
                "group_error": _(
                    f"Превышено максимальное количества групп: "
                    f"{Limits.MAX_GROUPS_AMOUNT}"
                )
            }
        )


def check_request_fields(data):
    if not data.get("group_name", None) and not data.get("group_id", None):
        raise ValidationError(
            {
                "field_error": _(
                    "Необходимо одно из полей group_name "
                    "или group_id для работы!"
                )
            }
        )
