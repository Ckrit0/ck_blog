-- Spec: MariaDB

------------------------------------------------------------------------------------------------------------
----------------------------------------------- 테이블 생성 ------------------------------------------------
------------------------------------------------------------------------------------------------------------

CREATE TABLE user(
    u_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    u_email VARCHAR(30) NOT NULL,
    u_pw VARCHAR(100) NOT NULL,
    u_state INT(1) NOT NULL DEFAULT 0,
    u_lastdate DATE NOT NULL DEFAULT NOW(),
    u_joindate DATE NOT NULL DEFAULT NOW(),
    u_leavedate DATE NULL DEFAULT NULL
);

CREATE TABLE category(
    c_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    c_name VARCHAR(100) NOT NULL,
    c_upper INT(10) NULL,
    c_order INT(10) NOT NULL
);

CREATE TABLE board(
    b_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    u_no INT(10) NOT NULL,
    c_no INT(10) NOT NULL,
    b_date DATETIME NOT NULL DEFAULT NOW(),
    b_title VARCHAR(100) NOT NULL,
    b_contents MEDIUMTEXT NOT NULL,
    b_isdelete INT(1) NOT NULL DEFAULT 0,
    b_ip VARCHAR(15) NOT NULL
);

CREATE TABLE image(
    i_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    i_path VARCHAR(1000) NOT NULL
);

CREATE TABLE views(
    b_no INT(10) NOT NULL,
    u_no INT(10) NULL,
    v_ip VARCHAR(15) NOT NULL,
    v_date DATETIME NOT NULL DEFAULT NOW(),
    v_url VARCHAR(100) NULL
);

CREATE TABLE likes(
    b_no INT(10) NOT NULL,
    u_no INT(10) NULL,
    l_ip VARCHAR(15) NOT NULL,
    l_date DATE NOT NULL DEFAULT NOW()
);

CREATE TABLE comment(
    co_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    b_no INT(10) NOT NULL,
    u_no INT(10) NULL,
    co_ip VARCHAR(15) NOT NULL,
    co_comment VARCHAR(1000) NOT NULL,
    co_date DATETIME NOT NULL DEFAULT NOW(),
    co_upper INT(10) NULL,
    co_isdelete INT(1) NOT NULL DEFAULT 0
);

CREATE TABLE blacklist(
    u_no INT(10) NOT NULL,
    bl_ip VARCHAR(15) NOT NULL,
    bl_date DATETIME NOT NULL DEFAULT NOW(),
    bl_expire  DATETIME NULL,
    bl_cause INT(1) NOT NULL,
    bl_reason VARCHAR(100) NULL DEFAULT NULL
);

CREATE TABLE sessionlist(
    u_no INT(10) PRIMARY KEY NOT NULL,
    s_key VARCHAR(100) NOT NULL,
    s_ip VARCHAR(15) NOT NULL,
    s_expire DATETIME NOT NULL
);

------------------------------------------------------------------------------------------------------------
-------------------------------------------------- SELECT --------------------------------------------------
------------------------------------------------------------------------------------------------------------
---------------
-- User DAO  --
---------------
-- 이메일 주소로 유저번호와 유저상태 가져오기 - 탈퇴한 회원 제외
SELECT u_no, u_state, u_joindate FROM user WHERE u_email = "u_email" AND u_state NOT IN (0, 3);
-- 이메일과 비밀번호로 유저정보 가져오기 (탈퇴한 회원 제외)
SELECT * FROM user WHERE u_email="u_email" AND u_pw="u_pw" AND u_state NOT IN (0, 3);
-- 유저 번호로 유저 정보 받기
SELECT * FROM user WHERE u_no = 0 AND u_state != 0; -- 0 미가입
-- 쿠키에 저장된 세션키로 유저넘버 가져오기
SELECT u_no FROM sessionlist WHERE s_key = "laksfhdkl";
-- 쿠키에 저장된 세션키로 유저정보 가져오기 (탈퇴한 회원 제외)
SELECT * FROM user WHERE u_no = (SELECT u_no FROM sessionlist WHERE s_key = "laksfhdkl") AND u_state NOT IN (0, 3);
-- 유저번호로 세션 만료시간 가져오기
SELECT s_expire FROM sessionlist WHERE u_no = 1;
-- 1분동안 유저 view 횟수 가져오기
SELECT count(*) FROM views WHERE u_no = 1 AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1분동안 IP view 횟수 가져오기
SELECT count(*) FROM views WHERE v_ip = "0.0.0.0" AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1시간동안 유저 view 횟수 가져오기
SELECT count(*) FROM views WHERE u_no = 1 AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1시간동간 IP view 횟수 가져오기
SELECT count(*) FROM views WHERE v_ip = "0.0.0.0" AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 유저별 마지막 읽은 글 제목의 목록 가져오기 (b_no가 0이면 게시글이 아닌 페이지라 제외)
SELECT b.b_no, b.b_title FROM board b
JOIN (SELECT DISTINCT b_no FROM views WHERE u_no = 0 AND b_no != 0 ORDER BY v_date DESC LIMIT 5) v
ON b.b_no = v.b_no;
-- IP별 마지막 읽은 글 제목의 목록 가져오기 (b_no가 0이면 게시글이 아닌 페이지라 제외)
SELECT b.b_no, b.b_title FROM board b
JOIN (SELECT DISTINCT b_no FROM views WHERE v_ip = "0.0.0.0" AND b_no != 0 ORDER BY v_date DESC LIMIT 5) v
ON b.b_no = v.b_no;
-- 현재 적용중인 블랙리스트 가져오기
SELECT u_no FROM blacklist WHERE bl_expire >= NOW() AND u_no != 0
UNION ALL
SELECT bl_ip FROM blacklist WHERE bl_expire >= NOW() AND bl_ip != "";

