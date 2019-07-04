import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
default_app_config = 'sales.apps.SalesConfig'