import os
from dbManager import DB


def print_mainmemu():
    print('------------------------------------------------------------')
    print('                  도서관 관리 시스템 메인 메뉴')
    print('------------------------------------------------------------')
    print('1. 도서 정보 조회')
    print('2. 도서 대출')
    print('3. 도서 반납')
    print('4. 대출 정보 조회')
    print('5. 종료')
    print('------------------------------------------------------------')


def main():
    print_mainmemu()
    print('-> 메뉴 번호 선택 : ', end='')
    user_select = int(input())
    print('------------------------------------------------------------')

    if user_select == 1: # 도서 정보 조회
        os.system('cls')
        print('------------------------------------------------------------')
        print('                      도서 정보 조회 메뉴')
        print('------------------------------------------------------------')
        DB.cur.execute("SELECT * FROM Books;")
        rows = DB.cur.fetchall()
        for row in rows:
            # row는 튜플 형태로 id, 책제목, 저자, 출판사 순서로 값을 저장함
            print(row[0], '|', row[1], '|', row[2], '|', row[3])
        main()
    elif user_select == 2:
        pass
    elif user_select == 3:
        pass
    elif user_select == 4:
        pass
    elif user_select == 5:
        print('프로그램을 종료합니다.')
    else:
        print('올바른 값을 입력해주세요.')
        main()


main()
