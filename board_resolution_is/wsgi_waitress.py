"""
WSGI config for board_resolution_is project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_resolution_is.settings')

DEBUG = os.environ.get('BRIS_DEBUG', 'False') == 'True'

# WhiteNoise is for `waitress` deployment method
# NOTE: Cannot serve media files!
if DEBUG:
    application = get_wsgi_application()
else:
    application = WhiteNoise(get_wsgi_application())
