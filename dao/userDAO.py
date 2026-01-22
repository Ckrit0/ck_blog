from flask import make_response
from dto import userDTO
from service import db, store, loger
import string, random, re, smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

'''
비밀번호 암호화 (복호화 불가. 암호화 된 비밀번호를 서로 비교해야 함.)
parameter: pw(String)
return: encPw(String)
'''
def __encryptPw(pw):
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
            tempPw += encPw[i] + str((ord(pw[i%len(pw)]) * ord(key[i%len(key)]))//8)
        encPw = tempPw
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
30분이 경과한 인증코드들 삭제
'''
def __updateVerifyList():
    expireIndexList = []
    for i in range(len(store.verifyList)):
        if store.verifyList[i]['expire']  + timedelta(minutes=30) < datetime.now():
            expireIndexList.append(i)
    for i in range(len(expireIndexList)):
        store.verifyList.pop(expireIndexList[i]-i)

'''
조회 설정하기.(글이 아닌 모든 부분은 b_no를 0으로 설정)
parameter: user객체(userDTO)
return: 실패 0, 성공 1 (int)
'''
def setView(user):
    sql=f'INSERT INTO views(b_no,u_no,v_ip) VALUES(0,{user.getNo()},"{user.getIp()}")'
    result = db.setData(sql=sql)
    return result

'''
메일주소로 가입된 이메일 여부와 인증여부 확인
parameter: email(String)
return: dataList([['유저번호'(int),'유저상태'(int),'가입일'(datetime)]....])
'''
def getUserDataByEmailAddress(email):
    sql = f'SELECT u_no, u_state, u_joindate FROM user WHERE u_email = "{email}" AND u_state NOT IN (0, 3)'
    userData = db.getData(sql=sql)
    return userData

'''
인증코드 확인
parameter: email(String), code(String)
return: store.verifyResultCode(int)
'''
def matchVerify(email,code):
    __updateVerifyList()
    for verifyDict in store.verifyList:
        if verifyDict['email'] == email:
            if verifyDict['code'] == code:
                if verifyDict['expire'] > datetime.now():
                    # 확인 성공시점에서 1시간 유지
                    verifyDict['expire'] = datetime.now() + timedelta(hours=store.sessionTime)
                    return store.USER_RESULT_CODE['인증 성공']
                else:
                    return store.USER_RESULT_CODE['시간 종료']
            else:
                return store.USER_RESULT_CODE['코드 불일치']
    return store.USER_RESULT_CODE['발급된 코드 없음']

'''
인증코드 메일 발송
parameter: email(String), verifyCode(String)
return: store.verifyResultCode(int)
'''
def sendMail(email):
    def __getCode():
        code = ''
        pool = string.ascii_letters + string.digits
        #8자리 무작위 코드 생성
        for i in range(8):
            code += random.choice(pool)
        return code
    def __setVerify(email,code):
        expireTime = datetime.now() + timedelta(minutes=store.verifyExpireTime)
        verifyDict = {
            'email': email,
            'code' : code,
            'expire' : expireTime
        }
        store.verifyList.append(verifyDict)
    __updateVerifyList()
    code = __getCode()
    message = MIMEMultipart()
    message["From"] = store.send_email_addr
    message["To"] = email
    message["Subject"] = store.send_email_title + f'"{code}"'
    text = f'인증 코드: {code}\n' + store.send_email_message
    message.attach(MIMEText(text, 'plain'))
    try:
        # SSL/TLS 연결 시작 (STARTTLS)
        server = smtplib.SMTP(host=store.send_eamil_smtp, port=store.send_email_port)
        server.starttls() # TLS 암호화 적용
        server.login(user=store.send_email_addr, password=store.send_email_key)
        server.sendmail(store.send_email_addr, email, message.as_string())
        __setVerify(email=email,code=code)
        return store.USER_RESULT_CODE['메일 발송 완료']
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
        return store.USER_RESULT_CODE['실패-unknown']
    finally:
        server.quit() # 서버 연결 종료
    

'''
신규 유저 생성
parameter: email(String), pw(String), confirm(String), verify(String)
return: store.join_result_code(int)
'''
def setUser(email, pw, confirm, verify):
    def __checkEmailAndPwRegex(email, pw):
        result = [False, False]
        # 이메일 패턴: (영어 숫자 ._%+_) @ (영어 숫자 .-) . (2자리 이상의 영어)
        emailPtn = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(emailPtn, email):
            result[0] = True
        # 비밀번호 패턴: 영문자, 숫자, 특수문자가 모두 들어간 8~16자리
        pwPtn = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
        if re.match(pwPtn, pw):
            result[1] = True
        return result
    
    def __alreadyUserCode(userState):
        if userState == store.USER_STATE_CODE['미인증']:
            return store.USER_RESULT_CODE['가입된 Email']
        elif userState == store.USER_STATE_CODE['인증']:
            return store.USER_RESULT_CODE['가입된 Email']
        elif userState == store.USER_STATE_CODE['블랙리스트']:
            return store.USER_RESULT_CODE['블랙리스트']
        elif userState == store.USER_STATE_CODE['관리자']:
            return store.USER_RESULT_CODE['가입된 Email']
    
    # password와 컨펌이 서로 맞지 않는 경우
    if pw != confirm:
        return store.USER_RESULT_CODE['Confirm 오류']
    
    # email 주소나 PW 형식이 틀린 경우
    checkRegex = __checkEmailAndPwRegex(email=email, pw=pw)
    if checkRegex[0] == False:
        return store.USER_RESULT_CODE['Email 형식 오류']
    elif checkRegex[1] == False:
        return store.USER_RESULT_CODE['Pw 형식 오류']
    
    # 이메일을 이미 사용중인 유저의 데이터
    userData = getUserDataByEmailAddress(email=email)
    
    user = userDTO.UserDTO()
    user.setEmail(email=email)
    user.setPw(pw=__encryptPw(pw=pw))
    sqlList = []
    
    # verify 미진행
    if verify == "" or verify == None:
        user.setState(state=store.USER_STATE_CODE['미인증'])
        # 미인증시 기존 생성된 이메일 주소의 강제 진행 불가
        if len(userData) != 0:
            return __alreadyUserCode(userData[0][1])
            
    # verify 진행
    else:
        verifyResult = matchVerify(email=email, code=verify)
        if verifyResult == 0:
            user.setState(state=store.USER_STATE_CODE['인증'])
            # 인증완료시 기존 생성된 이메일 주소의 탈퇴처리
            sql = f'UPDATE user SET u_state = 3 WHERE u_email = "{email}";'
            # 회원가입 처리가 정상적으로 처리되지 않을 때를 위해서 List방식으로 한번에 commit
            sqlList.append(sql)
        else:
            user.setState(state=store.USER_STATE_CODE['미인증'])
            # 미인증시 기존 생성된 이메일 주소의 강제 진행 불가
            if len(userData) != 0:
                return __alreadyUserCode(userData[0][1])

    sql=f'INSERT INTO user(u_email,u_pw,u_state) VALUES("{user.getPlaneEmail()}","{user.getPw()}",{user.getState()})'
    sqlList.append(sql)
    result = db.setDatas(sqlList=sqlList)
    if result != 0:
        return store.USER_RESULT_CODE['정상 가입']
    else :
        return store.USER_RESULT_CODE['실패-unknown']

'''
해당 유저 블랙리스트에 추가
parameter: user객체(userDTO)
return: 0은 실패, 1은 성공
'''
def setBlackList(user):
    sql = f'''INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause) VALUES({user.getNo()},"{user.getIp()}",NOW() + INTERVAL {store.ddosBlockHour} HOUR,"{store.BLACK_REASON_CODE['Ddos 주의']}");'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    else:
        log = loger.Loger()
        log.setLog(store.LOG_NAME['블랙리스트'], f"{user.getEmail()}({user.getIp()}) {store.getBlackReason(store.BLACK_REASON_CODE['Ddos 주의'])}사유로 {store.ddosBlockHour}시간동안 BlackList에 추가됨")
        return True

