from django.shortcuts import get_object_or_404, render,redirect
from .models import Car
from .models import Blog
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from .models import Customer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import AddressForm
from django.views import View

def home(request):
    # Fetch all cars or just the featured ones
    cars = Car.objects.filter(availability=True)  # Only available cars
    categories = Category.objects.prefetch_related('subcategory_set').all()
    total_cars = Car.objects.count()
    blogs = Blog.objects.all().order_by('-created_at')[:3]
    featured_cars = Car.objects.filter(is_featured=True) # Only featured cars
    
    return render(request, 'home.html', {'cars': cars , 'total_cars': total_cars,'categories': categories,  'blogs': blogs, 'featured_cars': featured_cars})

def about(request):
    return render(request,"about.html")

def services(request):
    return render(request,"services.html")

def pricing(request):
    return render(request,"pricing.html")

def cars(request):
    cars = Car.objects.filter(status='Approved')  # Only fetch approved cars  # Assuming you have a Car model
    return render(request, 'cars.html', {'cars': cars})

# def blog(request):
#     return render(request,"blog.html")

def terms(request):
    return render(request,"terms.html")

# views.py
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                f'Contact Us Form: {subject}',  # Email subject
                f'Message from {name} ({email}):\n\n{message}',  # Email body
                settings.DEFAULT_FROM_EMAIL,  # From email (configured in settings.py)
                ['harshavtomy@gmail.com'],  # Recipient email
                fail_silently=False,
            )

            # Show success message
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'contact.html', {'form': form})
        else:
            # Show error message
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def car_detail(request, id):
    # Fetch the car using the ID
    car = get_object_or_404(Car, id=id)
    reviews = car.reviews.all()  # Fetching reviews

    context = {
        'car': car,
        'reviews': reviews  # Make sure reviews are passed only once
    }
    return render(request, 'car_detail.html', context)


from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Car, Booking

from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime

def search_cars(request):
    if request.method == 'POST':
        pickup_date = request.POST.get('pickup_date')
        dropoff_date = request.POST.get('dropoff_date')
        car_query = request.POST.get('search_query', '').strip()  # Get input and remove spaces

        # Remove any punctuation from car_query (e.g., "Brezza." → "Brezza")
        import re
        car_query = re.sub(r'[^\w\s]', '', car_query)  # Keep only words & spaces

        # Filter available cars
        cars = Car.objects.filter(availability=True)

        # Apply name or brand filter if provided
        if car_query:
            cars = cars.filter(Q(name__icontains=car_query) | Q(brand__icontains=car_query))

        return render(request, 'search_results.html', {'cars': cars})

    return render(request, 'car_search_form.html')




def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')



def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('your-email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        phone_number = request.POST.get('phone-number')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords Do Not Match!')
            return render(request, 'register.html')

        # Check password strength using Django's built-in validators
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return render(request, 'register.html')

        # Create user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except:
            messages.error(request, 'Email already exists!')
            return render(request, 'register.html')

        # Create customer
        customer = Customer.objects.create(user=user, customer_name=full_name, email=email, contact_number=phone_number)
        
        # Authenticate and login user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Your Account Has Been Registered Successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Failed to login user.')
            return render(request, 'register.html')

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  # Change 'home' to your desired redirect URL after login
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'login.html')  # Change 'customer/login.html' to your login template path
    return render(request, 'login.html')  # Change 'login.html' to your login template path

def user_logout(request):
    logout(request)
    return redirect('home') 



