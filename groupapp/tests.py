from django.test import TestCase
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pro.settings")
django.setup()
# Create your tests here.
from groupapp.models import Person


def test_db():
    user = Person.objects.get(name='Derek')
    status = user.status
    print(status)

test_db()