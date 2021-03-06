from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Article, Page, Comment


# Create your views here.
# 메인화면
class NewsFeedView(TemplateView):
    template_name = 'newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedView, self).get_context_data(**kwargs)

        context['feeds'] = Article.objects.all()

        return context


# 상세화면
class NewsFeedDetailView(DetailView):
    model = Article
    template_name = 'feed_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedDetailView, self).get_context_data(**kwargs)

        user = self.request.user

        context['feed'] = Article.objects.select_related('user').filter(author=user)

        context['comments'] = Comment.objects.filter(
            article_id=self.kwargs['pk']
        )

        return context


# 뉴스피드 생성화면
@method_decorator(login_required, name='dispatch')
class FeedCreate(TemplateView):
    template_name = 'feed_create.html'


# 뉴스피드 수정 화면
@method_decorator(login_required, name='dispatch')
class FeedUpdate(UpdateView):
    model = Article
    fields = [
        'title', 'text'
    ]
    template_name = 'feed_update.html'

    def get_context_data(self, **kwargs):
        context = super(FeedUpdate, self).get_context_data(**kwargs)

        return context


# 페이지 목록 화면
class PageView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        user = self.request.user

        context['pages'] = Page.objects.all()

        return context


# 페이지 상세화면
class PageDetailView(DetailView):
    template_name = 'page_detail.html'
    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)

        return context


# 페이지 생성화면
class PageCreate(TemplateView):
    template_name = 'page_create.html'


# 페이지 수정화면
@method_decorator(login_required, name='dispatch')
class PageUpdate(UpdateView):
    template_name = 'page_update.html'
    model = Page
    fields = [
        'master',
        'name',
        'text'
    ]

    def get_context_data(self, **kwargs):
        context = super(PageUpdate, self).get_context_data(**kwargs)
        # self.kwargs['pk']를 통해서 url에서 pk값을 받을 수 있습니다.
        # url은 `path('<pk>/', PhotoView.as_view())으로 구현되어있어서 해당 pk 부분을 받아옵니다.`
        # context['page_id'] = Page.objects.filter(page_id=self.kwargs['pk'])
        return context


# 팔로우 화면
class RelationView(TemplateView):
    pass
