import sys
import os
import face_identify
import json
import sqlite3
import uuid
import base64

sys.path.append('gen-py')

from identify import FaceIdentify
from identify.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

face_recognition = face_identify

class FaceServiceHandler:
    def __init__(self):
        self.log = {}

    """同时识别多张图片并计算每一张的位置"""

    def mult_faces_recognition(self,known_image):
        face_loc = face_recognition._raw_face_locations(known_image)
        for face in face_loc:
            print("-----------------------begin------------------\n")
            print(face.top(), face.right(), face.bottom(), face.left())
            print("-----------------------end------------------\n")
        locations = face_recognition.get_face_landmarks(known_image, face_loc)
        face_encodings = face_recognition.face_known_encodings(known_image, locations)
        return face_loc, face_encodings

    def FI_add_face_database(self, uid, user_info, group_id, b64code):
        """将人脸加入数据库中"""
        rand = uuid.uuid4()
        name = "faces_img/face_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))

        image = face_recognition.load_image_file(name)
        face_encoding = face_recognition.face_encodings(image)[0]
        conn = sqlite3.connect("database/faces.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO FACE_TB VALUES (?,?,?,?,?)",
                      (uid,group_id,user_info,name,
                       json.dumps(face_encoding.tolist()))
                      )
        except sqlite3.IntegrityError as IE:
            print("UID already existed!!!! ",  IE)
            conn.close()
            return -1
        conn.commit()
        # cursors = c.execute("SELECT * FROM FACE_TB")
        # for face in cursors:
        #     print("*******----------{0}------------".format(face[0]))
        #     print(face[4])
        conn.close()
        return 0

    def FI_del_face_database(self, uid, group_id):
        """
        将UID从数据库中删除
        """
        conn = sqlite3.connect("database/faces.db")
        c = conn.cursor()
        c.execute("DELETE from FACE_TB where UID='{0}';".format(uid))
        conn.commit()
        # cursors = c.execute("SELECT * FROM FACE_TB")
        conn.close()
        return 0

    def FI_update_face_database(self, uid, user_info, group_id, imagename):
        ret = self.FI_del_face_database(uid,group_id)
        ret = self.FI_add_face_database(uid, user_info, group_id, imagename)
        return ret

    def FI_find_user_info(self, uid):
        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        cursors = cur.execute("SELECT * FROM FACE_TB where UID='{0}'".format(uid))
        for face in cursors:
            print("*******----------{0}------------".format(face[0]))
            print(face[4])
        conn.close()
        return 1

    def FI_find_group_users(self, group_id):
        """
        Parameters:
         - group_id
        """
        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        cursors = cur.execute("SELECT * FROM FACE_TB where GROUP_ID='{0}'".format(group_id))
        info_name = []
        for face in cursors:
            print("+++++++++++++++++++++++++++++++++++++++++")
            print("*******----------{0}------{1}------".format(face[0], face[2]))
            print("++++++++++++++++++++++++++++++++++++++++++")
            info_name.append(face)
        conn.close()
        return info_name


    def FI_face_database_identify(self, group_id, b64code):
        rand = uuid.uuid4()
        name = "faces_img/identify_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))
        image = face_recognition.load_image_file(name)
        try:
            #unknown_face_encoding = face_recognition.face_encodings(image)[0]
            face_loc, face_encodings = self.mult_faces_recognition(image)
        except IndexError as IE:
            print("IndexError:  ",  IE)
            face_str = "[]"
            return face_str

        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        faces_encode = []
        faces_uid = []
        faces_group = []
        faces_info = []

        cursors = cur.execute("SELECT * FROM FACE_TB WHERE GROUP_ID='{0}'".format(group_id))
        for face in cursors:
            faces_uid.append(face[0])
            faces_group.append(face[1])
            faces_info.append(face[2])
            faces_encode.append(json.loads(face[4]))

        params = face_id_st()
        params.result_num = len(face_encodings)
        face_dict = {}
        cnt = 0
        if params.result_num == 0:
            print("detect no face!!!!\n")
            os.remove(name)
            return params
        for face_enc, location in zip(face_encodings,face_loc):
            results = face_recognition.compare_faces(faces_encode, face_enc)
            length = len(results)
            print("-----------------------begin--------------------------\n")
            print("=:", results)
            print("=:", faces_info)
            print("------------------------end-------------------------\n")
            idx = results.index(min(results))
            #相似度
            if results[idx] < 0.45:
                f_info = face_info()
                f_info.uid = faces_uid[idx]
                f_info.group = faces_group[idx]
                f_info.info = faces_info[idx]
                print(faces_encode[idx])
                face_rect = rectangle()
                face_rect.top = location.top()
                face_rect.right = location.right()
                face_rect.bottom = location.bottom()
                face_rect.left = location.left()
                f_info.rect = face_rect
                face_dict[cnt] = f_info
                cnt += 1
            else:
                print("face No recognition result:", results)
        params.result_num = cnt
        if cnt > 0:
            params.result = face_dict
        else:
            params.result = {}
        conn.close()
        os.remove(name)
        print(params)
        return params

    def FI_face_database_verify(self, uid, user_info, group_id, imagename):
        """
        Parameters:
         - uid
         - user_info
         - group_id
         - imagename
        """
        pass

    def FI_group_deleteuser(self, uid, group_id):
        """
        Parameters:
         - uid
         - group_id
        """
        pass

    def FI_group_adduser(self, src_group_id, group_id, uid):
        """
        Parameters:
         - src_group_id
         - group_id
         - uid
        """
        pass

    def FI_face_detect(self, b64code):
        rand = uuid.uuid4()
        name = "faces_img/detect_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))
        image = face_recognition.load_image_file(name)
        face_locations = face_recognition.face_locations(image, model="hog")
        faces_num = (len(face_locations))
        result = []
        d_info = face_detect_st()
        d_info.result_num = len(face_locations)
        if d_info.result_num  == 0:
            os.remove(name)
            print("detect no Faces!!!!!\n")
            return d_info
        m_faces = {}
        cnt  = 0
        # 循环找到的所有人脸
        for face_location in face_locations:
            # 打印每张脸的位置信息
            face_rect = rectangle()
            face_rect.top, face_rect.right, face_rect.bottom, face_rect.left = face_location
            m_faces[cnt] = face_rect
            cnt += 1
        d_info.result = m_faces
        os.remove(name)
        return d_info

    def FI_face_match(self, image1, image2):
        """
        Parameters:
         - image1
         - image2
        """
        pass


handler = FaceServiceHandler()
processor = FaceIdentify.Processor(handler)
transport = TSocket.TServerSocket(port=50040)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
# server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print('Starting the server...')
server.serve()
print('done.')
