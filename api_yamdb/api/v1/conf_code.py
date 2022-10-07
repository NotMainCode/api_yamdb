"""Generation, verification, saving confirmation code and sending to mail."""

from secrets import token_hex

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail

from api_yamdb.settings import LEN_COMFIRM_CODE
from users.models import User


def make_conf_code(email):
    user = User.objects.get(email=email)
    conf_code = token_hex(LEN_COMFIRM_CODE)
    conf_code = "12345678123456781234567812345678"
    user.confirmation_code = make_password(conf_code)
    user.password = user.confirmation_code
    user.save()
    send_mail(
        "Confirmation code",
        f"Use this code to get an access token: {conf_code}",
        "api_yamdb",
        (email,),
        fail_silently=False,
    )


def check_conf_code(user, conf_code):
    expected_conf_code = user.confirmation_code
    return check_password(conf_code, expected_conf_code)