def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user  # Assuming the user is already logged in

        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('login')
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Old password is incorrect.")

    return render(request, 'change_password.html')

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.password + str(timestamp)
        )



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = CustomTokenGenerator().make_token(user)
            reset_password_url = request.build_absolute_uri('/reset_password/{}/{}/'.format(uid, token))
            email_subject = 'Reset Your Password'

            # Render both HTML and plain text versions of the email
            email_body_html = render_to_string('reset_password_email.html', {
                'reset_password_url': reset_password_url,
                'user': user,
            })
            email_body_text = "Click the following link to reset your password: {}".format(reset_password_url)

            # Create an EmailMultiAlternatives object to send both HTML and plain text versions
            email = EmailMultiAlternatives(
                email_subject,
                email_body_text,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.attach_alternative(email_body_html, 'text/html')  # Attach HTML version
            email.send(fail_silently=False)

            messages.success(request, 'An email has been sent to your email address with instructions on how to reset your password.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and CustomTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully. You can now login with your new password.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'reset_password.html')
    else:
        messages.error(request, "Invalid reset link. Please try again or request a new reset link.")
        return redirect('login')


@login_required
def edit_customer(request):
    # Retrieve the current logged-in user
    current_user = request.user
    # Check if the current user has a corresponding Customer instance
    try:
        customer = Customer.objects.get(user=current_user)
    except Customer.DoesNotExist:
        # Handle the case where the logged-in user does not have a corresponding Customer instance
        return HttpResponse("You are not associated with any customer profile.")

    if request.method == 'POST':
        # Update customer details with the data from the form
        customer.customer_name = request.POST['full-name']
        customer.email = request.POST['your-email']
        customer.contact_number = request.POST['phone-number']
        customer.save()

        # Update associated user's email
        current_user.email = request.POST['your-email']
        current_user.username = request.POST['your-email']
        current_user.save()

        # Redirect to the customer detail page after editing
        return redirect('home')

    # If it's a GET request, display the edit form with existing customer details
    return render(request, 'edit_customer.html', {'customer': customer})

@login_required
def address_list(request):
    addresses = Address.objects.filter(customer=request.user.customer)
    return render(request, 'address_list.html', {'addresses': addresses})

@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user.customer
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})

@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, customer=request.user.customer)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'address_form.html', {'form': form})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, customer=request.user.customer)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'address_confirm_delete.html', {'address': address})

from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Car, Booking
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, AddressForm

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
import stripe
from decimal import Decimal

# Set Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def book_now(request, car_id):
    """
    Handles booking a car and redirecting to payment flow.
    """
    car = get_object_or_404(Car, id=car_id)
    if not car.availability:
        messages.error(request, "Sorry, this car is currently unavailable.")
        return redirect('car_detail', id=car.id)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, request.FILES, car=car)
        address_form = AddressForm(request.POST)

        if booking_form.is_valid() and address_form.is_valid():
            # Save booking details
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.total_price = Decimal(booking_form.cleaned_data['total_price'])
            booking.save()

            # Save address details
            address = address_form.save(commit=False)
            address.customer = request.user.customer
            address.save()

            # Mark the car as unavailable
            car.availability = False
            car.save()

            messages.success(request, "Your booking has been successfully placed! Proceed to payment.")

            # Redirect to the payment page
            return redirect('checkout', booking_id=booking.id)

    else:
        booking_form = BookingForm(car=car)
        address_form = AddressForm()

    return render(request, 'book_now.html', {
        'car': car,
        'booking_form': booking_form,
        'address_form': address_form,
    })


@login_required
def checkout(request, booking_id):
    """
    Checkout page for processing payment for a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Restrict access if the booking is not confirmed
    if booking.status != 'Confirmed':
        messages.error(request, "You cannot proceed to payment until the booking is confirmed by the admin.")
        return redirect('my_bookings')  # Redirect to the user's bookings page

    if booking.payment_status == 'Paid':
        messages.warning(request, "This booking has already been paid.")
        return redirect('booking_success', booking_id=booking.id)

    context = {
        "booking": booking,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    }

    return render(request, "checkout.html", context)



@csrf_exempt
@login_required
def create_checkout_session(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)

        # Construct success and cancel URLs correctly
        success_url = request.build_absolute_uri(reverse('payment_success', kwargs={'booking_id': booking_id}))
        cancel_url = request.build_absolute_uri(reverse('payment_failed'))

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': booking.car.name,
                    },
                    'unit_amount': int(booking.total_price * 100),  # Stripe expects amounts in paise
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        # Respond with session ID for Stripe
        return JsonResponse({'id': session.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def payment_success(request, booking_id):
    """
    Handles successful payment for a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.payment_status == "Pending":
        booking.payment_status = "Paid"
        booking.save()

        # Define the pickup location
        pickup_location = "Office Location: XYZ Street, City, Office Hours: 9 AM to 6 PM"

        # Read the terms and conditions from the terms.html file
        terms_html = render_to_string('terms.html')  # Assuming the terms.html is in the templates folder

        # Send confirmation email
        subject = "Booking Confirmed: Payment Successful"
        context = {
            'user': booking.user,
            'car': booking.car,
            'total_price': booking.total_price,
            'booking_id': booking.id,
            'terms_html': terms_html,
            'pickup_location': pickup_location,
        }
        html_message = render_to_string('booking_confirmation_email.html', context)
        send_mail(
            subject,
            'Your booking is confirmed. Thank you for your payment!',
            'harshavtomy@gmail.com',  # Replace with your email
            [booking.user.email],
            fail_silently=False,
            html_message=html_message,
        )

        messages.success(request, "Payment successful! Your booking is confirmed.")
    else:
        messages.info(request, "Payment has already been processed for this booking.")

    return render(request, "payment_success.html", {"booking": booking})


