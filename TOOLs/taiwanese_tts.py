# !/usr/bin/env python
# _*_coding:utf-8_*_

# 給任何使用這支程式的人：這支程式是新版台語台羅語音合成的API的client端。具體上會發送最下方變數data的台羅
# 給伺服器，並接收一個回傳的wav檔，output.wav
# 接受之台羅為教育部羅馬拼音，非教會羅馬拼音，請注意。
# 接受格式為UTF-8台羅，不是帶數字的。即請用類似"phái-sè"而非"phai2-se3"這種
# 不同port可以有不同格式，詳見下面的[注意]

# 客戶端 ，用來呼叫service_Server.py
import socket
import sys
import struct
# Don't touch


def askForService(token, data, model="M12_5"):
    # HOST, PORT 記得修改
    global HOST
    global PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = ""
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token+"@@@"+data+"@@@"+model, "utf-8")
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)

        with open('/Users/liushiwen/Desktop/NCKU_project/PROJECT/lecture2_api/output.wav', 'wb') as f:
            while True:
                # print("True, wait for 15sec")
                # time.sleep(15)

                l = sock.recv(8192)
                # print('Received')
                if not l:
                    break
                f.write(l)
        print("File received complete")
    finally:
        sock.close()
    return "OK"
# Don't touch


def process(token, data):
    # 可在此做預處理

    # 送出
    result = askForService(token, data)
    # 可在此做後處理
    return result


global HOST
global PORT
# 注意：以下數字，10008為原版，10010套用實驗室變調版，10012則是接受中文輸入，即多套一個中文轉台羅
# ***10008以及10010接受台羅，10012接受中文
HOST, PORT = "140.116.245.146", 10012
token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTEyOTMxMzMsImlhdCI6MTYzMzYxMzEzMywic3ViIjoiIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJpc3MiOiJKV1QiLCJ1c2VyX2lkIjoiMjkwIiwibmJmIjoxNjMzNjEzMTMzLCJ2ZXIiOjAuMSwic2VydmljZV9pZCI6IjI0IiwiaWQiOjM5Niwic2NvcGVzIjoiMCJ9.XtqCCNnmc6tiNIOvcCsY6_vX-IjQFreYQWeU3BqXAvhZYCnjRUZvkcQcRLo-FjUikviipwRRYZhBGXK2Pd2xK8gfNu7LKRGh9V3sPvHIHn4MxC-YzV0tjQItGyIDW2w708YJQffx3v4A7wxnj3sjkxDxHIS8LApRcgk7Cd3Rdig"
data = "I kú-kú tsiah lâi tsi̍t pái"
# data = "lîm--sian--sinn ê tsa-bóo-kiánn、 tíng-kò-gue̍h tsò--lâng āu--ji̍t 、tio̍h beh kè--lâng"
# data = "loo7-thau3-sia7 po3-to7 hian7-jim7 go5-lo5-su1 kok4-ka1 an1-tsuan5 hue7-gi7 Russian1 Security1 Council1 hu3 tsu2-sek8 e5 beh8-i5-tik4-hu1 kong2 ti7 ling7 lang5 gin7 kiong7-beh4 e7-sai2 kong2 si7 huat4-se1-su1 tsu2-gi7 e5 ki1-hu3 tsing3-khuan5"# 」 hoo7 lang5 thui1-huan1 、 oo1-khik4-lan5 uan5-tsuan5 hui1 kun1-su7-hoa3 tsing5 ， bok8-su1-kho1 tsiong1 ke3-siok8 ti7 oo1-kok4 huat4-tong7 tsian3-tsing1 。 phoo2-ting5 ti7 25ji̍t hian3-kng1 e5 hong2-bun7 ting3 kong2 ， go5-lo5-su1 i2-king1 tsun2-pi7-honn3 beh4 kap4 tsham1-tsian3 koh4 hng1 tsin3-hing5 tam5-phuann3 ， tan7-si7 ki1-hu3 kap4 ki5 se1-hong1 tsi1-tshi5 tsia2 ki7-tsuat8 tshap4 tai7-tsi3 tam5-phuann3 。 beh8-i5-tik4-hu1 si7 Go5-oo1 tsian3-tsing1 siong7 ing1-phai3 e5 tsi1-tshi5 tsia2 tsi1 tsit8 ， su3-siong5 khian2-tsik4 se1-hong1 ， tsi2-khong3 se1-hong1 khi3-too5 hun1-liat8 go5-lo5-su1 ，"
for i in range(1):
    print("Client : ", process(token, data))
