import datetime
import uuid
import happybase
import requests
from lxml import etree

# Create your views here.
# 连接hbase数据库，做日志记录的存储
class Log(object):
    def __init__(self,func):
        self.func= func # func代表被装饰的函数
        # self.request = request
        self.log = self.table('log')

    def __call__(self, request):
        self.request = request
        self.log.put(self.rowkey,{'visit_info:name':self.name,'visit_info:ip':self.ip,'visit_info:ipaddress':self.ipaddress,'visit_info:url':self.url,\
        'visit_info:time':self.time})
        self.query('log')
        return self.func(request)

    def table(self,table):
        return self.hbsae.table(table)

    @property
    def rowkey(self):
        row_key = str(uuid.uuid4())
        return row_key
    @property
    def hbsae(self):
        hb = happybase.Connection(host='39.97.96.39', port=9090)
        hb.open()
        return hb
    @property
    def name(self):
        return  self.request.session.get('name')
    @property
    def ip(self):
        ip = self.request.META.get('REMOTE_ADDR',None)
        return ip

    @property
    def ipaddress(self):
        return Log.getAddress(self.ip)

    @property
    def url(self):
        return self.request.path_info

    @property
    def time(self):
        t = str(datetime.datetime.now()).split('.')[0] #2019-07-04 17:02:42  格式的时间
        # t = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())  # 2019/07/03-22:42:57 格式的时间
        return t

    def create_table(self,table,row):
        self.hbsae.create_table(table, {row: {}})

    def delete_table(self,table):
        self.hbsae.delete_table(name=table, disable=True)

    def query(self,table):
        # table.put('1', {'visit_info:username': 'Derek', 'visit_info:gender': 'male'})
        # row = table.row("2")
        scaner = self.table(table).scan()
        for i in scaner:
            print(i)

    @staticmethod
    def getAddress(ip):  # 得到ip所属地址的方法
        url = 'http://www.ip138.com/ips138.asp?ip=' + ip + '&action=2'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_f4f76646cd877e538aa1fbbdf351c548=1562224888; Hm_lpvt_f4f76646cd877e538aa1fbbdf351c548=1562224888; ASPSESSIONIDCSDBTACB=ECEPGKBBJABOGLOBFNLJLCIC; Hm_lvt_b018ba5033f3b0d184416653ad858a48=1562224904; Hm_lpvt_b018ba5033f3b0d184416653ad858a48=1562224918',
            'Host': 'www.ip138.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        resp = requests.get(url=url, headers=headers)
        resp.encoding = resp.apparent_encoding
        html = etree.HTML(resp.text)
        msg = html.xpath('//ul[@class="ul1"]/li/text()')[0]
        msg = msg.split('本站数据：')[1]
        return msg  # ip查询的地址
# 插入数据的格式  table.put('1':{"visit_info:username": "Derek"})
#插入多条数据table.put('2',{'visit_info:username':'Derek','visit_info:gender':'male'})
