"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
#import django_heroku
from pathlib import Path
import os
import logging.config
import cloudinary
import django_cache_url


# # Base Configuration ========================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kjhjksjkfhdskfdfklhlksdhfkdsfksh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "optional"


# AXES_ONLY_ADMIN_SITE = True #Only apply restricitons to admin sites

# WARNING: this has to be true if the real ip address is not passed through usually behind a proxy or this will cause everyone to be blocked
AXES_ONLY_USER_FAILURES = True  # only apply restrictions based on username

AXES_NEVER_LOCKOUT_GET = True  # never lock out get requests


# Axes Proxy stuff is not working
AXES_PROXY_COUNT = 1

# AXES_META_PRECEDENCE_ORDER = [
#    'HTTP_X_FORWARDED_FOR',
#    'REMOTE_ADDR',
# ]

AXES_COOLOFF_TIME = 1  # 1 hour cooloff time
AXES_FAILURE_LIMIT = 100


# Disable Caching in development
if DEBUG:

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    pass
    # CACHES = {
    #     "default": django_cache_url.parse(os.getenv("MEMCACHED_URL"))
    # }  # set by dokku automatically when linking apps


# # Sentry Monitoring Configuration ========================================================
# only in production
if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_KEY"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.3,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )


ALLOWED_HOSTS = ['*']

# # Email Configuration ========================================================
ADMINS = [("CT", "calorietrackerio@gmail.com")]
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "calorietrackerio@gmail.com"
SERVER_EMAIL = "calorietrackerio@gmail.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "calorietrackerio@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Deprecated
# # Stripe Configuration ========================================================
# STRIPE_LIVE_PUBLIC_KEY = os.getenv("STRIPE_LIVE_PUBLIC_KEY")
# STRIPE_LIVE_SECRET_KEY = os.getenv("STRIPE_LIVE_SECRET_KEY")
# STRIPE_TEST_PUBLIC_KEY = os.getenv("STRIPE_TEST_PUBLIC_KEY")
# STRIPE_TEST_SECRET_KEY = os.getenv("STRIPE_TEST_SECRET_KEY")
# STRIPE_LIVE_MODE = os.getenv("STRIPE_LIVE_MODE", False)
# DJSTRIPE_WEBHOOK_VALIDATION = None

# # Cloudinary Configuration ========================================================
cloudinary.config(
    cloud_name="calorietracker-io",
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# # Log in/out Configuration ========================================================
LOGIN_REDIRECT_URL = "/logdata"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "login"

MULTIFACTOR = {
    # False, or dotted import path to function to process after successful authentication
    "LOGIN_CALLBACK": False,
    # 'RECHECK': True,                     # Invalidate previous authorisations at random intervals
    # 'RECHECK_MIN': 60 * 60 * 3,          # No recheks before 3 hours
    # 'RECHECK_MAX': 60 * 60 * 6,          # But within 6 hours
    #
    # 'FIDO_SERVER_ID': 'example.com',     # Server ID for FIDO request
    # 'FIDO_SERVER_NAME': 'Django App',    # Human-readable name for FIDO request
    # TOTP token issuing name (to be shown in authenticator)
    "TOKEN_ISSUER_NAME": "CalorieTracker.io",
    # 'U2F_APPID': 'https://example.com',  # U2F request issuer
}


# # Logging Configuration ========================================================
# Only in production
# Get loglevel from env
# LOGGING_CONFIG = None
LOGLEVEL = os.getenv("DJANGO_LOGLEVEL", "info").upper()
if not DEBUG:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                },
                "mail_admins": {
                    "level": "ERROR",
                    "class": "django.utils.log.AdminEmailHandler",
                    "email_backend": EMAIL_BACKEND,
                    "reporter_class": "django.views.debug.ExceptionReporter",
                },
            },
            "loggers": {
                "": {
                    "level": LOGLEVEL,
                    "handlers": [
                        "console",
                        "mail_admins",
                    ],
                },
            },
        }
    )


# # Applications Configuration ========================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # needed by pinax.referrals
    "calorietracker",
    "api",
    # third party packages/apps
    "rest_framework",
    "safedelete",
    "crispy_forms",
    "bootstrap_datepicker_plus",
    "chartjs",
    "measurement",
    "pinax.referrals",
    # "djstripe", deprecated
    "cloudinary",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.discord",
    "allauth.socialaccount.providers.google",
    "sslserver",
    "friendship",
    "debug_toolbar",
    "request",
    "corsheaders",
    "axes",
    "multifactor",
    "pinax.announcements",
    "actstream",
    "bootstrapform",
    "pinax.templates",
    "pinax.messages",
]

# 1 == dev domaine and sitename
# 2 == production domaine and sitename
SITE_ID = 1 if DEBUG else 2  # see migration 0008_Configure_Site_Names for more info


CORS_ALLOW_ALL_ORIGINS = True if DEBUG else False

CRISPY_TEMPLATE_PACK = "bootstrap4"

PINAX_REFERRALS_SECURE_URLS = False if DEBUG else True


# # Middleware ========================================================
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "pinax.referrals.middleware.SessionJumpingMiddleware",
    "request.middleware.RequestMiddleware",
    "axes.middleware.AxesMiddleware",
]


# Django_debug_toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# # URLCONF ========================================================
ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"

# # Templates ========================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "calorietracker.context_processors.notifications.notifications_count",
                "calorietracker.context_processors.notifications.notifications",
                "calorietracker.context_processors.coachclients.isCoach",
                "pinax.messages.context_processors.user_messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
                "pinax.messages.context_processors.user_messages",
            ],
        },
    },
]


# # Database(s) ========================================================
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# # Cockroach
# DATABASES = {
#     'default': {
#         'ENGINE': 'django_cockroachdb',
#         'NAME': 'django6',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '26257',
#         # If connecting with SSL, include the section below, replacing the
#         # file paths as appropriate.
#         # 'OPTIONS': {
#         #     'sslmode': 'require',
#         #     'sslrootcert': '/certs/ca.crt',
#         #     # Either sslcert and sslkey (below) or PASSWORD (above) is
#         #     # required.
#         #     'sslcert': '/certs/client.myprojectuser.crt',
#         #     'sslkey': '/certs/client.myprojectuser.key',
#         # },
#     },
# }

# Yugabyte
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ysql_django',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '5433',
#     }
# }


# # Password Validation ========================================================
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
# ]


# # Internationalization ========================================================
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# # Static Files(CSS, JavaScript, Images) ========================================================
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"

# # Media Files ========================================================
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# # Heroku ========================================================
# Configure Django App for Heroku.
#django_heroku.settings(locals())

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# # Provider specific settings
# https://django-allauth.readthedocs.io/en/latest/providers.html#facebook
SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "js_sdk",
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "name",
            "name_format",
            "picture",
            "short_name",
        ],
        "EXCHANGE_TOKEN": True,
        # 'LOCALE_FUNC': 'path.to.callable',
        "VERIFIED_EMAIL": False,
        "VERSION": "v7.0",
        "APP": {
            "client_id": os.getenv("ZUCC_APP_ID"),
            "secret": os.getenv("ZUCC_APP_SECRET"),
        },
    },
    "discord": {
        "APP": {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "secret": os.getenv("DISCORD_SECRET"),
            "key": os.getenv("DISCORD_KEY"),
        }
    },
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_SECRET"),
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}
