from Preprocess import Preprocess

#sent = "내일 오전 10시에 짬뽕 주문하고 싶어ㅋㅋ"
#sent = "원격지원  어떻게 해요?"
sent = "설치를 하고 싶은데 원격가능 할까요?"

# 전처리 객체 생성 
p = Preprocess(userdic='../ch08(챗봇엔진 만들기)user_dic.tsv')

# 형태소 분석기 실행
pos = p.pos(sent)



# 품사 태그와 같이 키워드 출력
ret = p.get_keywords(pos, without_tag=False)
print(ret)

# 품사 태그와 없이 키워드 출력
ret = p.get_keywords(pos, without_tag=True)
print(ret)