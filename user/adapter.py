from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username
from allauth.utils import valid_email_or_none
from allauth.account.adapter import get_adapter as get_account_adapter
import string, random


class CustomSocialAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        uu = string.ascii_letters + string.digits
        ss = ""
        for i in range(6):
            ss += random.choice(uu)
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)
        u.nickname = "소셜" + ss
        sociallogin.save(request)
        return u

    def populate_user(self, request, sociallogin, data):
        uu = string.ascii_letters + string.digits
        uname = ""
        for i in range(20):
            uname += random.choice(uu)
        username = uname
        email = data.get("email")
        user = sociallogin.user
        user_username(user, username or "")
        user_email(user, valid_email_or_none(email) or "")
        return user
