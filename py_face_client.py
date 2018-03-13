import sys, glob

sys.path.append('gen-py')

from identify import FaceIdentify
from identify.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import base64

try:
    # Make socket
    transport = TSocket.TSocket('192.168.10.248', 50040)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = FaceIdentify.Client(protocol)
    # Connect!
    transport.open()
    # info = client.FI_face_detect('d003.jpg')
    # print('information:   ', info)

    #client.FI_add_face_database('101', 'biden','group02', 'biden.jpg')
    # client.FI_add_face_database('002', 'obama','group02', 'obama.jpg')
    #ret = client.FI_del_face_database('100','group02')
    #print(ret) 
    # client.FI_find_user_info("004")
    # group_id = "group02"
    #
    # with open("known/xuch.jpg", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # # client.FI_add_face_database("085", "徐崇",'group02', b64str)
    # with open("known/linyisu.jpg", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("088", "林义苏",'group02', b64str)
    #with open("known/yuanjie.jpg", "rb") as f:
    #    b64code = base64.b64encode(f.read())
    #b64str = bytes.decode(b64code)
    #client.FI_add_face_database("091", "袁洁",'group02', b64str)
    # with open('known/yangshaohua.jpg', "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("082", "杨邵华",'group02', b64str)
    # with open('known/lijunbao1.jpg', "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("083", "李军宝",'group02', b64str)
    # with open('known/dingzhaozhu.jpg', "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("084", "丁兆柱",'group02', b64str)
    #with open('known/zhangqiu.jpg', "rb") as f:
    #    b64code = base64.b64encode(f.read())
    #b64str = bytes.decode(b64code)
    #ret = client.FI_add_face_database("100", "张秋",'group02', b64str)
    #print(ret)
    #with open('known/lijunbao.jpg', "rb") as f:
#	b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("008", "李军宝",'group02', b64str)
    # with open("known/face04.jpg", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("009", "丁兆柱",'group02', b64str)
    # with open("known/zhangxueyou.jpg", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("012", "张学友",'group02', b64str)
    # with open("known/liuyifei.jpg", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # client.FI_add_face_database("013", "刘亦菲",'group02', b64str)
    #with open("4444.jpeg", "rb") as f:
    #      b64code = base64.b64encode(f.read())
    #b64str = bytes.decode(b64code)
    #result = client.FI_face_database_identify("group02", b64str)
    #print(result)

    # result = client.FI_find_group_users("group02")
    # print(result)
    #with open("111.JPG", "rb") as f:
    #     b64code = base64.b64encode(f.read())
    # b64str = bytes.decode(b64code)
    # result = client.FI_face_detect(b64str)
    # print(result)
    # result = client.FI_del_face_database("009","group02")
    # result = client.FI_del_face_database("099", "group02")
    # result = client.FI_del_face_database("003", "group02")
    # result = client.FI_del_face_database("006", "group02")
    #####object tracking test######################
    import os

    start = 1
    video_folder = os.path.join("video_frames")
    for k, name in enumerate(sorted(glob.glob(os.path.join(video_folder, "*.jpg")))):
        print("filename:", name)
        with open(name, "rb") as f:
            b64code = base64.b64encode(f.read())
        b64str = bytes.decode(b64code)
        rect = rectangle()
        rect.left, rect.top, rect.right, rect.bottom = 74, 67, 112, 153
        if start == 1:
            client.FI_object_tracking(b64str, rect, start)
            start = 0
        else:
            pos = client.FI_object_tracking(b64str, rect, start)
            print(pos)

    # Close!
    transport.close()

except Thrift.TException as tx:
    print('%s' % (tx.message))