-------------------
-- Category DAO  --
-------------------
-- 상위 카테고리 가져오기
SELECT * FROM category WHERE c_upper IS NULL ORDER BY c_no;
-- 하위 카테고리 가져오기
SELECT * FROM category WHERE c_upper=1 ORDER BY c_no;

----------------
-- Board DAO  --
----------------
-- 전체 글 제목의 목록 가져오기(최신순, 페이지별)
SELECT
    b.b_no, b.b_title,
    (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views v WHERE v.b_no=b.b_no),
    (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no)
FROM board b
WHERE b_isdelete=0
ORDER BY b_no DESC
LIMIT 5 OFFSET 0;
-- 전체 글 갯수 가져오기
SELECT count(*) FROM board WHERE b_isdelete=0;
-- 카테고리별 글 제목의 목록 가져오기(최신순, 페이지별)
SELECT
    b_no, b_title,
    (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no),
    (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no)
FROM board WHERE c_no="c_no" AND b_isdelete=0
ORDER BY b_no DESC LIMIT 5 OFFSET 0;
-- 카테고리별 글 갯수 가져오기
SELECT count(*) FROM board WHERE c_no=1 AND b_isdelete=0;
-- 카테고리별 글 제목의 목록에서 현재 글이 몇번째인지 가져오기
SELECT count(*) FROM board WHERE c_no=1 AND b_isdelete=0 AND b_no > 11;
-- 글번호로 글 가져오기
SELECT
	b.*, u.u_email, u.u_state,
	(SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no),
	(SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no)
FROM board b
JOIN user u
ON b.u_no = u.u_no 
WHERE b.b_no = 11 AND b.b_isdelete=0;
-- 마지막 게시글 가져오기
SELECT
	b.*, u.u_email, u.u_state,
	(SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no),
	(SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no)
FROM board b
JOIN user u
ON b.u_no = u.u_no 
WHERE b.b_isdelete=0
ORDER BY b_no DESC LIMIT 1;
-- 유저번호로 작성한 글 갯수 가져오기
SELECT count(*) FROM board WHERE u_no = 1 AND b_isdelete = 0;
-- 유저번호로 작성한 최신글 목록 가져오기
SELECT b.*, u.u_email, u.u_state,
	(SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no),
	(SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no)
FROM board b
JOIN user u
ON b.u_no = u.u_no 
WHERE b.u_no = 1 AND b.b_isdelete = 0
ORDER BY b_no DESC LIMIT 5;





-- 검색어가 포함된 글 제목의 목록 가져오기(최신순, 페이지별)
SELECT b_title FROM board
WHERE
    b_isdelete=0 AND
    (b_title LIKE "%검색어%" OR b_contents LIKE "%검색어%")
ORDER BY b_no DESC LIMIT 5 OFFSET 0;
-- 검색어가 포함된 글 갯수 가져오기
SELECT count(*) FROM board WHERE b_isdelete=0 AND (b_title LIKE "%검색어%" OR b_contents LIKE "%검색어%");




