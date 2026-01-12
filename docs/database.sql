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
    c_upper INT(10) NULL
);

CREATE TABLE board(
    b_no INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    u_no INT(10) NOT NULL,
    c_no INT(10) NOT NULL,
    b_date DATE NOT NULL DEFAULT NOW(),
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
    v_date DATE NOT NULL DEFAULT NOW()
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
    co_upper INT(10) NULL,
    co_isdelete INT(1) NOT NULL DEFAULT 0
);

CREATE TABLE blacklist(
    u_no INT(10) NOT NULL,
    bl_ip VARCHAR(15) NOT NULL,
    bl_date DATE NOT NULL DEFAULT NOW(),
    bl_expire  DATE NULL,
    bl_cause VARCHAR(1000) NULL
);

CREATE TABLE sessionlist(
    u_no INT(10) NOT NULL,
    s_key VARCHAR(100) NOT NULL,
    s_ip VARCHAR(15) NOT NULL,
    s_expire DATE NOT NULL
);

------------
-- SELECT --
------------
-- 최상위 카테고리 가져오기
SELECT * FROM category WHERE c_upper IS NULL
-- 하위 카테고리 가져오기
SELECT * FROM category WHERE c_upper=1
-- 전체 글 제목의 목록 가져오기(최신순, 페이지별)
SELECT b_title FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT 5 OFFSET 0
-- 전체 글 갯수 가져오기
SELECT count(*) FROM board WHERE b_isdelete=0
-- 마지막 게시글 가져오기
SELECT * FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT 1 OFFSET 0
-- 게시글 조회수 가져오기
SELECT count(DISTINCT v_ip) FROM views WHERE b_no=11
-- 게시글 좋아요수 가져오기
SELECT count(DISTINCT l_ip) FROM likes WHERE b_no=11

------------
-- INSERT --
------------

-- 유저
INSERT INTO user(u_email,u_pw,u_state) VALUES("email","pw","state")
-- 카테고리
INSERT INTO category(c_name,c_upper) VALUES("c_name","c_upper")
-- 글
INSERT INTO board(u_no,c_no,b_title,b_contents) VALUES("u_no","c_no","b_title","b_contents")
-- 조회 (u_no nullable로 변경해야함.)
INSERT INTO views(b_no,u_no,v_ip) VALUES("b_no","u_no","v_ip")
-- 좋아요 (is_like 토글방식으로 해야할지, insert delete 해야할지..)
INSERT INTO likes(b_no,u_no,l_ip,l_islike) VALUES("b_no","u_no","l_ip","l_islike")
-- 댓글
INSERT INTO comment(b_no,u_no,co_ip,co_comment,co_upper) VALUES("b_no","u_no","co_ip","co_comment","co_upper")
-- 블랙리스트 (u_no nullable로 변경해야함.)
INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause) VALUES("u_no","bl_ip","bl_expire","bl_cause")
-- 세션리스트 (u_no nullable로 변경해야함.)
INSERT INTO sessionlist(u_no,s_key,s_ip,s_expire) VALUES("u_no","s_key","s_ip","s_expire")

------------
-- UPDATE --
------------



------------
-- DELETE --
------------

