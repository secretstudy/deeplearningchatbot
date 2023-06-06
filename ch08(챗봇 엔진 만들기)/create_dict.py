from Preprocess import *
from tensorflow.keras import preprocessing
import pickle

# 말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:] # 헤더 제거
    return data

#말뭉치 데이터 가져오기 
#read_corpus_data함수는 파일을 읽어와 리스트로 반환합니다.
corpus_data = read_corpus_data('./corpus.txt')

#말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성 
#데이터 리스트에서 문장을 한개씩 가져와 POS 태깅한다.
p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c[1])
    for k in pos:
        dict.append(k[0])
        
        
#사전에 사용될 word2index 생성
# 사전의 첫 번째 인덱스에는 OOOV 사용
#토크나이저를 이용해 단어 리스트(dict)를 단어 인덱스 딕셔너리 테이터로 만든다.
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index

#사전 파일 생성 
#생성된 단어 인덱스 딕셔너리 객체를 파일로 저장한다.

f = open("chatbot_dict.bin","wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()
    print("파일 종료")
