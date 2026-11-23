from datetime import date
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'guest_name',
            'guest_email',
            'guest_phone',
            'check_in',
            'check_out',
            'guests',
            'special_requests',
        ]
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rami Mansour'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+963 9XX XXX XXX'}),
            'check_in': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Sea-view balcony, late check-in...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        guests = cleaned_data.get('guests')

        if check_in and check_in < date.today():
            raise forms.ValidationError("Check-in date cannot be in the past.")

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out date must be at least one day after check-in.")

        if guests is not None and guests < 1:
            raise forms.ValidationError("At least 1 guest is required.")

        return cleaned_data