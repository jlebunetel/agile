"""
WSGI config for myapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            os.environ.setdefault(key, value)

application = get_wsgi_application()
