from django import forms
import datetime


class CreateRaffleForm(forms.Form):
    name = forms.CharField(max_length=125,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'description'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'description'}))
    total_number_of_tickets = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    start_time = forms.DateField(initial=datetime.date.today, widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    end_time = forms.DateField(initial=datetime.date.today, widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    pricing_per_ticket = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))