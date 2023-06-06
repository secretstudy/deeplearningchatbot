from konlpy.tag import Komoran

class Preprocess:
    def __init__(self, userdic=None): # 생성자
        # 형태소 분석기 초기화 
        #gudxoth dlstmxjstmfmf todtjd 
        #userdic 인자에는 사용자 정의 사전 파일의 경로를 입력할 수 있음
        self.komoran = Komoran(userdic=userdic)
        
        #제외할 품사 
        #어떤 품사를 불용어로 정의할지 클래스 맴버 변수에 정의
        # 관계언 제거, 기호 제거, 어미 제거, 접미사 제거
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]
        
    # 형태소 분석기 pos 태거 
    # 클래스 외부에서는 형태소 분석기 객체를 직접 호출할수 없게 한다.
    
    def pos(self, sentemce):
        return self.komoran.pos(sentemce)
    
    # 불용어 제거후 필요한 품사 정보만 가져오기 
    # self.exclusion_tags에 해당하지 않는 품사 정보만 키워드로 저장
    def get_keywords(self, pos, without_tag=False):
        f = lambda x: x in self.exclusion_tags
        word_list = []
        for p in pos:            
            if f(p[1]) is False:                
                word_list.append(p if without_tag is False else p[0])
        return word_list