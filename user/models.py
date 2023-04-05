#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# AbstractUser Django가 제공하는 기본적인 auth_user테이블과 연동
from django.conf import settings



class UserModel(AbstractUser):
    #장고의 기본 모델을 상속받는다.
    class Meta:
        db_table = "my_user"
    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')


