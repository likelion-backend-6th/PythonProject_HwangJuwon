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
    print('5. 도서 정보 입력')
    print('6. 종료')
    print('------------------------------------------------------------')


def book_search():
    os.system('cls')
    print('------------------------------------------------------------')
    print('                      도서 정보 조회 메뉴')
    print('------------------------------------------------------------')
    find = input('검색할 책의 제목 혹은 ID를 입력해주세요 : ')
    try:  # 입력한 값이 int로 변환될 수 있다면(id를 입력했다면) id로 검색, 변환될 수 없다면(책 제목을 입력했다면) 제목으로 검색
        int(find)
        DB.cur.execute(f"SELECT * FROM Books WHERE id='{find}';")
    except ValueError:
        DB.cur.execute(f"SELECT * FROM Books WHERE title='{find}';")
    print('ID | 책 제목 | 저자 | 출판사 | 대출 가능 여부')
    rows = DB.cur.fetchall()
    for row in rows:
        # row는 튜플 형태로 id, 책제목, 저자, 출판사, 대출 가능여부 순서로 값을 저장함
        print(row[0], '|', row[1], '|', row[2], '|', row[3], '|', row[4])
    repeat = input('계속 검색하시겠습니까? (y/n) : ')
    if repeat == 'y':
        book_search()
    elif repeat == 'n':
        main()
    else:
        print('잘못된 값이 입력되었습니다. 메인메뉴로 돌아갑니다.')
        main()


def book_loan():
    os.system('cls')
    print('------------------------------------------------------------')
    print('                      도서 대출 메뉴')
    print('------------------------------------------------------------')
    find = input('대여할 책의 제목 혹은 ID를 입력해주세요 : ')
    try:
        int(find)
        DB.cur.execute(f"SELECT loanable FROM books WHERE id = {find}")
        loan = DB.cur.fetchone()
        if loan[0]:  # fetch는 튜플 형식으로 값을 가져오기 때문에 0번 인덱스를 불러와야 True 혹은 False가 출력됨
            DB.cur.execute(f"INSERT INTO loans (book_id, loan_date) VALUES ({find}, cast(now() as date));"
                           f"UPDATE books SET loanable = FALSE WHERE id = {find};")
            DB.conn.commit()
            print(f"{find}번 책을 대출했습니다.")
        else:
            print('이미 대출중인 책입니다.')
    except ValueError:
        DB.cur.execute(f"SELECT loanable, id FROM books WHERE title = '{find}';")
        loan = DB.cur.fetchone()
        if loan[0]:
            book_id = loan[1]
            DB.cur.execute(f"INSERT INTO loans (book_id, loan_date) VALUES ({book_id}, cast(now() as date));"
                           f"UPDATE books SET loanable = FALSE WHERE id = {book_id};")
            DB.conn.commit()
            print(f"{find} 책을 대출했습니다.")
        else:
            print('이미 대출중인 책입니다.')
    repeat = input('계속 대출하시겠습니까? (y/n) : ')
    if repeat == 'y':
        book_loan()
    elif repeat == 'n':
        main()
    else:
        print('잘못된 값이 입력되었습니다. 메인메뉴로 돌아갑니다.')
        main()

def book_return():
    os.system('cls')
    print('------------------------------------------------------------')
    print('                      도서 반납 메뉴')
    print('------------------------------------------------------------')
    find = input('반납할 책의 제목 혹은 ID를 입력해주세요 : ')
    try:
        int(find)
        DB.cur.execute(f"SELECT b.loanable, l.loan_id FROM books b, loans l WHERE b.id=l.book_id AND id = {find};")
        loan = DB.cur.fetchone()
        if not loan[0]:
            loan_id = loan[1]
            DB.cur.execute(f"UPDATE books SET loanable = TRUE WHERE id = {find};"
                           f"UPDATE loans SET return_date = cast(now() as date) WHERE loan_id = {loan_id};")
            DB.conn.commit()
            print(f"{find}번 책을 반납했습니다.")
        else:
            print('대출중인 책이 아닙니다.')
    except ValueError:
        DB.cur.execute(f"SELECT b.loanable, b.id, l.loan_id FROM books b, loans l WHERE b.id=l.book_id AND title = '{find}';")
        loan = DB.cur.fetchone()
        if not loan[0]:
            book_id = loan[1]
            loan_id = loan[2]
            DB.cur.execute(f"UPDATE books SET loanable = TRUE WHERE id = {book_id};"
                           f"UPDATE loans SET return_date = cast(now() as date) WHERE loan_id = {loan_id};")
            DB.conn.commit()
            print(f"{find} 책을 반납했습니다.")
        else:
            print('대출중인 책이 아닙니다.')

def loan_search():
    # select l.loan_id, l.book_id, b.title, l.loan_date from loans l, books b where l.book_id=b.id;
    pass

def book_insert():
    os.system('cls')
    print('------------------------------------------------------------')
    print('                      도서 정보 입력 메뉴')
    print('------------------------------------------------------------')
    title = input('추가할 도서 제목 : ')
    author = input('추가할 도서 저자 : ')
    pub = input('추가할 도서 출판사 : ')
    DB.cur.execute(f"INSERT INTO Books (title, author, publisher) VALUES ('{title}', '{author}', '{pub}');")
    DB.conn.commit()
    repeat = input('계속 입력하시겠습니까? (y/n) : ')
    if repeat == 'y':
        book_insert()
    elif repeat == 'n':
        main()
    else:
        print('잘못된 값이 입력되었습니다. 메인메뉴로 돌아갑니다.')
        main()


def main():
    print_mainmemu()
    print('-> 메뉴 번호 선택 : ', end='')
    user_select = int(input())
    print('------------------------------------------------------------')

    if user_select == 1:  # 도서 정보 조회
        book_search()
    elif user_select == 2:  # 도서 대출
        book_loan()
    elif user_select == 3:  # 도서 반납
        book_return()
    elif user_select == 4:  # 대출 정보 조회
        loan_search()
    elif user_select == 5:  # 도서 정보 입력
        book_insert()
    elif user_select == 6:
        DB.conn.close()
        DB.cur.close()
        print('프로그램을 종료합니다.')
    else:
        print('올바른 값을 입력해주세요.')
        main()


main()
