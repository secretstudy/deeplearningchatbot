import socket
#p.276
class BotServer:
    def __init__(self, srv_port, listen_num):#포트번호(srv_port)와 동시에 연결을 수락할 클라이언트 수(listen_num)를 멤버 변수로 저장합니다.
        self.port = srv_port#포트번호
        self.listen = listen_num#동시에 연결할 클라이언트 수
        self.mySock = None

    #sock 생성
    def create_sock(self):#소캣을 생성하는 메서드
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0", int(self.port)))  # 포트 지정
        self.mySock.listen(int(self.listen))#지정한 연결 수 만큼 클라 연결을 수락
        return self.mySock
    
    # client 대기
    def ready_for_client(self):#챗봇 클라이언트 연결을 대기하고 있다가 연결을 수락하는 메서드
        return self.mySock.accept()
        #반환값 conn : 연결된 챗봇 클라이언트와 데이터를 송수신할 수 있는 클라이언트 소켓
        #반환값 address : 연결된 챗봇 클라이언트 소켓의 바인드된 주소


    # sock 반환
    def get_sock(self):#현재 생성된 서버 소켓을 반환합니다.
        return self.mySock