#from decouple import config
from pathlib import Path
import os
import environ
import dj_database_url
#git merge origin/main
#devlop@gmail.com-develop
#repo Connection : v2-Myfavor-docker-backend 
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    ".choeaein.click", 
    "www.choeaein.click",
    "https://www.choeaein.click", 
    "https://backend.choeaein.click",
    "13.228.225.19",
    "18.142.128.26",
    "54.254.162.138",
]



RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

THIRD_PARTY_APPS = [
    'corsheaders',
    "rest_framework",
    "rest_framework.authtoken",
    'storages',
    'debug_toolbar',
    'django_seed',
]

CUSTOM_APPS = [
    "boards.apps.BoardsConfig",
    "users.apps.UsersConfig",
    "usersCalendar.apps.UserscalendarConfig",
    "common.apps.CommonConfig",
    "medias.apps.MediasConfig",
    "idols.apps.IdolsConfig",
    "groups.apps.GroupsConfig",
    "prizes.apps.PrizesConfig",
    "schedules.apps.SchedulesConfig",
    "oauth.apps.OauthConfig",
    "search.apps.SearchConfig",
    "solos.apps.SolosConfig",
    "albums.apps.AlbumsConfig",
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
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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


DEBUG = 'RENDER' not in os.environ  #딕셔너리 key에 RENDER라는 환경변수가 설정되어 있지 않은경우(=개발환경인 경우)에만 True 반환
# DEBUG = True

if DEBUG:#개발 환경에서의 설정

    STATIC_ROOT=os.path.join(BASE_DIR,'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    DATABASES = {
             'default': {
                     'ENGINE': 'django.db.backends.sqlite3',
                     'NAME': BASE_DIR/ 'db.sqlite3',
                 }
         }
    
else:#베포환경에서의 설정
    
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

USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"


MEDIA_ROOT = "uploads"
MEDIA_URL = "user-uploads/"

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW = True
# CORS_ALLOWED_ORIGINS_ALL = True#모든 호스트 허용
CORS_ORIGIN_WHITELIST = [
    "https://www.choeaein.click"  
]
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Set-Cookie',
)
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CSRF_TRUSTED_ORIGINS =(
    "http://127.0.0.1:3000", 
    "http://localhost:3000",
    "https://www.choeaein.click"
)
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True  
ACCOUNT_SESSION_REMEMBER = True  
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

AUTH_COOKIE_DOMAIN = ".choeaein.click"
SESSION_COOKIE_DOMAIN = ".choeaein.click"
CSRF_COOKIE_DOMAIN = ".choeaein.click"

CSRF_COOKIE_SECURE = False
AUTH_COOKIE_SECURE = False
SESSION_COOKIE_SECURE=False

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_HTTPONLY = False


CF_TOKEN=env("CF_TOKEN")
CF_ID=env("CF_ID")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
}

#debug tool-bar        
INTERNAL_IPS=[
    '127.0.0.1',
]

#gmail SMTP
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER=env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
PASSWORD_RESET_CONFIRM_URL = 'password_reset_confirm'

# FRONTEND_URL='127.0.0.1:3000/signup/user'
FRONTEND_URL='https://www.choeaein.click/signup/user'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'#(email인증을 하지 않으면 로그인 할 수 없음.)
ACCOUNT_CONFIRM_EMIAL_ON_GET = True #(인증 링크를 누르면 바로 확인이 되게 함 )
#ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1


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

CACHE_TTL=15
CACHES={
    'default':{
        'BACKEND':'django_redis.cache.RedisCache',
        'LOCATION':'redis://127.0.0.1:6379/1',
        'OPTIONS':{
            'CLIENT_CLASS':'django_redis.client.DefaultClient',
            'TIMEOUT':5,
        },
    }
}

