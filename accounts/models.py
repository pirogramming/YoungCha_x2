from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.db import models


class UserManager(AuthUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    score = models.CharField(default='10000000', max_length=30)
    wallet = models.IntegerField(default=10000000)


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=30, default='0')
    rate_of_return = models.CharField(max_length=10, default='0')
    total_assets = models.CharField(max_length=100,  default='0')
    amount_of_asset_change = models.CharField(max_length=100,  default='0')
    trade_numbers = models.CharField(max_length=100,  default='0')
    john_bur_term = models.CharField(max_length=10, default='0')
    game_date = models.DateTimeField(auto_now_add=True)


# def on_post_save_for_user(sender, **kwargs):
#     if kwargs['created']:
#         # 가입시기
#         user = kwargs['instance']
#
#         # 환영 이메일 보내기
#         send_mail(
#             '환영합니다.',
#             'Here is the message.',
#             'me@askcompany.kr',
#             [user.email],
#             fail_silently=False,
#         )
# post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    session_key = models.CharField(max_length=40, editable=False)
    # created_at = models.DateTimeField(auto_now_add=True)


def on_user_logged_in(sender, request, user, **kwargs):
    user.is_user_logged_in = True


user_logged_in.connect(on_user_logged_in)

