import os

CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
DEBUG = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
