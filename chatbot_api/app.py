from flask import Flask , request, jsonify, abort

import socket
import json

#챗봇 엔진 서버 정보
host = "127.0.0.1"
port = 5050

#Falsk 애플리케이션
app = Flask(__name__)

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host,port))

    # 챗봇 엔진 질의 요청
    json_data = {

    }