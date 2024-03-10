# 客戶端 ，用來呼叫service_Server.py
import socket
import struct
import timeit

def askForService(token, data):
    # HOST, PORT 記得修改
    HOST = "140.116.245.149"
    PORT = 2802
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    model = "Minnan"
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token + "@@@", "utf-8") + struct.pack("8s",bytes(model, encoding="utf8")) + b"P" + data
        msg = struct.pack(">I", len(msg)) + msg  # msglen
        sock.sendall(msg)
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()

    return received

def process(token, data):
    # 可在此做預處理
    # 送出
    result = askForService(token, data)
    # 可在此做後處理
    return result

if __name__ == "__main__":
    token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2NTQwODM1NDAsImlzcyI6IkpXVCIsInVzZXJfaWQiOiIyOTMiLCJzdWIiOiIiLCJhdWQiOiJ3bW1rcy5jc2llLmVkdS50dyIsImV4cCI6MTY2OTYzNTU0MCwic2NvcGVzIjoiMCIsImlhdCI6MTY1NDA4MzU0MCwiaWQiOjQzNiwidmVyIjowLjEsInNlcnZpY2VfaWQiOiIzIn0.bOezSZYxdVJmULUaVDgor-1atGraLBuc6d0h_lQoq_kLrFllsbZq5noQxdZ9W85mdXrUGFkyiBuu8LxU1_IOHrtmnTNobXdjBzzSoWFw6w5RNrNCy0xJ-wGI5nit1gcB512spzaxMQcvSQbJcT3TIiYxjWd0sNGoGRRKkPaoJbM"
    file_name = "output.wav"
    file = open(r"/Users/liushiwen/Desktop/NCKU_project/PROJECT/lecture2_api/{}".format(file_name), 'rb')
    data = file.read()
    total_time = 0
    count = 0.0
    print(process(token, data))
