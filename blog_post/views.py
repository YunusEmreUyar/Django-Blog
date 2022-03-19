from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import FormView
from django.db.models import Count
from .models import Post, Category, Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CommentForm
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib import messages
from taggit.models import Tag
from .filters import PostFilter

def robotsView(request):
    text = """
User-Agent: *

Disallow: /api/

Sitemap: https://pencereblog.pythonanywhere.com/sitemap.xml
    """
    return HttpResponse(text, content_type="text/plain")


def homeView(request, tag_slug=None):
    posts = Post.objects.filter(is_draft=False)
    tag = None
    post_filter = PostFilter(request.GET, queryset=Post.objects.filter(is_draft=False))

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    return render(request, "home.html", {"posts": posts, "tag":tag, "filter": post_filter})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(post = self.get_object()).order_by('-created_at')
        data['comments'] = comments

        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=self.object.id)
        data["similar_posts"] = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags")[:6]

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),created_by=self.request.user,post=self.get_object())
        new_comment.save()
        messages.success(request, "Yorum başarılı bir şekilde yapıldı.")
        return self.get(self, request, *args, **kwargs)

def categoryView(request, id):
    posts = Post.objects.all().filter(category=id, is_draft=False).order_by("-date_created")
    category = Post.objects.filter(category=id).first()
    context = {'posts': posts, 'category':category}
    return render(request, 'category.html', context)


class PostLikeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if not user in obj.likes.all():
                obj.likes.add(user)
        return url_


class PostLikeApiView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if not user in obj.likes.all():
                liked = True
                obj.likes.add(user)
            updated = True
        data = {"updated": updated, "liked": liked}
        messages.success(request, "Beğenme işlemi başarıyla sonuçlandı.")
        return Response(data)


def authorView(request, id):
    posts = Post.objects.all().filter(author=id, is_draft=False).order_by("-date_created")
    author = User.objects.filter(id=id).first()
    context = {'posts': posts, 'author': author}
    return render(request, 'author.html', context)
