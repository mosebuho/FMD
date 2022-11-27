from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username
from allauth.utils import valid_email_or_none
from allauth.account.adapter import get_adapter as get_account_adapter
import string, random


class CustomSocialAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        item = string.ascii_letters + string.digits
        pick = ""
        for i in range(8):
            pick += random.choice(item)
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)
        u.nickname = "소셜" + pick
        u.social = True
        sociallogin.save(request)
        return u

    def populate_user(self, request, sociallogin, data):
        item = string.ascii_letters + string.digits
        pick = ""
        for i in range(20):
            pick += random.choice(item)
        username = pick
        email = data.get("email")
        user = sociallogin.user
        user_username(user, username or "")
        user_email(user, valid_email_or_none(email) or "")
        return user