------------------
-- Comment DAO  --
------------------
-- 게시글의 상위 댓글 가져오기(오래된 순, 유저 이메일, 유저 상태, 게시글 제목, 하위글 갯수 포함)
SELECT c.*, u.u_email, u.u_state, b.b_title, (SELECT count(*) FROM comment WHERE co_upper = c.co_no)
FROM comment c
JOIN user u ON c.u_no = u.u_no
JOIN board b ON c.b_no = b.b_no
WHERE c.b_no=11 AND c.co_upper IS NULL
ORDER BY c.co_no;
-- 게시글의 하위 댓글 가져오기(오래된 순, 유저 이메일, 유저 상태, 게시글 제목 포함)
SELECT c.*, u.u_email, u.u_state, b.b_title FROM comment c
JOIN user u ON c.u_no = u.u_no
JOIN board b ON c.b_no = b.b_no
WHERE c.b_no=11 AND c.co_upper = 1
ORDER BY c.co_no;
-- 유저번호로 작성한 댓글 갯수 가져오기
SELECT count(*) FROM comment WHERE u_no = 1 AND co_isdelete = 0;
-- 유저번호로 작성한 최신댓글 목록 가져오기
SELECT c.*, u.u_email, u.u_state, b.b_title FROM comment c
JOIN user u ON c.u_no = u.u_no
JOIN board b ON c.b_no = b.b_no
WHERE c.u_no = 1
ORDER BY c.co_no DESC LIMIT 5 OFFSET 0;
-- 댓글번호로 유저번호 가져오기
SELECT u_no FROM comment WHERE co_no = "co_no";

------------------------------------------------------------------------------------------------------------
-------------------------------------------------- INSERT --------------------------------------------------
------------------------------------------------------------------------------------------------------------
---------------
-- User DAO  --
---------------
-- 조회 설정
INSERT INTO views(b_no,u_no,v_ip,v_url) VALUES("b_no","u_no","v_ip","v_url");
-- 유저
INSERT INTO user(u_email,u_pw,u_state) VALUES("email","pw","state");
-- 블랙리스트
INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause,bl_reason) VALUES("u_no","bl_ip","bl_expire","bl_cause","bl_reason");
-- 세션리스트
INSERT INTO sessionlist(u_no,s_key,s_ip,s_expire) VALUES("u_no","s_key","s_ip","s_expire") ON DUPLICATE KEY UPDATE s_key = VALUES(s_key), s_ip = VALUES(s_ip), s_expire = VALUES(s_expire);

-------------------
-- Category DAO  --
-------------------
-- 카테고리
INSERT INTO category(c_name,c_upper) VALUES("c_name","c_upper");

----------------
-- Board DAO  --
----------------


-- 글
INSERT INTO board(u_no,c_no,b_title,b_contents,b_ip) VALUES("u_no","c_no","b_title","b_contents","b_ip");

-- 좋아요 (취소불가 노빠꾸임)
INSERT INTO likes (b_no, u_no, l_ip)
SELECT "b_no", "u_no", "l_ip" FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM likes WHERE b_no = "b_no" AND (u_no = "u_no" OR l_ip = "l_ip"));

-----------------
-- Comment DAO --
-----------------
-- 댓글 작성
INSERT INTO comment(b_no,u_no,co_ip,co_comment,co_upper) VALUES("b_no","u_no","co_ip","co_comment","co_upper");


------------------------------------------------------------------------------------------------------------
-------------------------------------------------- UPDATE --------------------------------------------------
------------------------------------------------------------------------------------------------------------
---------------
-- User DAO  --
---------------
-- 유저 번호로 유저의 탈퇴 처리
UPDATE user SET u_state = 3 WHERE u_no = 1;
-- 유저 이메일로 유저의 탈퇴 처리
UPDATE user SET u_state = 3 WHERE u_email = "u_email" AND u_state IN (1, 2, 5);
-- 유저 비밀번호 변경
UPDATE user SET u_pw = "u_pw" WHERE u_no = "u_no";
-- 유저 상태 변경
UPDATE user SET u_state = 2 WHERE u_no = "u_no";
-- 유저 탈퇴
UPDATE user SET u_state = 3 WHERE u_no = "u_no";
-- 세션 시간 초기화
UPDATE sessionlist SET s_expire = NOW() + INTERVAL 1 HOUR WHERE u_no = "u_no";

-------------------
-- Category DAO  --
-------------------
-- 카테고리 수정
UPDATE category SET c_name="c_name", c_upper=Null, c_order=1 WHERE c_no=0;

----------------
-- Board DAO  --
----------------
-- 글 수정하기
UPDATE board SET c_no={cno}, b_title="{bTitle}", b_contents="{bContents}" WHERE b_no={board.getNo()}
-- 글 카테고리 변경
UPDATE board SET c_no = "c_no" WHERE b_no = "b_no";
-- 글 삭제
UPDATE board SET b_isdelete = 1 WHERE b_no = "b_no";

-----------------
-- Comment DAO --
-----------------
-- 댓글번호로 댓글 삭제
UPDATE comment SET co_isdelete = 1 WHERE co_no = "co_no";

------------------------------------------------------------------------------------------------------------
-------------------------------------------------- DELETE --------------------------------------------------
------------------------------------------------------------------------------------------------------------
---------------
-- User DAO  --
---------------

-------------------
-- Category DAO  --
-------------------
-- 카테고리 삭제
DELETE FROM category WHERE c_no = "c_no";

----------------
-- Board DAO  --
----------------


-----------------
-- Comment DAO --
-----------------