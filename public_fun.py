import time
import uuid
import happybase

# Create your views here.
# 连接hbase数据库，做日志记录的存储
class Log(object):
    def __init__(self,func):
        self.func= func # func代表被装饰的函数
        # self.request = request
        self.log = self.table('log')

    def __call__(self, request):
        self.request = request
        self.log.put(self.rowkey,{'visit_info:name':self.name,'visit_info:ip':self.ip,'visit_info:url':self.url,\
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
    def url(self):
        return self.request.path_info
    @property
    def time(self):
        t = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())  # 2019/07/03-22:42:57 格式的时间
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
# 插入数据的格式  table.put('1':{"visit_info:username": "Derek"})
#插入多条数据table.put('2',{'visit_info:username':'Derek','visit_info:gender':'male'})
