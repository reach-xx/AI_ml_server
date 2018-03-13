import sys
import os
import face_identify
from AI_ml_interface import FaceServiceAPI
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

    def FI_add_face_database(self, uid, user_info, group_id, b64code):
        """将人脸加入数据库中"""
        rand = uuid.uuid4()
        name = "faces_img/face_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))
        FaceAPI = FaceServiceAPI()
        ret = FaceAPI.add_face(uid, user_info, group_id, name)
        os.remove(name)
        return ret

    def FI_del_face_database(self, uid, group_id):
        FaceAPI = FaceServiceAPI()
        ret = FaceAPI.del_face(uid, group_id)
        return ret

    def FI_update_face_database(self, uid, user_info, group_id, b64code):
        ret = self.FI_del_face_database(uid,group_id)
        ret = self.FI_add_face_database(uid, user_info, group_id, b64code)
        return ret

    def FI_find_user_info(self, uid):
        FaceAPI = FaceServiceAPI()
        FaceAPI.find_user_info(uid)
        return 1

    def FI_find_group_users(self, group_id):
        FaceAPI = FaceServiceAPI()
        info = FaceAPI.find_group_faces(group_id)
        return info

    def FI_face_database_identify(self, group_id, b64code):
        rand = uuid.uuid4()
        name = "faces_img/identify_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))
        FaceAPI = FaceServiceAPI()
        params = FaceAPI.face_identify(group_id, name)
        os.remove(name)
        return params

    def FI_face_database_verify(self, uid, user_info, group_id, imagename):
        pass

    def FI_group_deleteuser(self, uid, group_id):
        pass

    def FI_group_adduser(self, src_group_id, group_id, uid):
        pass

    def FI_face_detect(self, b64code):
        rand = uuid.uuid4()
        name = "faces_img/detect_"+str(rand)+".jpg"
        with open(name, "wb") as w:
            w.write(base64.b64decode(str.encode(b64code)))
        FaceAPI = FaceServiceAPI()
        ret = FaceAPI.faces_detect(name)
        os.remove(name)
        return ret

    def FI_face_match(self, image1, image2):
        pass


"""thrift program start server"""
if __name__ == "__main__":
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