'''
유저 정보 수정하기
parameter: user객체(userDTO)
return: 
'''
def updateUser(user):
    pass

'''
상태 변경
parameter: userNo(int), u_state(int)
return: 실패 0, 성공 1
'''
def updateUserState(uno, u_state):
    sql = f'UPDATE user SET u_state = {u_state} WHERE u_no = {uno}'
    result = db.setData(sql=sql)
    return result

'''
비밀번호 수정하기
parameter: user객체(userDTO), 현재비번(String), 새비번(String), 비번확인(String)
return: store.joinResultCode (int)
'''
def updateUserPassword(user, nowPw, newPw, newConfirm):
    def __checkPwRegex(pw):
        result = False
        # 비밀번호 패턴: 영문자, 숫자, 특수문자가 모두 들어간 8~16자리
        pwPtn = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
        if re.match(pwPtn, pw):
            result = True
        return result
    # 변경할 비밀번호와 확인이 다를 때
    if newPw != newConfirm:
        return store.USER_RESULT_CODE['Confirm 오류']
    # 사용중인 비밀번호와 변경하고자 하는 비밀번호가 같을 때
    if nowPw == newPw:
        return store.USER_RESULT_CODE['nowPw=newPw']
    # 비밀번호의 형식이 틀렸을 때
    elif not __checkPwRegex(newPw):
        return store.USER_RESULT_CODE['Pw 형식 오류']
    # 현재 비밀번호가 틀렸을 때
    elif user.getPw() != __encryptPw(nowPw):
        return store.USER_RESULT_CODE['비밀번호 틀림']
    else:
        sql = f'UPDATE user SET u_pw = "{__encryptPw(newPw)}" WHERE u_no = {user.getNo()}'
        result = db.setData(sql=sql)
        if result == 0:
            return store.USER_RESULT_CODE['실패-unknown']
        else:
            return store.USER_RESULT_CODE['비밀번호 변경 성공']

