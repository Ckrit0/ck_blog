from flask import make_response
from dto import userDTO
from service import db
from service import store
from service import loger
import string
import random

'''
비밀번호 암호화 (복호화 불가. 암호화 된 비밀번호를 서로 비교해야 함.)
parameter: pw(String)
return: encPw(String)
'''
def encryptPw(pw):
    # 임의로 버려지고 추가되는 값들이 있어서 복호화는 불가능.
    encPw = ""
    key = store.secret_key
    # 비밀번호와 지정한 키를 한글자씩 꺼내고
    for i in range(len(pw)):
        # 비밀번호 unicode에 10을 더해주고
        pwCharNo = ord(pw[i]) + 10
        keyCharNo = ord(key[i % len(key)])
        # 지정한 키 unicode와 곱한 뒤, 10으로 나누고 나머지는 버린다
        saveCharNo = (pwCharNo * keyCharNo) // 10
        # 그 숫자를 문자열 방식으로 더한 뒤,
        encPw += str(saveCharNo)
    # 만들어진 문자가 40글자 미만이면
    while len(encPw) < 40:
        tempPw = ""
        # encPw로 만들어진 숫자와 조금 다르게 설정된 숫자의 문자를 합해준다.
        for i in range(len(encPw)):
            tempPw += encPw[i] + str((ord(pw[i]) * ord(key[i %len(key)]))//8)
    # 만들어진 문자가 100글자(DB가 VARCHAR(100))가 넘으면
    while len(encPw) > 100:
        tempPw = ""
        # 문자열의 index가 5의 배수인 문자를 버린다.
        for i in range(len(encPw)):
            if i % 5 != 0:
                tempPw += encPw[i]
        encPw = tempPw
    return encPw

'''
신규 유저 생성
parameter: user객체(userDTO)
return: 
'''
def setUser(user):
    # 동일이메일중 state가 활성화된 유저가 있으면 거부해야함
    # 패스워드 암호화 필요,(글자수 체크도)
    sql=f'INSERT INTO user(u_email,u_pw,u_state) VALUES("{user.getEmail()}","{user.getPw()}",{user.getState()})'
    result = db.setData(sql=sql)
    return result

'''
해당 유저의 세션 생성
parameter: user객체(userDTO)
return: 0 실패, 1 성공
'''
def __setSession(user):
    def getNewSessionKey():
        length = 50
        pool = string.ascii_letters + string.digits
        key = ""
        for i in range(length):
            key += random.choice(pool)
        return key
    sessionKey = getNewSessionKey()
    sql = f'INSERT INTO sessionlist(u_no,s_key,s_ip,s_expire)\
        VALUES({user.getNo()},"{sessionKey}","{user.getIp()}",NOW() + INTERVAL {store.sessionTime} HOUR)\
        ON DUPLICATE KEY\
            UPDATE s_key = VALUES(s_key),\
                s_ip = VALUES(s_ip),\
                s_expire = VALUES(s_expire);'
    result = db.setData(sql=sql)
    if result != 0:
        return sessionKey
    else:
        return False

'''
해당 유저 블랙리스트에 추가
parameter: user객체(userDTO)
return: 0은 실패, 1은 성공
'''
def setBlackList(user):
    sql = f'INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause) VALUES({user.getNo()},"{user.getIp()}",NOW() + INTERVAL {store.ddosBlockHour} HOUR,"{store.ddosBlackListCause}");'
    result = db.setData(sql=sql)
    if result == 0:
        return False
    else:
        log = loger.Loger()
        log.setLog(store.logName_blackList, f"{user.getEmail()}({user.getIp()}) {store.ddosBlackListCause}사유로 {store.ddosBlockHour}시간동안 BlackList에 추가됨")
        return True

'''
유저 정보 수정하기
parameter: user객체(userDTO)
return: 
'''
def updateUser(user):
    pass

'''
세션 만료일시를 갱신
parameter: user객체(userDTO)
return: 
'''
def updateSessionDate(user):
    pass

'''
이메일과 비밀번호로 세션키 받기(세션 등록)
parameter: email(String), pw(String)
return: sessionKey(string)
'''
def getSessionKeyByEmailAndPw(email,pw,ip):
    sql = f'SELECT * FROM user WHERE u_email="{email}" AND u_pw="{pw}" AND u_state IN (0,1,2,5)'
    result = db.getData(sql=sql)
    user = userDTO.UserDTO()
    user.setUser(result[0])
    user.setIp(ip=ip)
    sessionKey = __setSession(user=user)
    return sessionKey

'''
유저번호로 유저객체 받기
parameter: 유저번호(int), IP(String)
return: user객체(userDTO)
'''
def getUserByUserNo(uno, ip):
    user = userDTO.UserDTO()
    if uno != 0:
        sql = f'SELECT * FROM user WHERE u_no = {uno} AND u_state != 0'
        result = db.getData(sql=sql)
        if len(result) != 0:
            user.setUser(result[0])
    user.setIp(ip=ip)
    return user

'''
세션키를 이용하여 유저객체 받기
parameter: 세션키(String), IP(String)
return: user객체(userDTO)
'''
def getUserBySessionKey(cookieKey, ip):
    if cookieKey == "" or cookieKey == None:
        user = userDTO.UserDTO()
        user.setIp(ip)
        return user
    sql = f'SELECT u_no FROM sessionlist WHERE s_key = "{cookieKey}"'
    uno = db.getData(sql=sql)[0][0]
    user = getUserByUserNo(uno=uno, ip=ip)
    return user

'''
유저 번호로 세션 만료시간 받기
parameter: 유저번호(int)
return: user객체(userDTO)
'''
def getSessionTimeByUserNo(uno):
    sql = f'SELECT s_expire FROM sessionlist WHERE u_no = {uno}'
    s_expire = db.getData(sql=sql)[0][0]
    return s_expire

'''
유저 및 ip가 1분, 1시간 동안 접속한 횟수 받기
parameter: 유저객체(userDTO)
return: 리스트([1분user접속횟수,1시간user접속횟수,1분ip접속횟수,1시간ip접속횟수])
'''
def getViewCount(user):
    viewCountList = []
    if user.getNo() != 0:
        viewCountList.append(db.getData(f'SELECT count(*) FROM views WHERE u_no = {user.getNo()} AND v_date >= NOW() - INTERVAL 1 MINUTE')[0][0])
        viewCountList.append(db.getData(f'SELECT count(*) FROM views WHERE u_no = {user.getNo()} AND v_date >= NOW() - INTERVAL 1 HOUR')[0][0])
    else:
        viewCountList.append(0)
        viewCountList.append(0)
    viewCountList.append(db.getData(f'SELECT count(*) FROM views WHERE v_ip = "{user.getIp()}" AND v_date >= NOW() - INTERVAL 1 MINUTE')[0][0])
    viewCountList.append(db.getData(f'SELECT count(*) FROM views WHERE v_ip = "{user.getIp()}" AND v_date >= NOW() - INTERVAL 1 HOUR')[0][0])
    return viewCountList


'''
해당 user 최근에 읽은 글목록 가져오기
parameter: user객체(userDTO)
return: [글번호(int),글제목(String)]의 리스트
'''
def getLastViewList(user):
    pass

'''
유저별 최근에 읽은 글 목록 가져오기
parameter: 유저객체(userDTO)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_user(user):
    boardNoAndTitleList = []
    return boardNoAndTitleList

'''
블랙리스트 목록 받기
return: 블랙리스트(List)
'''
def getBlackList():
    blackList = []
    sql = 'SELECT u_no, bl_ip FROM blacklist WHERE bl_expire >= NOW()'
    result = db.getData(sql=sql)
    for black in result:
        for data in black:
            if data != 0:
                blackList.append(data)
    return blackList

'''
유저 삭제하기(u_status를 3으로 update)
parameter: user객체(userDTO)
return: 
'''
def deleteUser(user):
    pass