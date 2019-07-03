import time
import uuid
import happybase

# Create your views here.
# 连接hbase数据库，做日志记录的存储
def connect_hbase():
    hb = happybase.Connection(host='39.97.96.39', port=9090)
    hb.open()
    table = hb.table('log') # 列簇名为visit_info
    return table

def get_ip(request):
    ip = request.META['REMOTE_ADDR']
    return ip

# 插入数据的格式  table.put('1':{"visit_info:username": "Derek"})
#插入多条数据table.put('2',{'visit_info:username':'Derek','visit_info:gender':'male'})
def generate_log(table,name=None,phone=None,email=None,ip=None):
    t = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())   #2019/07/03-22:42:57 格式的时间
    table.put(str(uuid.uuid4()),{'visit_info:name':name,'visit_info:phone':phone,'visit_info:email':email,\
                                 'visit_info:ip':ip,'visit_info:time':t})