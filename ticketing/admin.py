from django.contrib import admin
from ticketing.models import Picture, Ticket, Product


admin.site.register(Product)
admin.site.register(Ticket)
admin.site.register(Picture)
