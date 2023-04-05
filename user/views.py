from django.shortcuts import render,redirect
# html파일을 화면에 보여주는 헤더파일
from .models import UserModel
# 내가 가지고 있는앱 models의 UserModel을 가져오겠다.
from django.http import HttpResponse
# 화면에 글자를 띄울때 사용하는 헤더파일
from django.contrib.auth import get_user_model
#사용자가 데이터 베이스 안에 있는지 검사하는 함수
from django.contrib import auth
#Django의 인증 기능을 제공하는 헤더파일
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else :
            return render(request,'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        bio = request.POST.get('bio','')

        if password != password2:
            #패스워드가 같지 않을경우

            return render(request,'user/signup.html',{'error':'비밀번호를 확인 해 주세요'})
        #올바르다면, 데이터 저장
        else:
            if username == '' or password == '':
                #아이디, 비밀번호를 입력하지 않고 로그인 시도할 경우
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수입니다.'})

            exist_user = get_user_model().objects.filter(username=username)
            #filter를 통해, 똑같은 이름을 검색해서, 있다면 변수에 담는다.
            if exist_user :
                #빈 문자열을 거짓을 반환하기에 조건문으로 사용 할 수 있다.
                return render(request,'user/signup.html',{'error':'동일한 사용자가 존재합니다.'})
            else:
                UserModel.objects.create_user(
                    username=username,password=password,bio=bio
                )
                #로그인 페이지로 이동
                return redirect('sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        #POST방식으로 받은 데이터를 변수에 저장, 디폴트 값은 ''
        #'username','password'는 html태그와 동일하게 작성해야 한다.
        password = request.POST.get('password','')

        me = auth.authenticate(request,username = username,password=password)
        # UserModel 클래스의 필드 username에, POST방식으로 저장한 username의 값이 있는지 확인한다.

        if me is not None:
            auth.login(request,me)
            return redirect('/')
        else:# 로그인에 실패할 경우 (비밀번호가 틀리거나 등등)
            return render(request,'user/signin.html',{'error':'아이디와 비밀번호를 확인 해 주세요.'})

        #로그인 성공 출력
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else :
            return render(request, 'user/signin.html')
        #GET이라면 화면에 HTML 출력


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        # exclude : 해당하는 데이터에서 특정한 데이터를 빼오겠다. > user.username 검색
        # 나를 제외한 사용자 리스트를 갖고 오겠다.
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    # me : 로그인한 사용자
    click_user = UserModel.objects.get(id=id)
    #click_user : 로그인한 사용자가 팔로우하거나 팔로우 취소할 사용자
    # 해당 사용자의 id의 모델을 가져온다.


    if me in click_user.followee.all():
        #click_user가 팔로우하는 모든 데이터를 가져온다.
        #그 데이터속에 me가 포함되어 있지 않다면 me는 상대방을 팔로우 하고 있지 않는다.
        # 동작 : 팔로우 중이면 팔로우
        # 동작 : 팔로우 중이 아니라면, 팔로우
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')