from dotenv import load_dotenv
import os

load_dotenv()

# 기본 설정 관련
secret_key = os.environ.get("secretKey")
send_email_addr = 'ckrit3@gmail.com'
send_email_key = os.environ.get("emailKey")
send_eamil_smtp = "smtp.gmail.com"
send_email_port = 587

# 유저 관련
USER_STATE_CODE = {
    '비회원':0,
    '미인증':1,
    '인증':2,
    '탈퇴':3,
    '블랙리스트':4,
    '관리자':5
}

JOIN_RESULT_CODE = {
    '정상 가입 되었습니다.':0,
    'Email 형식 오류':1,
    'PW 형식 오류':2,
    'Confirm 오류':3,
    '가입된 인증 Email':4,
    '가입된 미인증 Email':5,
    '블랙리스트':6,
    '비밀번호 틀림':7,
    '비밀번호 변경 성공': 8,
    '사용중인 비밀번호와 같음':9,
    '비밀번호 변경 실패':998,
    '가입실패-사유불분명':999
}
def getJoinResult(joinResultCode):
    for key, value in JOIN_RESULT_CODE.items():
        if value == joinResultCode:
            return key

USER_MESSAGE = {
    '로그인성공': "정상적으로 로그인되었습니다.",
    '로그인실패': "로그인에 실패하였습니다.",
    '로그아웃': "로그아웃 되었습니다.",
    '기로그인': "이미 로그인 되어있습니다.",
    '세션만료' : "세션이 만료되었습니다.",
    '가입성공' : "회원 가입에 성공하였습니다.",
    '가입실패-사유모름' : "알 수 없는 이유로 회원 가입에 실패하였습니다."
}

VERIFY_RESULT_CODE = {
    '성공':0,
    '발급된 코드 없음':1,
    '코드 불일치':2,
    '시간 종료':3,
    '메일 발송 완료':4,
    '메일 발송 실패':5,
    '실패-사유모름':99
}

sessionTime = 1 # 세션 유지 시간(hour)
verifyExpireTime = 10 # 인증코드 유효시간(minute)
verifyList = []
send_email_title = '인증 확인 메일입니다.'
send_email_message = '''
위 코드를 입력란에 입력해주세요.
인증코드는 대소문자를 구분합니다.
본인이 요청한 것이 아닌 경우, 답장 주시면 조치하겠습니다.
    from. CkriT 블로그 - 널리 인간을 일 없게 하라
'''

# 로그 관련
logPath = './log'
LOG_NAME = {
    '블랙리스트': 'blackList'
}

# 한 페이지에 보여줄 목록의 갯수
PAGE_COUNT = {
    '유저별':5,
    '카테고리별':5,
    '메인통합': 5,
    '검색결과': 5,
    '댓글':5
}

# 블랙리스트 관련
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