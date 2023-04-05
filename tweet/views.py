from django.shortcuts import render,redirect
from .models import TweetModel
from .models import TweetComment
# TweetModel 가져오기
from django.contrib.auth.decorators import login_required
#어떤 함수가 동작할때 로그인 되어 있어야만 동작할 수 있는 데코레이터 import
from django.views.generic import ListView, TemplateView

def home(request):
    user = request.user.is_authenticated
    #사용자가 로그인 했는지 검사해주는, 내장 기능

    if user:
        #사용자가 있다면
        return redirect('/tweet')

    else:
        #사용자가 없다면 로그인 화면으로 이동
        return redirect('/sign-in')

@login_required
def tweet(request):
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        all_tweet = TweetModel.objects.all().order_by('-created_at')
        return render(request, 'tweet/home.html', {'tweet': all_tweet})
    elif request.method == 'POST':  # 요청 방식이 POST 일때
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')
@login_required()
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def detail_tweet(request, id):
    #댓글 불러오기 함수
    my_tweet = TweetModel.objects.get(id=id)
    # TweetModel 클래스의 id값에 해당하는 데이터 필드의 정보를 변수에 저장
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    # TweetComment 클래스에 해당하는 id값만을 뽑아오는데, 이때 최신순으로 정렬한다.
    return render(request,'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})


@login_required
def write_comment(request, id):
    # 댓글 작성 함수, 데코레이터로 로그인한 사용자만 인증받아 작성할 수 있는 내장 기능이 첨가되어 있다.
    if request.method == 'POST':
        #POST방식일때 동작
        comment = request.POST.get("comment","")
        # 전달받은 데이터를 comment 변수에 저장
        current_tweet = TweetModel.objects.get(id=id)
        # TweetModel의 데이터베이스 필드중 id값과 일치하는 모든 데이터를 변수에 저장한다.

        TC = TweetComment()
        #TweetComment클래스의 객채 생성
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        # POST방식으로 전달된 데이터를 객체에 저장하고

        TC.save()
        #데이터를 저장한다.

        return redirect('/tweet/'+str(id))
        # id순서에 맞는 페이지를 반환한다.


@login_required
def delete_comment(request, id):
    #댓글 삭제기능, 데코레이터로 로그인한 사용자만 접근할 수 있다.
    comment = TweetComment.objects.get(id=id)
    #TweetComment클래스의 id필드에, 매개변수 id에 해당하는 댓글 데이터를 불러온다.
    current_tweet = comment.tweet.id
    #tweet id, 현재 게시글의 위치값을 반환한다.
    comment.delete()
    # 해당하는 댓글 데이터 삭제
    return redirect('/tweet/'+str(current_tweet))
    #게시글에 해당하는 페이지를 반환한다.

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
