import time

import happybase
from django.test import TestCase
import django,os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pro.settings")
django.setup()
# Create your tests here.

def hbase():
    hb = happybase.Connection(host='39.97.96.39', port=9090)
    hb.open()
    # hb.create_table('log', {"visit_info": {}})
    table = hb.table('log')
    # table.put("1", {"visit_info:username": "Derek"})
    table.put('2', {'visit_info:username': 'Derek', 'visit_info:gender': 'male'})
    row = table.row("2")
    print(row)

if __name__ == '__main__':
    t = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())  # 2019/07/03-22:42:57 格式的时间
    t = t.encode(encoding='utf-8')
    print(t)
