import braintree
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, redirect
from ticketing.forms import CreateRaffleForm
from ticketing.models import Product, Ticket, Picture
import datetime

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
    product = Product.objects.get(pk=product_id)
    return render(request,'ticketing/view_product.html', {
        'product': product,
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

    if request.method == "POST":
        raffle_form = CreateRaffleForm(request.POST)

        if raffle_form.is_valid():
            raffle = raffle_form.save(request.user)
            if raffle:
                return redirect('my_products')
    #
    #         if message:
    #             for recipient in send_form.cleaned_data['recipient']:
    #                 receiver = Receiver.objects.create(message=message,
    #                                                    recipient=Profile.objects.get(id=recipient))
    #             return redirect('dashboard')
    # data = {'messageactive': 'active',
    #         'profile': profile_picture,
    #         'send_form': send_form}

    return render(request, 'create_raffle.html', {'form': create_raffle_form})

    # send_form = SendMessageForm()
    # profile = Profile.objects.get(id=request.user.id)
    # try:
    #     profile_picture = ProfilePicture.objects.get(profile=profile, default_picture=True)
    # except:
    #     profile_picture = None
    #
    #
    # return render(request, 'message/send_message.html', data)

def purchase(request, product_id):
    pass