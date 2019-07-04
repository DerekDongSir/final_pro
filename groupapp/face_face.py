from PIL import Image
import uuid, os, MySQLdb, face_recognition


class Face_to_Face(object):
    # 创建对象时，传入：
    # data_name : 存放静态文件的地方；
    # table：你的库的存放对应关系的表名

    # 调用对比验证的方法时，传入：
    # user_name用户名（str）：
    # unknow_face传入需要识别的图片（str）：文件路径
    # yu_zhi阈值（float）：0是完全 一样，最大是1，越大越不像，建议0.5以下

    def __init__(self, data_name,table=None):
        self.data_name = data_name
        self.conn = MySQLdb.connect(host='rm-m5eid02685j03n7882o.mysql.rds.aliyuncs.com',  # mysql所在主机的ip
                                    port=3306,  # mysql的端口号
                                    user='znz',  # mysql 用户名
                                    password='Zhao0110282',  # mysql 的密码
                                    db='final',  # 要使用的库名
                                    charset="utf8")
        self.coun = self.conn.cursor()
        self.table = str(table)

    def face_yanzheng(self, user_name, unknown_face,yu_zhi):
        unknow_user = face_recognition.load_image_file(unknown_face)
        unknowencoding = face_recognition.face_encodings(unknow_user)[0]
        hehe = self.read_face(user_name)
        for i in hehe:
            face_distances = face_recognition.face_distance([unknowencoding], i)
            if face_distances[0]<yu_zhi:
                print('123')
                return True
        print('453')
        return False

    def add_face(self, user_name, face):
        image = face_recognition.load_image_file(face)
        face_locations = face_recognition.face_locations(image)
        try:
            top, right, bottom, left = face_locations[0]
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            face_name = self.data_name + '/' +user_name+'/'+ self.generateUUID(user_name) + '.jpg'
            sql = 'insert into '+self.table+'(user_name,face) values("%s","%s")'%(user_name,face_name)
            self.coun.execute(sql)
            self.conn.commit()
            self.mkdir(self.data_name+'/'+user_name)
            pil_image.save(face_name)
            return True
        except:
            return False

    def read_face(self, user_name):
        face_list=[]
        self.coun.execute('select face from '+self.table+' where user_name="'+user_name+'"')
        for i in self.coun.fetchall():
            user_face = face_recognition.load_image_file(i[0])
            face_list.append(face_recognition.face_encodings(user_face)[0])
        return face_list

    def generateUUID(self, filename):  # 创建唯一的文件名
        id = str(uuid.uuid4())
        extend = os.path.splitext(filename)[1]
        return id + extend

    def mkdir(self,path):
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建目录
             # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            return False