def payment_failed(request, booking_id):
    """
    Handles failed payment.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    messages.error(request, "Payment failed or was canceled. Please try again.")
    return render(request, "payment_failed.html", {"booking": booking})


    
def booking_success(request):
    return render(request, 'booking_success.html')

def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    cars = Car.objects.filter(subcategory__parent_category=category)
    return render(request, 'category_products.html', {'category': category, 'cars': cars})

def subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    cars = Car.objects.filter(subcategory=subcategory)
    return render(request, 'subcategory_products.html', {'subcategory': subcategory, 'cars': cars})
    
class SellerLoginView(View):
    def get(self, request):
        return render(request, 'seller_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        seller = authenticate(request, username=username, password=password)

        if seller is not None:
            login(request, seller)
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'seller_login.html')


from django.core.paginator import Paginator
from django.utils.text import Truncator

def blog_view(request):
    blogs_list = Blog.objects.all().order_by('-created_at')  # Order by created_at
    paginator = Paginator(blogs_list, 5)  # Show 5 blogs per page

    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    # Truncate content for each blog
    for blog in blogs:
        blog.excerpt = Truncator(blog.content).chars(150)  # Show first 150 characters

    return render(request, 'blogs.html', {'blogs': blogs})

def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)  # Fetch the blog by primary key (id)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def booking_details(request, booking_id):
    # Fetch the booking and ensure the user is authorized to view it
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    return render(request, 'booking_details.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def download_invoice(request, booking_id):
    """
    Generate and download the invoice PDF.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Prepare data for the invoice template
    context = {
        'booking': booking,
        'user': request.user,
        'pickup_location': booking.address,
    }

    # Load the template
    template = get_template('invoice_template.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{booking_id}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('An error occurred while generating the PDF', status=500)
    return response

from django.utils import timezone


@login_required
def return_car(request, booking_id):
    """
    Handles the car return process.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.car_returned:
        messages.warning(request, "This car has already been returned.")
        return redirect('my_bookings')

    # Update the car return status
    booking.car_returned = True
    booking.actual_return_date = timezone.now()  # Mark the return date
    booking.save()

    # Make the car available again
    booking.car.availability = True
    booking.car.save()


    # Send confirmation email after return
    subject = "Car Return Confirmed"
    context = {
        'user': booking.user,
        'car': booking.car,
        'return_date': booking.actual_return_date,
        'booking_id': booking.id,
    }
    html_message = render_to_string('car_return_confirmation_email.html', context)
    send_mail(
        subject,
        'Your car return has been successfully processed.',
        'harshavtomy@gmail.com',
        [booking.user.email],
        fail_silently=False,
        html_message=html_message,
    )

    messages.success(request, "Thank you! The car has been returned successfully.")

    # Redirect to review page
    return redirect('submit_review', car_id=booking.car.id)

@login_required
def cancel_booking(request, booking_id):
    """
    Allows the user to cancel a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Check if the booking can be cancelled
    if booking.status == 'Cancelled':
        messages.warning(request, "This booking has already been cancelled.")
        return redirect('my_bookings')

    if booking.status != 'Confirmed':
        messages.error(request, "You can only cancel confirmed bookings.")
        return redirect('my_bookings')

    # Cancel the booking
    booking.status = 'Cancelled'
    booking.car.availability = True  # Optional: Make the car available again
    booking.car.save()
    booking.save()

    # Send a cancellation email
    subject = "Booking Cancellation Confirmation"
    message = f"""
    Dear {booking.user.username},

    Your booking (ID: {booking.id}) for {booking.car.name} has been successfully cancelled.
    Any payment made will be refunded within 7 working days.

    If you have any questions, please contact our support team.

    Thank you,
    Car Rental Service
    """
    send_mail(
        subject,
        message,
        'harshavtomy@gmail.com',  # Replace with your email
        [booking.user.email],
        fail_silently=False,
    )

    # Notify the user
    messages.success(request, "Your booking has been cancelled. Refund will be processed within 7 days.")
    return redirect('my_bookings')

@login_required
def seller_dashboard(request):
    seller = request.user.seller
    cars = Car.objects.filter(seller=seller)
    return render(request, 'seller_dashboard.html', {'cars': cars})

from .forms import CarSubmissionForm

@login_required
def seller_add_car(request):
    if request.method == 'POST':
        form = CarSubmissionForm(request.POST, request.FILES)  # Use request.FILES to handle uploaded files
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user.seller  # Assign the logged-in seller
            car.status = 'Pending'  # Set the initial status to Pending
            car.save()
            messages.success(request, "Car submitted successfully and is pending approval.")
            return redirect('seller_dashboard')  # Redirect to the seller's dashboard
        else:
            messages.error(request, "Error in form submission. Please check the details.")
    else:
        form = CarSubmissionForm()
    return render(request, 'seller_add_car.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, Review
from .forms import ReviewForm

@login_required
def submit_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # If user provided either rating or review, save it
            if form.cleaned_data.get('rating') or form.cleaned_data.get('review_text'):
                review = form.save(commit=False)
                review.user = request.user
                review.car = car
                review.save()

            return redirect('car_detail', id=car.id)  # Redirect to car detail page

    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'car': car})

