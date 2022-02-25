from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .sitemaps import PostSitemap, StaticSitemap, CategorySitemap
from django.contrib.sitemaps.views import sitemap
from blog_post.views import robotsView

sitemaps = {
    'static': StaticSitemap,
    'post': PostSitemap,
    'category': CategorySitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_post.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('user/', include('users.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", robotsView),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
