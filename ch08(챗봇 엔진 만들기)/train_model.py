import pandas as pd
import tensorflow as tf

#라이브러리 import
from tensorflow import keras
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding , Dense, Dropout,Conv1D,GlobalMaxPool1D, concatenate

#모듈 import
from GlobalParams import GlobalParams,MAX_SEQ_LEN
from Preprocess import Preprocess

# 데이터 읽어오기 
# csv파일을 읽어와 CNN 모델 학습을 위한 데이터를 리스트에 저장한다.
#csv에 있는 query와intent 컬럼 데이트를 리스트에 저장한다
train_file = "./total_train_data.csv"
data = pd.read_csv(train_file, delimiter=',')
queries = data['query'].tolist()
intents = data['intent'].tolist()

p = Preprocess(word2index_dic="./chatbot_dict.bin", userdic='./user_dic.tsv')


# 단어 시퀀스 생성
# 모듈 Preprocess로 단어 시퀀스를 생성하고 
#해당 단어에 매칭되는 번호로 시퀀스 생성
sequences = []
for sentence in queries:
    pos = p.pos(sentence)
    keywords = p.get_keywords(pos, without_tag=True)
    seq = p.get_wordidx_sequence(keywords)
    sequences.append(seq)

# 단어 시퀀스 벡터 생성 
# 생성한 단어 시퀀스 벡터의 크기를 동일하게 맞추기 위해 패딩 처리
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen = MAX_SEQ_LEN ,padding='post')

# 학습용, 검증용, 테스트용 데이터셋 생성 
# 패딩 처리된 시퀀스 리스트 전체를 데이터셋 객체로 만든다
# 학습셋:검증셋:테스트셋 = 7:2:1
ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
ds = ds.shuffle(len(queries))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

#하이퍼파라미터 설정
dropout_prob = 0.5
EMB_SIZE = 128
EPOCH = 5
VOCAB_SIZE = len(p.word_index) + 1 #전체 단어수

# CNN 모델 정의 
input_layer = Input(shape=(MAX_SEQ_LEN,))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

conv1 = Conv1D(filters=128, kernel_size=3, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPool1D()(conv1)
conv2 = Conv1D(filters=128, kernel_size=4, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPool1D()(conv2)
conv3 = Conv1D(filters=128, kernel_size=5, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool3 = GlobalMaxPool1D()(conv3)


# 3,4,5-gram 이후 합치기
concat = concatenate([pool1,pool2,pool3])

hidden = Dense(128, activation=tf.nn.relu)(concat)
dropout_hidden = Dropout(rate=dropout_prob)(hidden)
logits = Dense(3, name='logits')(dropout_hidden)
predictions = Dense(128, activation=tf.nn.relu)(logits)

# 모델 생성 5

model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer='adam',
             loss='sparse_categorical_crossentropy',
             metrics=['accuracy'])

# 모델 학습 6

model.fit(train_ds, validation_data = val_ds, epochs=EPOCH, verbose = 1)

# 모델 평가(테스트 데이터셋 이용) 
# evaluate 함수를 사용해 성능을 평가
loss, accuracy = model.evaluate(test_ds, verbose=1)
print('Accuracy: %f' % (accuracy * 100))
print('loss : %f' % (loss))

# 모델 저장 8
model.save('intent_model.h5')
