import pymysql

db = None
try:
    # DB호스트 정보에 맞게 입력해주세요
    print("DB 연결 전")
    db = pymysql.connect(
        host='192.168.35.185',
        user='chatbot',
        passwd='chatbotstudy',
        db='chatbot',
        charset='utf8',
    )
    print("DB 연결 성공!!")

    #  sql 쿼리
    id = 1
    sql = ''' 
           UPDATE tb_student SET name="케이", age=36 where id=%d
           ''' %id

    #데이터 삽입
    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)
finally:
    if db is not None:
        db.close()
        print("DB 연결 종료")