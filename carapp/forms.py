# forms.py
from django import forms
from .models import Address,Booking,Car

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['recepient_name', 'recepient_contact', 'address_line1', 'address_line2', 'city', 'state', 'postal_code']
        widgets = {
            'recepient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recepient_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from datetime import date
import re
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'start_date', 'return_date', 'contact_number',
            'local_contact_name', 'local_contact_number',
            'aadhaar_number', 'driving_license_number'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date', 'min': date.today().isoformat()
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date', 'min': date.today().isoformat()
            }),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'local_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'local_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'driving_license_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)  # Get car instance if provided
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        return_date = cleaned_data.get('return_date')
        aadhaar_number = cleaned_data.get('aadhaar_number')

        # Validate dates
        if start_date and return_date:
            if start_date >= return_date:
                raise forms.ValidationError("Return date must be after the start date.")

            if start_date < date.today():
                raise forms.ValidationError("Start date cannot be in the past.")

            if not self.car:
                raise forms.ValidationError("Car information is missing.")

            # Calculate total price
            days = (return_date - start_date).days
            cleaned_data['total_price'] = days * self.car.price_per_day

        # Validate Aadhaar number (should be 12 digits)
        if aadhaar_number:
            if not aadhaar_number.isdigit():
                raise forms.ValidationError("Aadhaar number must contain only digits.")

            if len(aadhaar_number) != 12:
                raise forms.ValidationError("Aadhaar number must be exactly 12 digits.")

        return cleaned_data

    def clean_driving_license_number(self):
        dl_number = self.cleaned_data.get('driving_license_number')

        if not dl_number:
            raise forms.ValidationError("Driving License number is required.")

        # Remove extra spaces to standardize input
        dl_number = re.sub(r'\s+', '', dl_number)  # Remove spaces

        # Check if the structure is correct (no spaces yet)
        if not re.match(r'^[A-Z]{2}\d{2}\d{4}\d{7}$', dl_number):
            raise forms.ValidationError("Invalid format. Expected: XX00 0000 0000000")

        # Automatically format with spaces
        formatted_dl_number = f"{dl_number[:4]} {dl_number[4:8]} {dl_number[8:]}"
        
        return formatted_dl_number


class CarSubmissionForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'name', 'brand', 'year', 'price_per_day', 'seating_capacity', 'fuel_type',
            'description', 'image1', 'image2', 'ac', 'sunroof', 'air_bags', 'central_lock',
            'subcategory', 'document_proof', 'insurance_copy', 'registration_certificate'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].empty_label = "Select Subcategory"


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ⭐") for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review (optional)...'})
        }

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        review_text = cleaned_data.get('review_text')

        # Allow skipping both fields
        if not rating and not review_text:
            return {}  # Return empty data if skipped

        return cleaned_data
