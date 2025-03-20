"""
Django settings for car project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cpx@2u+gl$dtqdbntr4bft8mc@bal86@up73nz&*akq=8**1-9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'carapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'car.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'assets')

MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

# Define media file settings
MEDIA_URL = '/media/'  # URL to access media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory to store uploaded media files

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'harshavtomy@gmail.com'
EMAIL_HOST_PASSWORD = 'cgpe kwyw dpki pbac'
# DEFAULT_FROM_EMAIL = 'harshavtomy@gmail.com'  # or another email address

# settings.py
STRIPE_PUBLISHABLE_KEY = "pk_test_51QefefPQRj0Y9B8jj53VDApfec6bUf92wRbcGuWka3oThck8SqK999qhDWotrZc0JvTY0GwkOxGaNKjnBSiPyOgB002GKTtc4T"  # Publishable Key
STRIPE_SECRET_KEY = "sk_test_51QefefPQRj0Y9B8j2t7iDhsxHKJbip3MhUuK4JxF0STESb0RNtO4S9sqlumIwbH6TRqIc8L1OFw0V6JxUZvu5ozc006Dg3gm1U"  # Secret Key

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "AdminDashboard",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "CARBOOK",
    
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "carrental logo.png",
    
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-square",
    
    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Customers", "url": "http://127.0.0.1:8000/admin/carapp/customer/", "new_window": False},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Car", "url": "http://127.0.0.1:8000/admin/carapp/car/", "new_window": False},

    ],

"custom_links": {
    "carapp": [
        {
            # Any Name you like
            "name": "Customer Report",
            
            "new_window": True,

            # url name e.g admin:index, relative urls e.g /admin/index or absolute urls e.g https://domain.com/admin/index
            "url": "http://127.0.0.1:8000/reports/customers/",

            # any font-awesome icon
            "icon": "fas fa-users",     
        },
        {
            "name": "Review report",
            "new_window": True,
            "url": "http://127.0.0.1:8000/reports/reviews/",
            "icon": "fas fa-chart-bar"
        },
        {
            "name": "Top rented cars",
            "new_window": True,
            "url": "http://127.0.0.1:8000/reports/top-rented-cars/",
            "icon": "fas fa-chart-bar"
        }
        
    ]
},

    
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],

    # Order apps automatically, but make sure choice and book admin links are first within the books app
    "order_with_respect_to": ["carapp.Customer", "carapp.Seller","carapp.Car"],

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "CARBOOK",
    "welcome_sign": "Welcome to the AdminDashboard",
    "copyright": "CARBOOK Ltd",
     "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "gadgetapp.Address": "fas fa-address-book",
        "gadgetapp.Customer": "fas fa-user",
        "gadgetapp.Seller": "fas fa-user",
        "gadgetapp.Product": "fas fa-ad",
        "books.Genre": "fas fa-photo-video",
        "loans.BookLoan": "fas fa-book-open",
        "loans.Library": "fas fa-book-reader",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lux",
    "dark_mode_theme": "slate",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}



