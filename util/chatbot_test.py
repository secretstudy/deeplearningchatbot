from config.DatabaseConfig import *
from util.Database import Database
from util.Preprocess import Preprocess
from model.intent.IntentModel import IntentModel

# 전처리 객체 생성
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin', userdic='../util/user_dic.tsv')

# 질문/답변 ㅎ학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST,user=DB_USER,password=DB_PASSWORD,db_name=DB_NAME
)
db.connect() # DB 연결

# 질문
query = "오전에 탕수육 10개 주문합니다."

#의도 파악
intent = IntentModel(model_name='../model/ner/ner_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

#개체명 인식