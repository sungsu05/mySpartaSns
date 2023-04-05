from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    #  sign-up 에 접속하면, views파일의 sign_up_view실행
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/',views.logout,name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>/', views.user_follow, name='user-follow')
]