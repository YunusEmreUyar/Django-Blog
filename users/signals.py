from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.dispatch import receiver
from .models import Profile
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        model_dict = model_to_dict(instance)
        current_site = "https://pencereblog.pythonanywhere.com"
        mail_subject = 'Hesabınızı aktif ediniz.'
        message = render_to_string('acc_active_email.html', {
            'user': instance,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(instance.id)),
            'token':account_activation_token.make_token(instance),
        })
        to_email = model_dict["email"]
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
