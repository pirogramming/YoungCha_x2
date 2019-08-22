from YoungCha_x2.settings.common import *

DEBUG = True

ALLOWED_HOSTS = [

    '127.0.0.1',
    'http://127.0.0.1:8000/admin',
    'kiljaeeun.pythonanywhere.com'

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
