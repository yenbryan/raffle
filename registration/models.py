from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
import local_settings


class Profile(AbstractUser):

    def __unicode__(self):
        return self.username

    def send_email(self, subject, message):
        self.email_user('{}'.format(subject), '{}'.format(message))
        text_content = '{}'.format(message)
        html_content = '{}'.format(message)
        msg = EmailMultiAlternatives('{}'.format(subject) , text_content, local_settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
