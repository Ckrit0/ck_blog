from dao import userDAO

def checkBlackList(user,ip):
    result = False
    blackList = userDAO.getBlackList()
    if user.getNo() in blackList:
        result = True
    elif user.getIp() in blackList:
        result = True
    elif ip in blackList:
        result = True
    return result