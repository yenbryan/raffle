from random import randint
import datetime
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Count
import local_settings


class Profile(AbstractUser):

    def __unicode__(self):
        return self.username

    def send_email(self, subject, message):
        # Why use these formats instead of just the variable?
        self.email_user('{}'.format(subject), '{}'.format(message))
        text_content = '{}'.format(message)
        html_content = '{}'.format(message)
        msg = EmailMultiAlternatives('{}'.format(subject) , text_content, local_settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# Lots of rules around ecommerce, you're not allowed to store credit card numbers
class CreditCard(models.Model):
    card_number = models.CharField(max_length=16)
    exp_date = models.CharField(max_length=7)
    user = models.ForeignKey(Profile, related_name="credit_cards")
