import random
from django.db import models
from django.db.models import Count
from registration.models import Profile
import datetime

# class Category(models.Model):
#     pass


class Product(models.Model):
    name = models.CharField(max_length=140, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    total_number_of_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()
    pricing_per_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    winning_ticket_number = models.IntegerField(blank=True)
    user = models.ForeignKey(Profile, related_name='products')
    default_picture = models.ForeignKey("Picture", related_name="products", blank=True, null=True)

    def get_ticket_price(self):
        return '${}'.format(self.pricing_per_ticket)

    def get_winning_probability(self, ticket_count):
        return (float(ticket_count)*100)/float(self.total_number_of_tickets)

    def save(self, *args, **kwargs):
        #  Create winning raffle ticket number
        if self.winning_ticket_number is None:
            self.winning_ticket_number = random.randint(1, self.total_number_of_tickets)
        super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    ticket_number = models.IntegerField(blank=True)
    user = models.ForeignKey(Profile, related_name='tickets')
    product = models.ForeignKey(Product, related_name='tickets')

    def save(self, *args, **kwargs):
        #  Create winning raffle ticket number
        self.product.tickets_sold = int(self.product.tickets_sold) + 1
        self.product.save()
        self.ticket_number = self.product.tickets_sold
        super(Ticket, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'product{}- ticket number{} {}'.format(self.product.id, self.ticket_number, self.user.username)


class Picture(models.Model):
    image = models.ImageField(upload_to='media/product_pictures',
                              blank=True,
                              null=True)
    description = models.CharField(max_length=140, blank=True, null=True)
    # default_picture = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name='pictures')

    def __unicode__(self):
        return 'img{}-{}'.format(self.id, self.product.name)