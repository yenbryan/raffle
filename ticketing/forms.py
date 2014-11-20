from django import forms
from ticketing.models import Product
import datetime


class CreateRaffleForm(forms.Form):
    name = forms.CharField(max_length=125,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'description'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'description'}))
    total_number_of_tickets = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    start_time = forms.DateTimeField(initial=datetime.date.today,
                                 # input_formats=['%Y-%m-%d %H:%M:%S'],
                                 widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    end_time = forms.DateTimeField(initial=datetime.date.today,
                               # input_formats=['%Y-%m-%d %H:%M:%S'],
                               widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    pricing_per_ticket = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self, user):
        product = Product.objects.create(name=self.cleaned_data['name'],
                                          description=self.cleaned_data['description'],
                                          total_number_of_tickets=self.cleaned_data['total_number_of_tickets'],
                                          start_time=self.cleaned_data['start_time'],
                                          end_time=self.cleaned_data['end_time'],
                                          pricing_per_ticket=self.cleaned_data['pricing_per_ticket'],
                                          user=user)
        return product