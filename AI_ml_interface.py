#!/usr/bin/python
#
# AI machine learn interface
# function :
#       1)face detectors
#       2)face recognition
#       3)objects detectors
#       4)objects tracking
#       5)object identify
#       and so on
import sqlite3
import json
import os
import sys

import face_identify
import object_detect
sys.path.append('gen-py')
from identify.ttypes import *

face_recognition = face_identify

# face detectors
# face recognition
class FaceServiceAPI:
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


    #Add face's information to database
    def add_face(self, uid, user_info,
                                    group_id, name):
        image = face_recognition.load_image_file(name)
        face_encoding = face_recognition.face_encodings(image)[0]
        conn = sqlite3.connect("database/faces.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO FACE_TB VALUES (?,?,?,?,?)",
                      (uid, group_id, user_info, name,
                       json.dumps(face_encoding.tolist()))
                      )
        except sqlite3.IntegrityError as IE:
            print("UID already existed!!!! ",  IE)
            conn.close()
            return 0
        conn.commit()
        conn.close()
        return 1

    def del_face(self, uid,  group_id):
        conn = sqlite3.connect("database/faces.db")
        c = conn.cursor()
        c.execute("DELETE from FACE_TB where UID='{0}';".format(uid))
        conn.commit()
        # cursors = c.execute("SELECT * FROM FACE_TB")
        conn.close()
        return 1

    def find_user_info(self, uid):
        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        cursors = cur.execute("SELECT * FROM FACE_TB where UID='{0}'".format(uid))
        for face in cursors:
            print("*******----------{0}------------".format(face[0]))
            print(face[4])
        conn.close()
        return 1

    def find_group_faces(self, group_id):
        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        cursors = cur.execute("SELECT * FROM FACE_TB where GROUP_ID='{0}'".format(group_id))
        params = db_users()
        users_dict = {}
        cnt = 0
        for face in cursors:
            u_info = user_info()
            u_info.uid, u_info.group, u_info.user_info = face[0], face[1], face[2]
            print("+++++++++++++++++++++++++++++++++++++++++")
            print("*******----------{0}------{1}------".format(u_info.uid, u_info.user_info))
            print("++++++++++++++++++++++++++++++++++++++++++")
            users_dict[cnt] = u_info
            cnt += 1
        conn.close()
        params.users_num = cnt
        params.user = users_dict
        return params

    def face_identify(self,  group_id, name):
        image = face_recognition.load_image_file(name)
        try:
            face_loc, face_encodings = self.mult_faces_recognition(image)
        except IndexError as IE:
            print("IndexError:  ",  IE)
            face_str = "[]"
            return face_str

        conn = sqlite3.connect("database/faces.db")
        cur = conn.cursor()
        faces_encode, faces_uid, faces_group, faces_info = [], [], [], []

        cursors = cur.execute("SELECT * FROM FACE_TB WHERE GROUP_ID='{0}'".format(group_id))
        for face in cursors:
            faces_uid.append(face[0])
            faces_group.append(face[1])
            faces_info.append(face[2])
            faces_encode.append(json.loads(face[4]))
        print("-----------------------------identify!!!!\n")
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
                f_info.uid, f_info.group, f_info.info = \
                            faces_uid[idx], faces_group[idx], faces_info[idx]
                face_rect = rectangle()
                face_rect.top,face_rect.right, face_rect.bottom, face_rect.left= \
                            location.top(),location.right(),location.bottom(),location.left()
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
        return params

    def faces_detect(self, name):
        image = face_recognition.load_image_file(name)
        face_locations = face_recognition.face_locations(image, model="hog")
        result = []
        d_info = face_detect_st()
        d_info.result_num = len(face_locations)
        if d_info.result_num == 0:
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
        return d_info


#objects detectors API
#objects tracking API
#object identify API
class ObjectServiceAPI:

    def object_tracking(self, image, rect, start):
        update_pos = rectangle()
        if start == 1:
            object_detect.start_object_track(image, rect)
            return rect
        else:
            pos = object_detect.update_object_track(image)
            print(pos)
        update_pos.left, update_pos.top, \
                        update_pos.right, update_pos.bottom = \
                                round(pos.left()), round(pos.top()), \
                                        round(pos.right()), round(pos.bottom())
        return update_pos



