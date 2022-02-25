from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import FormView
from .models import Post, Category, Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CommentForm
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib import messages

def robotsView(request):
    text = """
User-Agent: *

Disallow: /api/

Sitemap: https://pencereblog.pythonanywhere.com/sitemap.xml
    """
    return HttpResponse(text, content_type="text/plain")


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


class homeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date_created']

class articleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(post = self.get_object()).order_by('-created_at')
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),created_by=self.request.user,post=self.get_object())
        new_comment.save()
        messages.success(request, "Yorum başarılı bir şekilde yapıldı.")
        return self.get(self, request, *args, **kwargs)

def categoryView(request, id):
    posts = Post.objects.all().filter(category=id).order_by("-date_created")
    category = Post.objects.filter(category=id).first()
    context = {'posts': posts, 'category':category}
    return render(request, 'category.html', context)

def authorView(request, id):
    posts = Post.objects.all().filter(author=id).order_by("-date_created")
    author = User.objects.filter(id=id).first()
    context = {'posts': posts, 'author': author}
    return render(request, 'author.html', context)
