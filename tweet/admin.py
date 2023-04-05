from django.contrib import admin
from .models import TweetModel
# 생성한 TweetModel을 admin에 등록

# Register your models here.
admin.site.register(TweetModel)