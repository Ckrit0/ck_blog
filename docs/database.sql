-- Spec: MariaDB

-- 테이블 생성
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