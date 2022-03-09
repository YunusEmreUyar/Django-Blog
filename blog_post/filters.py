import django_filters
from .models import Post, Category


class PostFilter(django_filters.FilterSet):
	title = django_filters.CharFilter(lookup_expr="icontains")

	class Meta:
		model = Post
		fields = ['category', 'author', 'series']