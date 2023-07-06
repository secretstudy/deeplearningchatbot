import pymysql

db = None
try:
    # DB호스트 정보에 맞게 입력해주세요
    print("DB 연결 전")
    db = pymysql.connect(
        host='localhost',
        user='root',
        passwd='root',
        db='chatbot',
        charset='utf8',
    )
    print("DB 연결 성공!!")

    # 테이블 생성 sql 쿼리
    sql = ''' 
           CREATE TABLE tb_student(
               id int primary key auto_increment not null,
               name varchar(32),
               age int,
               address varchar(32)
           )'''

    #테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)
finally:
    if db is not None:
        db.close()
        print("DB 연결 종료")