'''
유저 탈퇴
parameter: 회원번호(int), 비밀번호(String)
return: store.joinResultCode(int)
'''
def leaveUser(uno, pw):
    user = getUserByUserNo(uno=uno)
    if user.getPw() != __encryptPw(pw=pw):
        return store.USER_RESULT_CODE['비밀번호 틀림']
    sql = f'''UPDATE user SET u_state = {store.USER_STATE_CODE['탈퇴']} WHERE u_no = {uno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return store.USER_RESULT_CODE['실패-unknown']
    return store.USER_RESULT_CODE['회원 탈퇴 성공']

'''
세션 만료시간 갱신
parameter: user객체(userDTO)
return: 실패 0, 성공 1 (int)
'''
def updateSessionTime(user):
    sql = f'UPDATE sessionlist SET s_expire = NOW() + INTERVAL {store.sessionTime} HOUR WHERE u_no = {user.getNo()}'
    result = db.setData(sql=sql)
    return result

'''
이메일과 비밀번호로 세션키 받기(세션 등록)
parameter: email(String), pw(String)
return: sessionKey(string)
'''
def getSessionKeyByEmailAndPw(email,pw,ip):
    sql = f'SELECT * FROM user WHERE u_email="{email}" AND u_pw="{__encryptPw(pw=pw)}" AND u_state NOT IN (0, 3)'
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
def getUserByUserNo(uno, ip=''):
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
    sql = 'SELECT u_no FROM blacklist WHERE bl_expire >= NOW()'
    result = db.getData(sql=sql)
    for uno in result:
        if uno != 0:
            blackList.append(uno)
    sql = 'SELECT bl_ip FROM blacklist WHERE bl_expire >= NOW()'
    result = db.getData(sql=sql)
    for bip in result:
        blackList.append(bip)
    return blackList

'''
유저 삭제하기(u_status를 3으로 update)
parameter: user객체(userDTO)
return: 
'''
def deleteUser(user):
    pass