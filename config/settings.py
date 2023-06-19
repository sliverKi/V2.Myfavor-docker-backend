#from decouple import config
from pathlib import Path
import os
import environ
import dj_database_url
#>>4월 8일 db 연결, data 다시 넣어야 함. 

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ["*"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    'storages',
    "corsheaders",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "usersCalendar.apps.UserscalendarConfig",
    "common.apps.CommonConfig",
    "medias.apps.MediasConfig",
    "idols.apps.IdolsConfig",
    "categories.apps.CategoriesConfig",
    "groups.apps.GroupsConfig",
    "prizes.apps.PrizesConfig",
    "schedules.apps.SchedulesConfig",
    "oauth.apps.OauthConfig",
    "search.apps.SearchConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# DEBUG = True
if DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR,'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    DATABASES = {
            'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR/ 'db.sqlite3',
                }
        }
else:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
        )
                    
    }
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

DATE_INPUT_FORMATS = ["%Y-%m-%d"]

DATE_FORMAT = "F j"

USE_I18N = False

USE_TZ = False

STATIC_URL = "/static/"
if not DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"


MEDIA_ROOT = "uploads"
MEDIA_URL = "user-uploads/"

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW = True
CORS_ALLOWED_ORIGINS_ALL = True
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
CSRF_TRUSTED_ORIGINS =["http://127.0.0.1:3000", "http://localhost:3000"]



CF_TOKEN=env("CF_TOKEN")
CF_ID=env("CF_ID")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True  
ACCOUNT_SESSION_REMEMBER = True  
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_SECURE=False
SESSION_COOKIE_DOMAIN="127.0.0.1"
CSRF_COOKIE_DOMAIN="127.0.0.1"

#gmail SMTP
# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST="smtp.gmail.com"
# EMAIL_PORT=587
# EMAIL_HOST_USER=env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS=True
# DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
# PASSWORD_RESET_CONFIRM_URL = 'password_reset_confirm'

#AWS-Iam-accessKey
# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID") # .csv 파일에 있는 내용을 입력 Access key ID
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY") # .csv 파일에 있는 내용을 입력 Secret access key
# AWS_REGION = env("AWS_REGION")

#S3 Storages
# AWS_STORAGE_BUCKET_NAME =env("AWS_STORAGE_BUCKET_NAME")  # 설정한 버킷 이름
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)#img upload endpoint
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_S3_FILE_OVERWRITE=False
# DEFAULT_FILE_STORAGE = 'config.utils.CustomS3Boto3Storage'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'path/to/store/my/files/')