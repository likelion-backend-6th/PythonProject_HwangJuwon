# PythonProject_HwangJuwon

## 1. 미션 요구사항 분석 & 체크리스트

---

### 1-1. 미션 요구사항 분석

---

```python
CLI 기반 메뉴
1. 파이썬 콘솔로 표현하는 메뉴 인터페이스
2. 번호를 입력받으면 그에 해당하는 기능을 수행
3. 기능을 수행하면 다시 메뉴로 돌아옴
4. 기능을 선택해서 들어가면 콘솔창이 삭제되어 선택한 메뉴만 출력함

데이터 입력 기능
1. 콘솔 조작으로 도서 정보 DB에 저장
2. csv, xml, json 등의 파일로 도서의 정보를 입력 가능

도서 정보 조회 기능
1. 콘솔 조작으로 도서 정보 조회 (id 또는 이름 입력)
2. 도서 정보는 도서 ID, 이름, 저자, 출판사, 대출 가능 여부 포함
3. 도서가 대출중인 경우 도서의 대출 정보 함께 출력 

도서 대출 기능
1. 콘솔 조작으로 도서 대출 (id 또는 이름 입력)
2. 대출중인 도서일 경우 대출이 불가능하다고 출력

도서 반납 기능
1. 콘솔 조작으로 반납을 원하는 도서 반납

대출 정보 조회 기능
1. 대출중인 도서 모두 출력하는 기능
2. 대출 정보는 도서 ID, 이름, 저자, 출판사, 대출 날짜, 반납일자로 구성
3. 대출 정보는 대출 날짜를 기준으로 내림차순으로

종료 기능
1. 프로그램 종료 기능
```

### 1-2. 미션 체크리스트

---

```python
DB 테이블 구성
도서 정보 테이블, 대출 정보 테이블 만들기[o]

CLI 기반 메뉴
메뉴 인터페이스 작성 [o]
번호 입력으로 메뉴 수행 로직 [o]
기능 수행 후 메뉴로 돌아오기 [o]

데이터 입력 기능
콘솔로 도서 정보 DB에 저장 [o]
csv, xml, json 등의 파일로 도서의 정보를 입력 가능 []

도서 정보 조회 기능
콘솔 조작으로 도서 정보 조회 (id 또는 이름 입력) [o]
도서 정보는 도서 ID, 이름, 저자, 출판사, 대출 가능 여부 포함 [o]
도서가 대출중인 경우 도서의 대출 정보 함께 출력 []

도서 대출 기능
콘솔 조작으로 도서 대출 [o]
대출중인 도서일 경우 대출이 불가능하다고 출력 [o]

도서 반납 기능
콘솔 조작으로 반납을 원하는 도서 반납 []

대출 정보 조회 기능
대출중인 도서 모두 출력하는 기능 []
대출 정보는 도서 ID, 이름, 저자, 출판사, 대출 날짜, 반납일자로 구성 []
대출 정보는 대출 날짜를 기준으로 내림차순으로 []

종료 기능
프로그램 종료 기능 [o]
```

## 2. 미션 진행 & 회고

---

### 2-1. 미션 진행 내용 요약

---

```markdown
DB 테이블 작성
- 테이블의 값들 중 ID는 직접 주지 않고 자동으로 1씩 늘어나게, 대출 가능 여부는 책 생성시 기본적으로
  대출 가능한 상태로 만들고 싶었다.
  [여기](https://lovethefeel.tistory.com/57)
  위 글을 참고하여 테이블 작성 때 ID를 자동으로 1씩 증가하게, 그리고 직접 넣을수도 있게 만드는 방법
  을 알았다.
    library=# create table books (
    library(# id int generated by default as identity unique primary key,
    library(# title varchar(100) not null,
    library(# author varchar(50) not null,
    library(# publisher varchar(50) not null,
    library(# loanable boolean not null default TRUE);
  
- 대출 테이블  
    library=# create table loans (
    library(# loan_id int generated by default as identity unique primary key,
    library(# book_id int not null,
    library(# loan_date date not null,
    library(# return_date date,
    library(# constraint fk_book_id foreign key(book_id) references "books"(id));
  
CLI 기반 메뉴
- 일단 함수 형태로 메인메뉴 구성을 해 놓고 기능의 동작이 끝날때마다 메인메뉴 함수를 불러오는 방식
  으로 구성했다.
  
도서 조회 메뉴
- 도서 조회 쿼리를
      try: 
        int(find)
        DB.cur.execute(f"SELECT * FROM Books WHERE id='{find}';")
    except ValueError:
        DB.cur.execute(f"SELECT * FROM Books WHERE title='{find}';")
  이렇게 작성해 봤다. int로 바꿀 수 없는 형식이 입력되면 책 제목이 입력되었다고 판단하여 제목으로
  검색하는 방식인데 만약 책 제목이 숫자로만 되어있는 경우가 있다면 어떻게 해야할까..

도서 대출 메뉴
- loans 테이블에 빌린 날짜를 저장할 때 
  INSERT INTO loans (book_id, loan_date) VALUES (find, cast(now() as date));
  라는 쿼리를 사용했다. postgreSQL의 내장함수인 now()는 현재 시간을 출력하는데 이를 date 형식으로 
  변환하여 넣을 수 있다.
  
도서 반납 메뉴
- UPDATE를 두번 사용해서 입력받은 책의 대출 가능여부를 True로, 대출 정보에서 반환 일자를 추가하는 
  방식으로 구현했다.

대출 조회 메뉴
- select l.loan_id, l.book_id, b.title, l.loan_date from loans l, books b where 
  l.book_id=b.id and b.loanable=false;
  쿼리를 사용해서 대출 불가능한 책 중에서 책 정보를 가져오는 쿼리를 작성했다.
  
도서 입력 메뉴
-

```

### 2-2. 회고

---

```markdown
[작성 가이드] 
이 블럭에 있는 내용은 확인 후 지워주세요. 

*구현 과정에서 아쉬웠던 점 / 궁금했던 점을 정리합니다.*

(작성 TIP) 
추후 리팩토링 시, 어떤 부분을 추가적으로 진행하고 싶은지에 대해 구체적으로 작성해보시기 바랍니다. 
```