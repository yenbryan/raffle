import braintree
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from ticketing.forms import CreateRaffleForm, TicketPurchaseForm
from ticketing.models import Product, Ticket, Picture
import datetime
import pytz

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id='cyttpz8353vkpbrd',
    public_key='nrn2r5tngvrn5f2v',
    private_key='0f09fcb2f66e479b3473297b35d85d35'
)


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
    product = get_object_or_404(Product, pk=product_id)
    purchase_form = TicketPurchaseForm()

    if request.method == "POST":
        purchase_form = TicketPurchaseForm(request.POST)

        if purchase_form.is_valid():
            result = purchase_form.purchase(request.user, product_id)
            return render(request,'ticketing/view_product.html', {
                'product': product,
                'purchase_form': purchase_form,
                'result': result
            })
    raffle_ended = False
    if product.end_time < pytz.utc.localize(datetime.datetime.now()):
        raffle_ended = True

    return render(request,'ticketing/view_product.html', {
        'product': product,
        'purchase_form': purchase_form,
        'raffle_ended': raffle_ended
        # 'today': datetime.datetime.now()
    })


def my_products(request):
    products = Product.objects\
        .filter(user=request.user)\
        .filter(end_time__gte=datetime.datetime.now())\
        .annotate(ticket_count=Count('tickets'))
    past_products = Product.objects\
        .filter(user=request.user)\
        .filter(end_time__lte=datetime.datetime.now())\
        .annotate(ticket_count=Count('tickets'))

    return render(request, 'ticketing/my_products.html', {
        'products': products,
        'past_products': past_products,
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
            'tickets': unexpired_tickets
        })
    for ticket in expired_tickets:
        ticket_count = Ticket.objects.filter(product=ticket.product, user=request.user).count()
        product = ticket.product
        past_ticket_list.append({
            'product': product,
            'count': ticket_count,
            'tickets': expired_tickets
        })
    return render(request, 'ticketing/my_tickets.html', {
        'tickets': current_ticket_list,
        'past_tickets': past_ticket_list,
    })


def splash_index(request):
    products = Product.objects\
                   .filter(end_time__gte=datetime.datetime.now())\
                   .order_by('?')[:9]
    return render(request, 'splash_index.html', {'products': products})


def create_raffle(request):
    create_raffle_form = CreateRaffleForm()

    if request.method == "POST":
        raffle_form = CreateRaffleForm(request.POST, request.FILES)

        if raffle_form.is_valid():
            raffle = raffle_form.save(request.user)
            if raffle:
                return redirect('view_product', raffle.id)
    return render(request, 'create_raffle.html', {'form': create_raffle_form})