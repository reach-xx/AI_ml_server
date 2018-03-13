import sqlite3
"""创建face数据库"""
conn = sqlite3.connect("database/faces.db")
c = conn.cursor()
c.execute("CREATE TABLE FACE_TB (UID VARCHAR(64) PRIMARY KEY, \
            GROUP_ID  VARCHAR(20)      NOT NULL ,    \
            USERINFO  TEXT,               \
            IMGNAME   CHAR(256),                \
            array IMGENCODE NOT NULL)")
conn.commit()
conn.close()
