import pickle
from util.Preprocess import Preprocess

f = open("../train_tools/dict/chatbot_dict.bin", "rb")
word_index = pickle.load(f)
f.close()

# sent = " 내일 오전 10시에 짬뽕 주문하고 싶어ㅋㅋ "
sent = " 원격지원  어떻게 해요? "
# sent = " 설치를 하고 싶은데 원격가능 할까요? "

# 전처리 객체 생성
p = Preprocess(userdic='../util/user_dic.tsv')

#형태소 분석기 실행
pos = p.pos(sent)

#품사 태그 없이 키워드 출력
keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        # 해당 단어가 사전에 없는 경우, OOV 처리
        print(word, word_index['OOV'])