# tweet/models.py
from django.db import models
from user.models import UserModel
# 유저앱에 있는 모델을 가져와서 사용할건데, 그중 이름이 UserModel을 갖고온다.
from taggit.managers import TaggableManager
# 게시글에 태그를 추가할 수 있게 만들어주는 매니저 헤더파일
# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    #ForeingKey  : 다른 데이터 베이스에서 내용을 가져온다.
    content = models.CharField(max_length=256)

    tags = TaggableManager(blank=True)
    #blank=True : 값이 비어 있어도 실행하겠다 알림

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)