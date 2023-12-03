from konlpy.tag import Komoran
import pickle
import jpype

#챗봇에서 전처리를 담당하
#전처리과정
#
class Preprocess:
    def __init__(self, word2index_dic='', userdic=None):
        # 단어 인덱스 사전 불러오기
        if(word2index_dic != ''):
            f = open(word2index_dic, "rb")
            self.word_index = pickle.load(f)
            f.close()
        else:
            self.word_index = None

        # 형태소 분석기 초기화
        # 1. Preprocess클래스가 생성될때 형태소 분석기 인스턴스 객체를 생성한다.
        # 2. 분석기는 코모란을 사용
        # 3. userdic 인자에는 사용자 정의 사전 파일의 경로를 입력할 수 있다.
        self.komoran = Komoran(userdic=userdic)

        # 관계언 제거, 기호 제거
        # 어미 제거
        # 접미사 제거
        # 형태소 분석기 인스턴스 객체 생성 잉후 어떤 품사를 불용어로 정의할지 클래스 멤버변수 리스트에 정의
        # 즉 해당 리스트에 정의 된 품사들은 불용어로 정의되어 핵심 키워드에서 제외됩니다.
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]

    # 형태소 분석기 POS 태거
    # 코모란 형태소 분석기의 POS 태거를 호출하는 메서드
    # Preprocess 클래스 외부에서는 코모란 형태소 분석기 객체를 직접적으로 호출할 일이 없게 하기 위해 정의한 래퍼 함수
    # 형태소 분석기 종류를 바꾸게 될 경우 이 래퍼 함수 내용만 변경하면 되므로 유지보수 측면에서 장점이 많다.
    def pos(self, sentence):
        jpype.attachThreadToJVM()# JPype를 사용하여 현재 스레드를 자바 가상 머신에 연결하는 부분으로, KoNLPy의 Komoran 분석기를 사용하기 위해 필요한 초기화 과정 중 하나
        return self.komoran.pos(sentence)

    # 불용어 제거 후, 필요한 품사 정보만 가져오기
    #생성자에서 정의한
    def get_keywords(self, pos, without_tag=False):
        f = lambda x: x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list

    # 키워드를 단어 인덱스 시퀀스로 변환
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []

        w2i = []
        for word in keywords:
            try:
                w2i.append(self.word_index[word])
            except KeyError:
                # 해당 단어가 사전에 없는 경우, OOV 처리
                w2i.append(self.word_index['OOV'])
        return w2i

