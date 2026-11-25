
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = list(
    dict.fromkeys(
        [
            host.strip()
            for host in os.environ.get(
                "ALLOWED_HOSTS",
                "localhost,127.0.0.1,portfolio-backend-89s1.onrender.com",
            ).split(",")
            if host.strip()
        ]
        + [
            "localhost",
            "127.0.0.1",
            "portfolio-backend-89s1.onrender.com",
        ]
    )
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portfolio',
    "rest_framework",
    "corsheaders",#to connect react and django diffrent url
    "cloudinary",
    "cloudinary_storage",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Origins allowed to call this API from a browser.
# The deployed frontend origins are always allowed, even if the hosting
# dashboard sets CORS_ALLOWED_ORIGINS to a partial list.
_SITE_ORIGINS = [
    "https://shahprashant.com.np",
    "https://www.shahprashant.com.np",
]

CORS_ALLOWED_ORIGINS = list(
    dict.fromkeys(
        [
            origin.strip()
            for origin in os.environ.get(
                "CORS_ALLOWED_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,"
                + ",".join(_SITE_ORIGINS),
            ).split(",")
            if origin.strip()
        ]
        + _SITE_ORIGINS
    )
)

# Lets Django accept HTTPS POSTs (contact form, admin login) from the live site.
CSRF_TRUSTED_ORIGINS = list(
    dict.fromkeys(
        [
            origin.strip()
            for origin in os.environ.get(
                "CSRF_TRUSTED_ORIGINS", ",".join(_SITE_ORIGINS)
            ).split(",")
            if origin.strip()
        ]
        + _SITE_ORIGINS
    )
)

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS= True
# Fail fast instead of letting the browser request hang for minutes.
EMAIL_TIMEOUT = 15

# acess using .env file
EMAIL_HOST_USER= os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD= os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# Where contact-form notifications are delivered. Defaults to the SMTP account,
# but you can point it at a different inbox (CONTACT_EMAIL env var) so the
# message is not From and To the same Gmail address, which Gmail often flags
# as spam.
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL") or EMAIL_HOST_USER

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}