from django.contrib import admin
# django에서 admin툴을 사용하겠다는 의미
from .models import UserModel
# 우리가 생성한 모델을 가져오는 것

# Register your models here.
admin.site.register(UserModel)
# 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다
# 관리자 페이지에 입력한다.