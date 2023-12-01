import socket
import json
import pymysql
from config.DatabaseConfig import *
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# MySQL 연결 설정
mydb = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

@app.route('/')
def index():
    return render_template('chat_test_chatgpt.html')  # HTML 페이지 렌더링

@app.route('/chat_service/', methods=['POST'])
def chat_service():
    query = request.form['input1']  # 클라이언트로부터 입력 받기

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    json_data = {
        'Query': query,
        'BotType': "chat_service",
    }

    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()

    # 예시로 간단하게 입력 받은 내용을 그대로 답변으로 반환하는 코드

    response = json.loads(data)
    #response = {'response': response['Answer']}
    print("답변 : ")
    print(response)
    #print(type(response))
    return jsonify(response)  # JSON 형태로 응답 반환
if __name__ == '__main__':
    app.run(debug=True)  # 서버 실행
