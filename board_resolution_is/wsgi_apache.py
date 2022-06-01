"""
WSGI config for board_resolution_is project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# TODO: Add the repo's directory to the PYTHONPATH
# These 2 lines are needed on a Windows server
# Root folder and django project folder
# USE FORWARD SLASH!
# sys.path.append('C:/Users/Kyle/repos/board_resolution_is')
# sys.path.append('C:/Users/Kyle/repos/board_resolution_is/board_resolution_is')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_resolution_is.settings')

application = get_wsgi_application()
