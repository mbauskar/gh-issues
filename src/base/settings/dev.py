from base.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'gh-issue.sqlite3',
    }
}