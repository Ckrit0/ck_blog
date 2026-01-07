from dto import userDTO
from service import db

'''
신규 유저 생성
parameter: user객체(userDTO)
return: 
'''
def setUser(user):
    pass

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
return: 
'''
def setBlackList(user):
    pass

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
    user = userDTO.UserDTO()
    return user

'''
유저번호로 유저객체 받기
parameter: 유저번호(int)
return: user객체(userDTO)
'''
def getUserByUserNo(uno):
    user = userDTO.UserDTO()
    return user

'''
세션키를 이용하여 유저객체 받기
parameter: 세션키(String)
return: user객체(userDTO)
'''
def getUserBySessionKey(sessionKey):
    user = userDTO.UserDTO()
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
    return blackList

'''
유저 삭제하기(u_status를 3으로 update)
parameter: user객체(userDTO)
return: 
'''
def deleteUser(user):
    pass