from django.urls import path
from .views import homeView, ArticleDetailView, PostLikeView, categoryView, authorView, PostLikeApiView
urlpatterns = [
    path('', homeView, name='blog_home' ),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('like/<int:pk>', PostLikeView.as_view(), name='like_post'),
    path('like/<int:pk>/api', PostLikeApiView.as_view(), name='like_api_post'),
    path('category/<int:id>', categoryView, name='category'),
    path('author/<int:id>', authorView, name='author'),
    path('tag/<slug:tag_slug>/', homeView, name='post_tag'),
]
