from konlpy.tag import Komoran
import pickle


class Preprocess:
    def __init__(self, word2index_dic='', userdic=None):
        # 단어 인덱스사전 불러오기
        if (word2index_dic != ''):
            f = open(word2index_dic, "rb")
            self.word_index = pickle.load(f)
            f.close()
        else:
            self.word_index = None

        # 형태소 분석기 초기화
        #Preprocess 클래스가 생성될때  형태소 인스턴스를 생성
        # userdic 인자에는 사용자 정의 사전 파일의 경로를 입력할 수 있음
        self.komoran = Komoran(userdic=userdic)

        # 제외할 품사
        # 어떤 품사를 불용어로 정의할지 클래스 맴버 변수에 정의
        # 해당 리스트에 정의된 품사들은 불용어로 정의 되어 핵심 키워드에서 제외된다.
        # 관계언 제거, 기호 제거, 어미 제거, 접미사 제거
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]

    # 코모란 형태소 분석기의 POS 태거를 호출하는 메서드
    # Preprocess 클래스 외부에서는 코모란 형태소를
    # 직접적으로 호출할 일 없게 하기 위해 정의한 래퍼 함수
    def pos(self, sentence):
        return self.komoran.pos(sentence)

    # 불용어 제거후 필요한 품사 정보만 가져오기
    # 생성자에서 정의한 self.exclusion_tags에 해당하지 않는 품사 정보만 키워드로 저장
    def get_keywords(self, pos, without_tag=False):
        f = lambda x: x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list

    # 키워드를 단어 인덱스 시퀸스로 변환
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        w2i = []
        for word in keywords:
            try:
                w2i.append(self.word_index[word])
            except KeyError:
                # 해당 단어가 사전에 없는 경우 OOV 처리
                w2i.append(self.word_index['OOV'])
        return w2i