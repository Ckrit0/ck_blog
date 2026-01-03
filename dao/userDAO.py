from service import db
from dto import userDTO

def setUser(user):
    pass

def setSession(user, session):
    pass

def setBlackList(user):
    pass

def updateUser(user):
    pass

def updateSessionDate(user):
    pass

def getUserByEmailAndPw(email,pw):
    user = userDTO()
    return user

def getUserByUserNo(uno):
    user = userDTO()
    return user

def getUserBySessionKey(sessionKey):
    user = userDTO()
    return user

def getSessionKeyByUserNo(uno):
    sessionKey = None
    return sessionKey

def getBlackList():
    blackList = []
    return blackList

def deleteUser(user):
    pass