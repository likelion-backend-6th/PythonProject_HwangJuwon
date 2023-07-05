import os
from dbManager import DB

def print_mainmemu():
    print('------------------------------')
    print('   도서관 관리 시스템 메인 메뉴')
    print('------------------------------')
    print('1. 도서 정보 조회')
    print('2. 도서 대출')
    print('3. 도서 반납')
    print('4. 대출 정보 조회')
    print('5. 종료')
    print('------------------------------')


def main():
    print_mainmemu()
    print('-> 메뉴 번호 선택 : ', end='')
    user_select = int(input())
    print('------------------------------')

    if user_select == 1:
        DB.cur.execute("SELECT * FROM Books;")
        rows = DB.cur.fetchall()
        for row in rows:
            print(row)
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
