from os import environ
import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv()

REST_KEY = os.environ.get('OTREE_REST_KEY')

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '_templates')], # This is the critical line
        'APP_DIRS': True,
    },
]

FOOTER_HTML = '© 2026 Social Science Experimental Lab | <a href="mailto:mayada@nyu.edu">Contact Us</a>'

SESSION_CONFIGS = [
    dict(
        name='public_goods',
        display_name="Public Goods",
        app_sequence=['app'],
        num_demo_participants=2,
        treatment='PG'
    ),

    dict(
        name='public_goods_punishment',
        display_name="Public Goods with Punishment",
        app_sequence=['app'],
        num_demo_participants=2,
        treatment='PG_P'
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0, participation_fee=0, doc=""
)
PARTICIPANT_FIELDS = ['name']

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5548332774700'

DEBUG = False