from dto import userDTO
from service import db
from service import store
from service import loger

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
parameter: user객체(userDTO), sessionKey(String)
return: 
'''
def setSession(user, session):
    pass

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
        log.setLog(f"{user.getEmail()}({user.getIp()}) {store.ddosBlackListCause}사유로 {store.ddosBlockHour}시간동안 BlackList에 추가됨")
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
이메일과 비밀번호로 유저객체 받기
parameter: email(String), pw(String)
return: user객체(userDTO)
'''
def getUserByEmailAndPw(email,pw):
    sql = f'SELECT * FROM user WHERE u_email="{email}" AND u_pw="{pw}" AND u_state IN (0,1,2,5)'
    result = db.getData(sql=sql)
    user = userDTO.UserDTO()
    user.setUser(result)
    return user

'''
유저번호로 유저객체 받기
parameter: 유저번호(int)
return: user객체(userDTO)
'''
def getUserByUserNo(uno):
    user = userDTO.UserDTO()
    sql = f'SELECT * FROM user WHERE u_no = {uno} AND u_state != 0'
    result = db.getData(sql=sql)
    if len(result[0]) != 0:
        user.setUser(result[0])
    return user

'''
세션키를 이용하여 유저객체 받기
parameter: 세션키(String)
return: user객체(userDTO)
'''
def getUserBySessionKey(sessionKey, ip):
    user = userDTO.UserDTO()
    # 유저객체 가져와서 세팅 필요
    user.setIp(ip)
    return user

'''
유저 번호로 세션키 받기
parameter: 유저번호(int)
return: 세션키(String)
'''
def getSessionKeyByUserNo(uno):
    sessionKey = None
    return sessionKey

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
            if data != None:
                blackList.append(data)
    return blackList

'''
유저 삭제하기(u_status를 3으로 update)
parameter: user객체(userDTO)
return: 
'''
def deleteUser(user):
    pass