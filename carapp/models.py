from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from decimal import Decimal
from django.urls import reverse

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12, unique=True, validators=[MinLengthValidator(10)])
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subcategory_name


class Car(models.Model):
    name = models.CharField(max_length=100)  # Car name or model
    brand = models.CharField(max_length=100)  # Brand of the car
    year = models.IntegerField()  # Manufacturing year
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)  # Rental price per day
    seating_capacity = models.IntegerField()  # Number of seats
    fuel_type = models.CharField(max_length=50, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])  # Fuel type
    description = models.TextField(blank=True, null=True)  # Optional description of the car
    image1 = models.ImageField(upload_to='car_images/', blank=True, null=True)  # Image of the car (Main)
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)  # Additional image of the car
    availability = models.BooleanField(default=True)  # Availability status
    ac = models.BooleanField(default=False)  # Air conditioning (yes or no)
    sunroof = models.BooleanField(default=False)  # Sunroof (yes or no)
    air_bags = models.BooleanField(default=False)  # Air bags (yes or no)
    central_lock = models.BooleanField(default=False)  # Central locking (yes or no)
    # Featured cars field, this will be True for featured cars
    is_featured = models.BooleanField(default=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    document_proof = models.FileField(upload_to='car_documents/', blank=True, null=True)  # Ownership proof
    insurance_copy = models.FileField(upload_to='car_documents/', blank=True, null=True)  # Insurance document
    registration_certificate = models.FileField(upload_to='car_documents/', blank=True, null=True)  # Registration certificate
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year}) - {self.status} "

    # def __str__(self):
    #     return f"{self.brand} {self.name} ({self.year})"

class Address(models.Model):
    recepient_name = models.CharField(max_length=100, null=True)
    recepient_contact = models.CharField(max_length=20, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} - {self.postal_code}"    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='customer')

    def __str__(self):
        return self.customer_name

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who booked the car
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Car being booked
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)  # Address for booking
    start_date = models.DateField()  # Arrival date (Booking start date)
    return_date = models.DateField()  # Return date (Booking end date)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for the booking
    contact_number = models.CharField(max_length=20)  # Landline/Mobile number
    local_contact_name = models.CharField(max_length=100)  # Name of local contact person
    local_contact_number = models.CharField(max_length=20)  # Local contact number

    aadhaar_number = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{12}$', 'Aadhaar number must be exactly 12 digits.')],
        help_text="Enter 12-digit Aadhaar number"
    )  # Aadhaar Number for verification

    driving_license_number = models.CharField(
        max_length=17,
        validators=[RegexValidator(r'^[A-Z]{2}\d{2} ?\d{4} ?\d{7}$', 
            'Driving License must be in format: XX00 0000 0000000')],
        help_text="Format: XX00 0000 0000000"
    )  # Driving License Number

    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )  # Booking status

    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')],
        default='Pending'
    )  # Payment status

    car_returned = models.BooleanField(default=False)  # To track if the car is returned
    actual_return_date = models.DateTimeField(null=True, blank=True)  # To record the actual return date

    def __str__(self):
        return f"Booking: {self.car.name} by {self.user.username} - {self.status} ({self.payment_status})"

    def clean(self):
        if self.start_date > self.return_date:
            raise ValidationError("Start date cannot be after the return date.")

from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, default='Admin')
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.id})

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reviewer
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='reviews')  # Car being reviewed
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)  # Optional rating
    review_text = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.rating or 'No Rating'} stars)"
