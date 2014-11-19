from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render
from ticketing.forms import CreateRaffleForm
from ticketing.models import Product, Ticket, Picture
import datetime


def products(request):
    all_products = Product.objects.filter(end_time__gte=datetime.datetime.now())
    paginator = Paginator(all_products, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, "ticketing/products.html", {
        'products': products,
    })


def view_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request,'ticketing/view_product.html', {
        'product': product,
    })


def my_products(request):
    products = Product.objects\
        .filter(user=request.user)\
        .filter(end_time__gte=datetime.datetime.now())
    tickets = Ticket.objects.filter(product__in=products)\
        .values('product')\
        .annotate(number_of_tickets_sold=Count('product'))
    past_products = Product.objects\
        .filter(user=request.user)\
        .filter(end_time__lte=datetime.datetime.now())
    past_tickets = Ticket.objects.filter(product__in=past_products)\
        .values('product')\
        .annotate(number_of_tickets_sold=Count('product'))
    return render(request, 'ticketing/my_products.html', {
        'products': products,
        'tickets':tickets,
        'past_products': past_products,
        'past_tickets': past_tickets
    })


def my_tickets(request):
    unexpired_tickets = Ticket.objects\
        .filter(product__end_time__gte=datetime.datetime.now())\
        .filter(user=request.user).distinct('product')
    expired_tickets = Ticket.objects\
        .filter(product__end_time__lte=datetime.datetime.now())\
        .filter(user=request.user).distinct('product')

    current_ticket_list = []
    past_ticket_list = []

    for ticket in unexpired_tickets:
        ticket_count = Ticket.objects.filter(product=ticket.product, user=request.user).count()
        product = ticket.product
        current_ticket_list.append({
            'product': product,
            'count': ticket_count,
            'total_tickets': product.total_number_of_tickets,
            'winning_probability': product.get_winning_probability(ticket_count),
        })
    for ticket in expired_tickets:
        ticket_count = Ticket.objects.filter(product=ticket.product, user=request.user).count()
        product = ticket.product
        past_ticket_list.append({
            'product': product,
            'count': ticket_count,
        })
    return render(request, 'ticketing/my_tickets.html', {
        'tickets': current_ticket_list,
        'past_tickets': past_ticket_list,
    })


def splash_index(request):
    return render(request, 'body_template.html')


def create_raffle(request):
    create_raffle_form = CreateRaffleForm()
    return render(request, 'create_raffle.html', {'form': create_raffle_form})


def purchase(request, product_id):
    pass