from django.shortcuts import render
from django.http import HttpResponse
import csv
from datetime import date
from django.db.models import Count
from .models import Customer, Car, Booking, Review

# 📌 Customer Report
def customer_report(request):
    customers = Customer.objects.all()
    return render(request, 'reports/customer_report.html', {'customers': customers})

# 📌 Top Rented Cars Report
def top_rented_cars(request):
    top_rented = Booking.objects.values('car__name').annotate(total=Count('car')).order_by('-total')

    # Extracting car names and rental counts for visualization
    car_names = [car['car__name'] for car in top_rented]
    rental_counts = [car['total'] for car in top_rented]

    return render(request, 'reports/top_rented_cars.html', {
        'top_rented': top_rented,
        'car_names': car_names,   # Pass car names to template
        'rental_counts': rental_counts  # Pass rental counts to template
    })

# 📌 Reviews Report
def reviews_report(request):
    reviews = Review.objects.all()
    return render(request, 'reports/review_report.html', {'reviews': reviews})

# 📌 Export Customers as CSV (Download)
def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Contact'])

    for customer in Customer.objects.all():
        writer.writerow([customer.user.username, customer.user.email, customer.contact_number])

    return response

# 📌 Download CSV Report for Top Rented Cars
def download_top_rented_cars(request):
    # Fetch the top rented cars data
    top_rented = Booking.objects.values('car__name').annotate(total=Count('car')).order_by('-total')

    # Create the HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="top_rented_cars.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Car Name', 'Total Rentals'])  # Header row

    # Write data rows
    for car in top_rented:
        writer.writerow([car['car__name'], car['total']])

    return response

import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Review

from django.shortcuts import render
from django.http import HttpResponse
import csv
from collections import defaultdict
from .models import Review

def customer_reviews(request):
    reviews = Review.objects.select_related('car', 'user__customer').all()

    # Aggregating ratings for each car
    car_ratings = defaultdict(list)
    for review in reviews:
        car_ratings[review.car.name].append(review.rating)

    car_names = list(car_ratings.keys())
    avg_ratings = [round(sum(ratings) / len(ratings), 1) for ratings in car_ratings.values()]  # Compute average

    context = {
        'reviews': reviews,
        'car_names': car_names,
        'avg_ratings': avg_ratings
    }
    
    return render(request, 'review_report.html', context)



# 📌 View for Downloading Reviews as CSV
def download_reviews(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_reviews.csv"'

    writer = csv.writer(response)
    writer.writerow(['Car Name', 'Customer Name', 'Rating', 'Review'])

    reviews = Review.objects.select_related('car', 'user__customer')
    for review in reviews:
        writer.writerow([
            review.car.name,
            review.user.customer.customer_name,
            review.rating,
            review.review_text
        ])

    return response
