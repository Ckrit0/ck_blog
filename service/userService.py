from service import store, loger
from datetime import datetime, timedelta
import string, random, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    
    updateVerifyList() # 만료된 인증코드 삭제
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

def updateVerifyList():
    '''
    30분 초과 인증코드들 삭제
    '''
    expireIndexList = []
    for i in range(len(store.verifyList)):
        if store.verifyList[i]['expire']  + timedelta(minutes=30) < datetime.now():
            expireIndexList.append(i)
    for i in range(len(expireIndexList)):
        store.verifyList.pop(expireIndexList[i]-i)

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
    updateVerifyList() # 만료된 인증코드 삭제
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

def markingEmail(email, state):
    '''
    이메일 일부 마킹 처리
    parameter: email(String), state(int)
    return: markingEmail(String)
    '''
    emailParts = email.split('@')
    markingEmail = emailParts[0][0:3] + '*' * (len(emailParts[0]) -3) + '@' + emailParts[1]
    if state == store.USER_STATE_CODE['비회원']:
        return '비회원'
    elif state == store.USER_STATE_CODE['미인증']:
        return markingEmail + "(미인증)"
    elif state == store.USER_STATE_CODE['탈퇴']:
        return '(탈퇴한 회원)'
    elif state == store.USER_STATE_CODE['차단']:
        return '(차단중인 회원)'
    elif state == store.USER_STATE_CODE['관리자']:
        return markingEmail + '(관리자)'

def markingIp(ip):
    '''
    IP 일부 마킹 처리
    parameter: ip(String)
    return: markingIp(String)
    '''
    ipList = ip.split('.')
    markingIp = ipList[0] + '.' + ipList[1] + '.' + '*' + '.' + '*'
    return markingIp