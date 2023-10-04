from flask import Flask, request

app = Flask(__name__)

# 카카오톡 텍스트형 응답
@app.route('/app/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json() # 봇 시스템 요청 body (SkillPayLoad)
    print(body)

    responseBody = {
        "version" : "2.0",
        "template": {
            "outputs" : [
                {
                    "simpleText" : {
                        "text" : "안녕 hello I'm 명탐정"
                    }
                }
            ]
        }
    }
    return responseBody

# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods = [ 'POST'])
def showHello():
    body = request.get_json() # 봇 시스템 요청 body(SkillPayload)
    print(body)

    responseBody = {
        "version" : "2.0",
        "template" : {
            "outputs" : [
                {
                    "simpleImage" : {
                        "imageUrl" : "https://ih1.redbubble.net/image.5110525840.4370/raf,360x360,075,t,fafafa:ca443f4786.jpg",
                        "altText" : "hello I'm haibara"
                    }
                }
            ]
        }
    }

    return responseBody

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)