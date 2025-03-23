import os
from pathlib import Path

# ✅ Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret Key (For Development Only, Use Environment Variables in Production)
SECRET_KEY = 'django-insecure-ia8n$(s6v6k$v8_c@rjg2)^195&%6l4j855=n$a*%2^=z*4!a('

# ✅ Debug Mode (Keep False in Production)
DEBUG = True

# ✅ Allowed Hosts (Include Localhost for Testing)
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ✅ Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',  # Your App
]

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Root URL Configuration
ROOT_URLCONF = 'online_courses_website.urls'

# ✅ Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',  # ✅ Added `media`
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ WSGI Application
WSGI_APPLICATION = 'online_courses_website.wsgi.application'

# ✅ Database (Using SQLite for Development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Media Settings (For Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ✅ Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Security: Trusted CSRF Origins (Add Razorpay Here)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",  # Local Development
    "https://api.razorpay.com",  # ✅ Required for Razorpay
]

# ✅ Razorpay API Keys (Replace with Your Actual Keys)
RAZORPAY_KEY_ID = "rzp_test_L2oHTkX5BzBNAK"  # ⚠️ Replace with actual Razorpay Key ID
RAZORPAY_KEY_SECRET = "4slF4XbOfVrC35oIlOrjy5fn"   # ⚠️ Replace with actual Razorpay Secret

# ✅ Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
