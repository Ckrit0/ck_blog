from dao import userDAO

'''
client가 블랙리스트에 포함되어있는지 확인
parameter: user객체(userDTO), ip(String)
return: 블랙리스트라면 True, 아니라면 False(bool)
'''
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