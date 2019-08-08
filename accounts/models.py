import re

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
from django.urls import reverse


def phone_validator(value):
    if not re.match(r'^(?\d{3}-\d{3,4}-\d{4}$', value):
        raise ValidationError('000-000-0000꼴로 입력해주세요!')






class User(models.Model):
    user_id = models.CharField(
        verbose_name='ID',
        help_text='ID를 입력해주세요!',
        unique=True, blank=True, null=True, max_length=20),

    user_pw = models.CharField(
        verbose_name='PASSWORD',
        help_text='비밀번호를 입력해주세요!',
        max_length=20, null=True, blank=True, ),
    user_name = models.CharField(
        verbose_name='본인이름',
        help_text='성함을 입력해주세요!',
        max_length=100, null=True, blank=True,
    ),
    user_email = models.CharField(
        verbose_name='email',
        help_text='이메일을 입력해주세요!',
        max_length=100, null=True, blank=True,
    ),
    user_phone = models.CharField(
        validators=[phone_validator],
        verbose_name='phone',
        help_text='핸드폰번호를 입력해주세요!',
        max_length=20, null=True, blank=True,

    ),

    def get_absolute_url(self):
        # 강추 기능 별 50개
        return reverse('haru:first' )

