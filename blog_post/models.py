from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="static/category_icons", blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=350, default="Will shown at home screen.")
    estimated_reading_time = models.IntegerField(default=0)
    cover = models.ImageField(upload_to="static/covers", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})

    def get_api_like_url(self):
        return reverse("like_api_post", kwargs={"pk":self.pk})

    def get_like_url(self):
        return reverse("like_post", kwargs={"pk":self.pk})

    class Meta:
        verbose_name = 'Gönderi'
        verbose_name_plural = 'Gönderiler'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.post.title} | {self.content}"

    class Meta:
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'