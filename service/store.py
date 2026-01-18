from dotenv import load_dotenv
import os

load_dotenv()

# 기본 설정 관련
secret_key = os.environ.get("secretKey")

# 로그 관련
logPath = './log'
logName_blackList = 'blackList'

# 한 페이지에 보여줄 목록의 갯수
pageCount_user = 5
pageCount_all = 5
pageCount_category = 5
pageCount_search = 5
pageCount_comment = 5

# 블랙리스트 관련
checkDdos_min = 10                  # (Ddos) 분당 접속 허용 횟수
checkDdos_hour = 60                 # (Ddos) 시간당 접속 허용 횟수
ddosBlockHour = 1                   # (Ddos) 블랙리스트 처리 될 시간
ddosBlackListCause = 'Ddos 주의'    # (Ddos) 블랙리스트 처리시 사유

# 로그인 관련
failToLogin_msg = "로그인에 실패하였습니다."
logout_msg = "로그아웃 되었습니다."
sessionTimeOut_msg = "세션이 만료되었습니다."
sessionTime = 1 # 세션 유지 시간