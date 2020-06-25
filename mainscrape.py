from django.conf import settings
import django

from thegiftrank.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from products.models import *


STORE = Store.objects.get(name="Amazon")
