"""Custom validators."""

from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_year(value):
    if value > now().year:
        raise ValidationError(
            "Release year can't exceed the current date",
            params={'value': value},
        )
