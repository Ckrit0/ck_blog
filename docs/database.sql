-- Spec: MariaDB

----------------
-- 테이블 생성 --
----------------

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
    b_isdelete INT(1) NOT NULL DEFAULT 0
);

CREATE TABLE image(
    i_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    i_path VARCHAR(1000) NOT NULL
);

CREATE TABLE views(
    b_no INT(10) NOT NULL,
    u_no INT(10) NULL,
    v_ip VARCHAR(15) NOT NULL,
    v_date DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE likes(
    b_no INT(10) NOT NULL,
    u_no INT(10) NULL,
    l_ip VARCHAR(15) NOT NULL,
    l_date DATE NOT NULL DEFAULT NOW(),
    l_islike  INT(1) NOT NULL DEFAULT 0
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
    bl_cause VARCHAR(1000) NULL
);

CREATE TABLE sessionlist(
    u_no INT(10) PRIMARY KEY NOT NULL,
    s_key VARCHAR(100) NOT NULL,
    s_ip VARCHAR(15) NOT NULL,
    s_expire DATETIME NOT NULL
);

------------
-- SELECT --
------------
-- 상위 카테고리 가져오기
SELECT * FROM category WHERE c_upper IS NULL ORDER BY c_no;
-- 하위 카테고리 가져오기
SELECT * FROM category WHERE c_upper=1 ORDER BY c_no;
-- 전체 글 제목의 목록 가져오기(최신순, 페이지별)
SELECT b_title FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT 5 OFFSET 0;
-- 전체 글 갯수 가져오기
SELECT count(*) FROM board WHERE b_isdelete=0;
-- 유저별 마지막 읽은 글 제목의 목록 가져오기 (b_no가 0이면 게시글이 아닌 페이지라 제외)
SELECT b.b_no, b.b_title FROM board b
JOIN (SELECT DISTINCT b_no FROM views WHERE u_no = 0 AND b_no != 0 ORDER BY v_date DESC LIMIT 5) v
ON b.b_no = v.b_no;
-- IP별 마지막 읽은 글 제목의 목록 가져오기 (b_no가 0이면 게시글이 아닌 페이지라 제외)
SELECT b.b_no, b.b_title FROM board b
JOIN (SELECT DISTINCT b_no FROM views WHERE v_ip = "0.0.0.0" AND b_no != 0 ORDER BY v_date DESC LIMIT 5) v
ON b.b_no = v.b_no;
-- 마지막 게시글 가져오기
SELECT * FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT 1 OFFSET 0;
-- 게시글 조회수 가져오기
SELECT count(DISTINCT v_ip) FROM views WHERE b_no=11;
-- 게시글 좋아요수 가져오기
SELECT count(DISTINCT l_ip) FROM likes WHERE b_no=11;
-- 게시글의 상위 댓글 가져오기(오래된 순, 페이지별)
SELECT * FROM comment WHERE b_no=11 AND co_upper IS NULL ORDER BY co_no DESC LIMIT 5 OFFSET 0;
-- 게시글의 하위 댓글 가져오기(오래된 순, 페이지별)
SELECT * FROM comment WHERE b_no=11 AND co_upper = 1 ORDER BY co_no LIMIT 5 OFFSET 0;
-- 게시글의 댓글 페이지 가져오기(상위 댓글 기준)
SELECT count(*) FROM comment WHERE b_no = 11 AND co_upper IS NULL;
-- 유저 번호로 유저 정보 받기
SELECT * FROM user WHERE u_no = 0 AND u_state != 0; -- 0 미가입
-- 현재 적용중인 블랙리스트 가져오기
SELECT u_no,bl_ip FROM blacklist WHERE bl_expire >= NOW();
-- 1분동안 유저 view 횟수 가져오기
SELECT count(*) FROM views WHERE u_no = 1 AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1분동안 IP view 횟수 가져오기
SELECT count(*) FROM views WHERE v_ip = "0.0.0.0" AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1시간동안 유저 view 횟수 가져오기
SELECT count(*) FROM views WHERE u_no = 1 AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 1시간동간 IP view 횟수 가져오기
SELECT count(*) FROM views WHERE v_ip = "0.0.0.0" AND v_date >= NOW() - INTERVAL 1 MINUTE;
-- 쿠키에 저장된 세션키로 유저넘버 가져오기
SELECT u_no FROM sessionlist WHERE s_key = "laksfhdkl";
-- 유저번호로 세션 만료시간 가져오기
SELECT s_expire FROM sessionlist WHERE u_no = 1;
-- 이메일과 비밀번호로 유저정보 가져오기 (탈퇴한 회원 제외)
SELECT * FROM user WHERE u_email="u_email" AND u_pw="u_pw" AND u_state NOT IN (0, 3);
-- 이메일 주소로 유저번호와 유저상태 가져오기 - 탈퇴한 회원 제외
SELECT u_no, u_state, u_joindate FROM user WHERE u_email = "u_email" AND u_state NOT IN (0, 3);
-- 유저번호로 작성한 글 갯수 가져오기
SELECT count(*) FROM board WHERE u_no = 1 AND b_isdelete = 0;
-- 유저번호로 작성한 댓글 갯수 가져오기
SELECT count(*) FROM comment WHERE u_no = 1 AND co_isdelete = 0;
-- 유저번호로 작성한 최신글 목록 가져오기
SELECT * FROM board WHERE u_no = 1 AND b_isdelete = 0 ORDER BY b_no DESC LIMIT 5 OFFSET 0;
-- 유저번호로 작성한 최신댓글 목록 가져오기
SELECT * FROM comment WHERE u_no = 1 AND co_isdelete = 0 ORDER BY co_no DESC LIMIT 5 OFFSET 0;


------------
-- INSERT --
------------

-- 유저
INSERT INTO user(u_email,u_pw,u_state) VALUES("email","pw","state");
-- 카테고리
INSERT INTO category(c_name,c_upper) VALUES("c_name","c_upper");
-- 글
INSERT INTO board(u_no,c_no,b_title,b_contents) VALUES("u_no","c_no","b_title","b_contents");
-- 조회
INSERT INTO views(b_no,u_no,v_ip) VALUES("b_no","u_no","v_ip");
-- 좋아요
INSERT INTO likes(b_no,u_no,l_ip,l_islike) VALUES("b_no","u_no","l_ip","l_islike");
-- 댓글
INSERT INTO comment(b_no,u_no,co_ip,co_comment,co_upper) VALUES("b_no","u_no","co_ip","co_comment","co_upper");
-- 블랙리스트
INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause) VALUES("u_no","bl_ip","bl_expire","bl_cause");
-- 세션리스트
INSERT INTO sessionlist(u_no,s_key,s_ip,s_expire) VALUES("u_no","s_key","s_ip","s_expire") ON DUPLICATE KEY UPDATE s_key = VALUES(s_key), s_ip = VALUES(s_ip), s_expire = VALUES(s_expire);


------------
-- UPDATE --
------------
-- 유저의 탈퇴 처리(유저번호)
UPDATE FROM user SET u_state = 3 WHERE u_no = 1;
-- 유저의 탈퇴 처리(유저이메일)
UPDATE user SET u_state = 3 WHERE u_email = "u_email";
-- 세션 시간 초기화
UPDATE sessionlist SET s_expire = NOW() + INTERVAL 1 HOUR WHERE u_no = "u_no";
-- 유저 비밀번호 변경
UPDATE user SET u_pw = "u_pw" WHERE u_no = "u_no";
-- 유저 상태 변경
UPDATE user SET u_state = 2 WHERE u_no = "u_no";


------------
-- DELETE --
------------