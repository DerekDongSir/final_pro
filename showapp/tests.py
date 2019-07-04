from django.test import TestCase
from public_fun import Log
import django,os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pro.settings")
django.setup()
# Create your tests here.
log = Log(lambda :None)

if __name__ == '__main__':
    log.query('log')