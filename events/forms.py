from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    price_details = forms.CharField(
        required=False,
        label='Price note',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. two tusker or one of them',
        })
    )

    payment_method = forms.ChoiceField(
        required=False,
        choices=Event.PAYMENT_METHOD_CHOICES,
        label='Payment method',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    payment_details = forms.CharField(
        required=False,
        label='Payment details',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter till number or phone number',
        })
    )

    total_tickets = forms.CharField(
        required=False,
        label='Capacity',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    price = forms.DecimalField(
        min_value=0,
        max_digits=8,
        decimal_places=2,
        label='Ticket Price (Ksh)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        exclude = ['organizer', 'is_approved']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }