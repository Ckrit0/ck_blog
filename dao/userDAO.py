from dto import userDTO
from service import db, store, loger
import string, random, re, smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

################################################################################################
######################################## Service Logic #########################################
################################################################################################

def __updateVerifyList():
    '''
    30분 초과 인증코드들 삭제
    '''
    expireIndexList = []
    for i in range(len(store.verifyList)):
        if store.verifyList[i]['expire']  + timedelta(minutes=30) < datetime.now():
            expireIndexList.append(i)
    for i in range(len(expireIndexList)):
        store.verifyList.pop(expireIndexList[i]-i)

def encryptPw(pw):
    '''
    비밀번호 암호화 (복호화 불가. 암호화 된 비밀번호를 서로 비교해야 함.)
    parameter: pw(String)
    return: encPw(String)
    '''
    encPw = ""
    key = store.secret_key
    for i in range(len(pw)):
        pwCharNo = ord(pw[i]) + 10
        keyCharNo = ord(key[i % len(key)])
        saveCharNo = (pwCharNo * keyCharNo) // 10
        encPw += str(saveCharNo)
    while len(encPw) < 40:
        tempPw = ""
        for i in range(len(encPw)):
            tempPw += encPw[i] + str((ord(pw[i%len(pw)]) * ord(key[i%len(key)]))//8)
        encPw = tempPw
    while len(encPw) > 100:
        tempPw = ""
        for i in range(len(encPw)):
            if i % 5 != 0:
                tempPw += encPw[i]
        encPw = tempPw
    return encPw

def setView(user):
    '''
    글이 아닌 페이지의 조회 설정하기
    b_no를 0으로 설정, 비회원의 경우 userNo를 0으로 설정
    parameter: user객체(userDTO)
    return: 실패 0, 성공 1 (int)
    '''
    sql = f'''INSERT INTO views(b_no,u_no,v_ip) VALUES(0,{user.getNo()},"{user.getIp()}")'''
    result = db.setData(sql=sql)
    return result

def sendMail(email):
    '''
    인증코드 메일 발송
    parameter: email(String), verifyCode(String)
    return: (int)
        store.USER_RESULT_CODE['메일 발송 완료']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    def __getCode(): # 8자리 랜덤 인증코드 생성
        code = ''
        pool = string.ascii_letters + string.digits
        for i in range(8):
            code += random.choice(pool)
        return code
    
    def __setVerify(email,code): # 인증코드 저장(host의 store에서 관리)
        expireTime = datetime.now() + timedelta(minutes=store.verifyExpireTime)
        verifyDict = {
            'email': email,
            'code' : code,
            'expire' : expireTime
        }
        store.verifyList.append(verifyDict)
    
    __updateVerifyList() # 만료된 인증코드 삭제
    code = __getCode()

    # 이메일 발송 설정
    message = MIMEMultipart()
    message["From"] = store.send_email_addr
    message["To"] = email
    message["Subject"] = store.send_email_title + f'"{code}"' # 제목에도 인증코드 포함
    text = f'인증 코드: "{code}"\n' + store.send_email_message
    message.attach(MIMEText(text, 'plain'))

    # 이메일 발송 시도
    try:
        server = smtplib.SMTP(host=store.send_eamil_smtp, port=store.send_email_port)
        server.starttls() # TLS 암호화 적용
        server.login(user=store.send_email_addr, password=store.send_email_key)
        server.sendmail(store.send_email_addr, email, message.as_string())
        __setVerify(email=email,code=code)
        log = loger.Loger()
        log.setLog(store.LOG_NAME['유저'], f"이메일 전송 완료: {email}, 인증코드: {code}")
        return store.USER_RESULT_CODE['메일 발송 완료']
    except Exception as e:
        log = loger.Loger()
        log.setLog(store.LOG_NAME['유저'], f"이메일 전송 실패: {e}")
        return store.USER_RESULT_CODE['실패-unknown']
    finally:
        server.quit() # 서버 연결 종료

def matchVerify(email,code):
    '''
    인증코드 확인
    parameter: email(String), code(String)
    return: (int)
        store.USER_RESULT_CODE['인증 성공']
        store.USER_RESULT_CODE['시간 종료']
        store.USER_RESULT_CODE['코드 불일치']
        store.USER_RESULT_CODE['발급된 코드 없음']
    '''
    __updateVerifyList() # 만료된 인증코드 삭제
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


################################################################################################
####################################### Get User Object ########################################
################################################################################################

def getUserByUserNo(uno, ip=''):
    '''
    유저번호로 유저객체 받기
    parameter: 유저번호(int), IP(String)
    return: user객체(userDTO)
    '''
    user = userDTO.UserDTO()
    if uno != 0:
        sql = f'''SELECT * FROM user WHERE u_no = {uno} AND u_state != 0'''
        result = db.getData(sql=sql)
        if len(result) != 0:
            user.setUserByDbResult(result[0])
    user.setIp(ip=ip)
    return user

def getUserByEmailAddress(email):
    '''
    메일주소로 가입된 이메일 여부와 인증여부 확인
    parameter: email(String)
    return: user객체(userDTO)
    '''
    sql = f'''SELECT * FROM user WHERE u_email = "{email}" AND u_state NOT IN (0, 3)'''
    result = db.getData(sql=sql)
    user = userDTO.UserDTO()
    if len(result) != 0:
        user.setUserByDbResult(result[0])
    return user

def getViewCount(user):
    '''
    유저 및 ip가 1분, 1시간 동안 접속한 횟수 받기
    parameter: 유저객체(userDTO)
    return: 리스트([1분user접속횟수,1시간user접속횟수,1분ip접속횟수,1시간ip접속횟수])
    '''
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

def getRecentlyTitleList_user(user):
    '''
    유저별 마지막 읽은 글목록 가져오기
    parameter: 유저객체(userDTO)
    return: 마지막 본 글 제목 리스트([[글번호(int),글제목(string)]...])
    '''
    limit = store.PAGE_COUNT['유저별']
    sql = f''''''
    uno = user.getNo()
    uip = user.getIp()
    if uno == 0:
        sql = f'''SELECT b.b_no, b.b_title FROM board b\
            JOIN (SELECT DISTINCT b_no FROM views WHERE v_ip = "{uip}" AND b_no != 0 ORDER BY v_date DESC LIMIT {limit}) v\
            ON b.b_no = v.b_no'''
    else:
        sql = f'''SELECT b.b_no, b.b_title FROM board b\
            JOIN (SELECT DISTINCT b_no FROM views WHERE u_no = {uno} AND b_no != 0 ORDER BY v_date DESC LIMIT {limit}) v\
            ON b.b_no = v.b_no'''
    result = db.getData(sql=sql)
    return result


################################################################################################
####################################### Set User Object ########################################
################################################################################################

def setUser(email, pw, confirm, verify):
    '''
    신규 유저 생성(회원 가입)
    parameter: email(String), pw(String), confirm(String), verify(String)
    return: (int)
        store.USER_RESULT_CODE['Confirm 오류']
        store.USER_RESULT_CODE['Email 형식 오류']
        store.USER_RESULT_CODE['Pw 형식 오류']
        store.USER_RESULT_CODE['가입된 Email']
        store.USER_RESULT_CODE['블랙리스트']
        store.USER_RESULT_CODE['정상 가입']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    def __checkEmailAndPwRegex(email, pw): # 이메일과 비밀번호 형식 체크
        result = [False, False]
        emailPtn = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(emailPtn, email):
            result[0] = True
        pwPtn = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
        if re.match(pwPtn, pw):
            result[1] = True
        return result
    
    # password와 컨펌이 서로 맞지 않는 경우
    if pw != confirm:
        return store.USER_RESULT_CODE['Confirm 오류']
    
    # email 주소나 PW 형식이 틀린 경우
    checkRegex = __checkEmailAndPwRegex(email=email, pw=pw)
    if checkRegex[0] == False:
        return store.USER_RESULT_CODE['Email 형식 오류']
    elif checkRegex[1] == False:
        return store.USER_RESULT_CODE['Pw 형식 오류']
    
    # 이메일을 이미 사용중인 유저의 데이터(탈퇴한 회원 제외) 가져오기
    user = getUserByEmailAddress(email=email)

    verifyResult = None
    sqlList = []

    # 기존에 가입된 이메일 주소가 있는 경우 처리
    if user.getNo() != 0:
        # 블랙리스트 상태인 경우 가입 불가
        if user.getState() == store.USER_STATE_CODE['블랙리스트']:
            return store.USER_RESULT_CODE['블랙리스트']
        
        # verify 미진행시 가입 불가
        elif verify == "" or verify == None:
            return store.USER_RESULT_CODE['가입된 Email']
        
        # verify 진행시 처리
        else:
            verifyResult = matchVerify(email=email, code=verify) # 인증코드 확인
            
            # 인증 성공시 기존 생성된 이메일 주소의 탈퇴처리
            if verifyResult == store.USER_RESULT_CODE['인증 성공']:
                user.setState(state=store.USER_STATE_CODE['인증'])
                sql = f'''UPDATE user SET u_state = {store.USER_STATE_CODE['탈퇴']} WHERE u_email = "{email}"'''
                # 회원가입 처리가 정상적으로 처리되지 않을 때를 위해서 List방식으로 한번에 commit
                sqlList.append(sql)
            
            # 인증 실패시 기존 생성된 이메일 주소의 강제 진행 불가
            else:
                return store.USER_RESULT_CODE['가입된 Email']
        
    # 신규 이메일 주소인 경우 처리
    else:
        user.setEmail(email=email)
        user.setPw(pw=encryptPw(pw=pw))
        user.setState(state=store.USER_STATE_CODE['미인증'])

    sql = f'''INSERT INTO user(u_email,u_pw,u_state) VALUES("{user.getEmail()}","{user.getPw()}",{user.getState()})'''
    sqlList.append(sql)
    result = db.setDatas(sqlList=sqlList)
    if result != 0:
        log = loger.Loger()
        if len(sqlList) >= 2:
            log.setLog(store.LOG_NAME['유저'], f"기존 유저 재가입: {email}")
        else:
            log.setLog(store.LOG_NAME['유저'], f"신규 유저 가입: {email}")
        return store.USER_RESULT_CODE['정상 가입']
    else :
        return store.USER_RESULT_CODE['실패-unknown']

def updateUserState(uno, u_state):
    '''
    유저 상태 변경
    parameter: userNo(int), u_state(int)
    return: (int)
        store.USER_RESULT_CODE['유저 상태 변경']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    sql = f'''UPDATE user SET u_state = {u_state} WHERE u_no = {uno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return store.USER_RESULT_CODE['실패-unknown']
    return store.USER_RESULT_CODE['유저 상태 변경']

def updateUserPassword(user, nowPw, newPw, newConfirm):
    '''
    비밀번호 수정하기
    parameter: user객체(userDTO), 현재비번(String), 새비번(String), 비번확인(String)
    return: (int)
        store.USER_RESULT_CODE['Confirm 오류']
        store.USER_RESULT_CODE['nowPw=newPw']
        store.USER_RESULT_CODE['Pw 형식 오류']
        store.USER_RESULT_CODE['비밀번호 틀림']
        store.USER_RESULT_CODE['비밀번호 변경 성공']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    def __checkPwRegex(pw): # 비밀번호 형식 체크
        result = False
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
    elif user.getPw() != encryptPw(nowPw):
        return store.USER_RESULT_CODE['비밀번호 틀림']
    else:
        sql = f'''UPDATE user SET u_pw = "{encryptPw(newPw)}" WHERE u_no = {user.getNo()}'''
        result = db.setData(sql=sql)
        if result == 0:
            return store.USER_RESULT_CODE['실패-unknown']
        else:
            return store.USER_RESULT_CODE['비밀번호 변경 성공']

def leaveUser(uno, pw):
    '''
    유저 탈퇴
    parameter: 회원번호(int), 비밀번호(String)
    return: (int)
        store.USER_RESULT_CODE['비밀번호 틀림']
        store.USER_RESULT_CODE['회원 탈퇴 성공']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    user = getUserByUserNo(uno=uno)
    if user.getPw() != encryptPw(pw=pw):
        return store.USER_RESULT_CODE['비밀번호 틀림']
    sql = f'''UPDATE user SET u_state = {store.USER_STATE_CODE['탈퇴']} WHERE u_no = {uno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return store.USER_RESULT_CODE['실패-unknown']
    return store.USER_RESULT_CODE['회원 탈퇴 성공']

################################################################################################
########################################### Session ############################################
################################################################################################

def __setSession(user):
    '''
    해당 유저의 세션 생성
    parameter: user객체(userDTO)
    return: sessionKey(String) or False
    '''
    def __getNewSessionKey():
        length = 50
        pool = string.ascii_letters + string.digits
        key = ""
        for i in range(length):
            key += random.choice(pool)
        return key
    sessionKey = __getNewSessionKey()
    sql = f'''INSERT INTO sessionlist(u_no,s_key,s_ip,s_expire)\
        VALUES({user.getNo()},"{sessionKey}","{user.getIp()}",NOW() + INTERVAL {store.sessionTime} HOUR)\
        ON DUPLICATE KEY\
            UPDATE s_key = VALUES(s_key),\
                s_ip = VALUES(s_ip),\
                s_expire = VALUES(s_expire);'''
    result = db.setData(sql=sql)
    if result != 0:
        return sessionKey
    else:
        return False

def getSessionTimeByUserNo(uno):
    '''
    유저 번호로 세션 만료시간 받기 (세션 만료 확인)
    parameter: 유저번호(int)
    return: user객체(userDTO)
    '''
    sql = f'''SELECT s_expire FROM sessionlist WHERE u_no = {uno}'''
    s_expire = db.getData(sql=sql)[0][0]
    return s_expire

def updateSessionTime(user):
    '''
    세션 만료시간 갱신
    parameter: user객체(userDTO)
    return: 실패 0, 성공 1 (int)
    '''
    sql = f'''UPDATE sessionlist SET s_expire = NOW() + INTERVAL {store.sessionTime} HOUR WHERE u_no = {user.getNo()}'''
    result = db.setData(sql=sql)
    return result

def getSessionKeyByEmailAndPw(email,pw,ip=''):
    '''
    이메일과 비밀번호로 세션키 등록 (로그인 처리)
    parameter: email(String), pw(String)
    return: sessionKey(String)
    '''
    sql = f'''SELECT * FROM user WHERE u_email="{email}" AND u_pw="{encryptPw(pw=pw)}" AND u_state NOT IN (0, 3)'''
    result = db.getData(sql=sql)[0]
    user = userDTO.UserDTO()
    user.setUserByDbResult(dbResult=result)
    user.setIp(ip=ip)
    sessionKey = __setSession(user=user) # 세션 등록
    return sessionKey

def getUserBySessionKey(cookieKey, ip):
    '''
    세션키를 이용하여 유저객체 받기 (로그인 확인)
    parameter: 세션키(String), IP(String)
    return: user객체(userDTO)
    '''
    if cookieKey == "" or cookieKey == None:
        user = userDTO.UserDTO()
        user.setIp(ip)
        return user
    sql = f'''SELECT * FROM user WHERE u_no = (SELECT u_no FROM sessionlist WHERE s_key = "{cookieKey}") AND u_state NOT IN (0, 3);'''
    result = db.getData(sql=sql)[0]
    user = userDTO.UserDTO()
    user.setUserByDbResult(dbResult=result)
    user.setIp(ip=ip)
    return user

################################################################################################
########################################## BlackList ###########################################
################################################################################################

def getBlackList():
    '''
    블랙리스트 목록 받기
    return: 블랙리스트(List)
    '''
    blackList = []
    sql = f'''SELECT u_no FROM blacklist WHERE bl_expire >= NOW() AND u_no != 0 \
        UNION ALL \
        SELECT bl_ip FROM blacklist WHERE bl_expire >= NOW() AND bl_ip != ""'''
    result = db.getData(sql=sql)
    for unoOrIp in result:
        blackList.append(unoOrIp)
    return blackList

def setBlackList(user, code, reason=''):
    '''
    해당 유저 블랙리스트에 추가
    parameter: user객체(userDTO), store.BLACK_REASON_CODE(int), 사유(String)
    return: (int)
        store.USER_RESULT_CODE['블랙리스트 등록']
        store.USER_RESULT_CODE['실패-unknown']
    '''
    sql = f'''INSERT INTO blacklist(u_no,bl_ip,bl_expire,bl_cause,bl_reason) VALUES({user.getNo()},"{user.getIp()}",NOW() + INTERVAL {store.ddosBlockHour} HOUR,"{code}","{reason}");'''
    result = db.setData(sql=sql)
    if result == 0:
        return store.USER_RESULT_CODE['실패-unknown']
    else:
        log = loger.Loger()
        log.setLog(store.LOG_NAME['유저'], f"블랙리스트 추가: {user.getEmail()}, 사유: {store.getBlackReason(code)}, 상세: {reason}")
        return store.USER_RESULT_CODE['블랙리스트 등록']