from dotenv import load_dotenv
import os

load_dotenv() # .env 파일 로드

####################
## 기본 설정 관련 ##
####################

secret_key = os.environ.get("secretKey") # 플라스크 시크릿 키
flask_port = 5000
flask_debug = True
sessionTime = 1 # 세션 유지 시간(hour)
verifyExpireTime = 10 # 인증코드 유효시간(minute)
verifyList = [] # 인증코드 저장 리스트
send_email_addr = 'ckrit3@gmail.com' # Gmail 발신자 주소
send_email_key = os.environ.get("emailKey") # Gmail 앱 비밀번호
send_eamil_smtp = "smtp.gmail.com" # Gmail SMTP 서버 주소
send_email_port = 587 # Gmail SMTP 서버 포트
send_email_title = '인증 확인 메일입니다.' # 인증 메일 제목
send_email_message = '''
안녕하세요. CkriT 블로그입니다.
위 인증 코드를 인증 코드 입력란에 입력해주세요.
인증 코드는 10분간 유효하며, 대소문자를 구분합니다.
본인이 요청한 것이 아닌 경우, 답장 주시면 조치하겠습니다.
    from. CkriT 블로그 - 널리 인간을 일 없게 하라
'''
hostDirectory = os.environ.get("hostDir") # 호스트 경로
imageUploadDirectory = os.path.join(hostDirectory, 'static','uploads') # 이미지 저장경로
imageDeleteDirectory = os.path.join(imageUploadDirectory, 'deleted') # 이미지 삭제경로
imageDummyDirectory = os.path.join(imageUploadDirectory, 'dummy') # 더미 파일 경로
if not os.path.exists(imageUploadDirectory): # 경로가 없다면 만들기
    os.makedirs(imageUploadDirectory)
if not os.path.exists(imageDeleteDirectory):
    os.makedirs(imageDeleteDirectory)
if not os.path.exists(imageDummyDirectory):
    os.makedirs(imageDummyDirectory)
imageSize = 16 * 1024 * 1024 # 이미지 최대 크기
PAGE_COUNT = { # 한 페이지에 보여줄 목록의 갯수
    '기본값': 5,
    '메인' : 20,
    '유저' : 5,
    '카테고리' : 5,
    '카테고리페이지' : 15,
    '검색' : 15,
    '댓글' : 5
}
shortTitleCount = 12 # 짧은 제목 글자수
middleTitleCount = 40 # 중간 제목 글자수
shortWordCount = 100 # 짧은 글 내용 글자수
searchWordCount = 400 # 검색 글 내용 글자수
searchWeight = [10,5,1] # 검색어 가중치. [전체,단어,글자]

###############
## 유저 관련 ##
###############

USER_STATE_CODE = {
    '비회원':0,
    '미인증':1,
    '인증':2,
    '탈퇴':3,
    '블랙리스트':4,
    '관리자':5
}

USER_RESULT_CODE = {
    '정상 가입':0,
    'Email 형식 오류':1,
    'Pw 형식 오류':2,
    'Confirm 오류':3,
    '가입된 Email':4,
    '세션 만료': 5,
    '블랙리스트':6,
    '비밀번호 틀림':7,
    '비밀번호 변경 성공': 8,
    'nowPw=newPw':9,
    '회원 탈퇴 성공': 10,
    '인증 성공': 11,
    '발급된 코드 없음':12,
    '코드 불일치':13,
    '시간 종료':14,
    '메일 발송 완료':15,
    '블랙리스트 등록':16,
    '유저 상태 변경':17,
    '로그아웃':18,
    '로그인':19,
    '기로그인':20,
    '좋아요 성공':21,
    '삭제된 댓글':22,
    '검색어 부족':23,
    '글작성성공':24,
    '권한없음':25,
    '글삭제성공':26,
    '삭제된글':27,
    
    '실패-unknown':999
}

USER_MESSAGE = { # userResultCode에 따라 사용자에게 보여줄 메시지
    0 : "회원 가입에 성공하였습니다.",
    1 : "Email 형식이 올바르지 않습니다.",
    2 : "비밀번호 형식이 올바르지 않습니다.",
    3 : "비밀번호 확인이 일치하지 않습니다.",
    4 : "이미 가입된 Email 주소입니다.",
    5 : "세션이 만료되었습니다. 다시 로그인 해주세요.",
    6 : "블랙리스트에 등록된 사용자입니다. 관리자에게 문의하세요.",
    7 : "비밀번호가 일치하지 않습니다.",
    8 : "비밀번호가 성공적으로 변경되었습니다.",
    9 : "새 비밀번호는 현재 비밀번호와 같을 수 없습니다.",
    10 : "회원 탈퇴가 성공적으로 처리되었습니다.",
    11 : "이메일 인증이 성공적으로 완료되었습니다.",
    12 : "발급된 인증 코드가 없습니다. 인증 코드를 다시 요청해주세요.",
    13 : "인증 코드가 일치하지 않습니다. 다시 확인해주세요.",
    14 : "인증 코드의 유효 기간이 만료되었습니다. 새로운 코드를 요청해주세요.",
    15 : "인증 메일이 성공적으로 발송되었습니다. 메일함을 확인해주세요.",
    16 : "블랙리스트에 추가되었습니다. 일정 시간이 지나면 해제됩니다.",
    17 : "유저 상태가 성공적으로 변경되었습니다.",
    18 : "로그아웃 되었습니다.",
    19 : "로그인 되었습니다.",
    20 : "로그인중입니다.",
    21 : "좋아요 성공",
    22 : "삭제된 댓글입니다.",
    23 : "검색은 최소 2글자 이상 입력해야합니다.(공백 제외)",
    24 : "글이 작성되었습니다.",
    25 : "권한이 없습니다.",
    26 : "글이 삭제되었습니다.",
    27 : "삭제된 글입니다.",
    999 : "알 수 없는 이유로 작업에 실패하였습니다. 잠시 후 다시 시도해주세요."
}

def getUserState(userStateCode):
    for key, value in USER_STATE_CODE.items():
        if value == userStateCode:
            return key
        
def getUserResult(joinResultCode):
    for key, value in USER_RESULT_CODE.items():
        if value == joinResultCode:
            return key
        
def getUserMessage(userResultCode):
    return USER_MESSAGE[userResultCode]



###############
## 로그 관련 ##
###############

logPath = os.path.join(hostDirectory, 'log') # 로그 저장 경로
LOG_NAME = { # 로그 파일 이름
    '유저' : 'user',
    '시스템' : 'system',
    '데이터베이스' : 'database'
}


#####################
## 블랙리스트 관련 ##
#####################

checkDdos_min = 10                  # (Ddos) 분당 접속 허용 횟수
checkDdos_hour = 60                 # (Ddos) 시간당 접속 허용 횟수
ddosBlockHour = 1                   # (Ddos) 블랙리스트 처리 될 시간
ddosBlackListCause = 'Ddos 주의'    # (Ddos) 블랙리스트 처리시 사유
BLACK_REASON_CODE = {
    'Ddos 주의' : 0,
    '기타' : 999
}
def getBlackReason(blackReasonCode):
    for key, value in BLACK_REASON_CODE.items():
        if value == blackReasonCode:
            return key