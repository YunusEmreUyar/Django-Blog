from django.contrib.sitemaps import Sitemap
from blog_post.models import Post, Category
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return ['blog_home']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
	change_freq = "weekly"
	priority = 0.8
	protocol = 'https'

	def items(self):
		return Post.objects.all()

	def lastmod(self, obj):
		return obj.date_created

	def location(self, obj):
		return f"/article/{obj.id}"


class CategorySitemap(Sitemap):
	change_freq = "weekly"
	priority = 0.7
	protocol = "https"

	def items(self):
		return Category.objects.all()

	def location(self, obj):
		return f"/category/{obj.id}"
