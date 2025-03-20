from django.contrib import admin
from .models import Car,Customer,Seller, Category, Subcategory,Blog
from django.utils.html import format_html
from django.contrib import messages
from django.core.mail import send_mail

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_no', 'address']
    search_fields = ['name', 'email', 'phone_no']

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]

    def get_subcategory_count(self, obj):
        return obj.subcategory_set.count()

    get_subcategory_count.short_description = 'Subcategory Count'

    list_display = ['category_name', 'get_subcategory_count']
    search_fields = ['category_name']


from django.utils.html import format_html
from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'year', 'price_per_day', 'availability', 
                    'is_featured', 'status', 'seller', 'view_documents')
    search_fields = ['name', 'brand']
    list_filter = ('status', 'brand', 'year', 'fuel_type')
    
    # Make document fields read-only
    readonly_fields = ('document_proof', 'insurance_copy', 'registration_certificate')
    
    actions = ['approve_cars', 'reject_cars']
    
    def view_documents(self, obj):
        """
        Display links to view the uploaded documents in the admin panel.
        """
        links = []
        if obj.document_proof:
            links.append(f'<a href="{obj.document_proof.url}" target="_blank">Ownership Proof</a>')
        if obj.insurance_copy:
            links.append(f'<a href="{obj.insurance_copy.url}" target="_blank">Insurance Copy</a>')
        if obj.registration_certificate:
            links.append(f'<a href="{obj.registration_certificate.url}" target="_blank">Registration Certificate</a>')
        
        return format_html('<br>'.join(links) if links else "No Documents Provided")
    view_documents.short_description = "Uploaded Documents"
    
    def approve_cars(self, request, queryset):
        """
        Approve selected cars only if their status is 'Pending'.
        """
        pending_cars = queryset.filter(status='Pending')
        if pending_cars.exists():
            pending_cars.update(status='Approved')
            self.message_user(request, f"{pending_cars.count()} cars have been approved.")
        else:
            self.message_user(request, "No pending cars to approve.", level='warning')
    approve_cars.short_description = "Approve selected cars"
    
    def reject_cars(self, request, queryset):
        """
        Reject selected cars only if their status is 'Pending'.
        """
        pending_cars = queryset.filter(status='Pending')
        if pending_cars.exists():
            pending_cars.update(status='Rejected')
            self.message_user(request, f"{pending_cars.count()} cars have been rejected.")
        else:
            self.message_user(request, "No pending cars to reject.", level='warning')
    reject_cars.short_description = "Reject selected cars"



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'contact_number']
    search_fields = ['customer_name', 'email', 'contact_number']
    
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'return_date', 'total_price', 'status','payment_status')  # Ensure these fields exist
    list_filter = ('status', 'car', 'user', 'start_date', 'return_date','payment_status')
    list_editable = ('status',)


admin.site.register(Blog)

from .models import Review

admin.site.register(Review)