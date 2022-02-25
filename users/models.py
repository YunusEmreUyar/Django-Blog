from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="static/profile_pics", blank=True, null=True)
    instagram_url = models.CharField(null=True, blank=True, max_length=300)
    medium_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            img = Image.open(self.profile_pic.path)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size, Image.ANTIALIAS)
                img.save(self.profile_pic.path)

     class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiller'
