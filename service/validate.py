from dao import userDAO
from service import store
from datetime import datetime

def checkDdos(user):
    '''
    client의 1분동안, 1시간동안 접속 횟수를 확인하고 설정값보다 많으면 블랙리스트 처리
    parameter: user객체(userDTO)
    return: 블랙처리 되면 True, 아니면 False
    '''
    result = False
    viewCountList = userDAO.getViewCount(user=user)
    if viewCountList[0] > store.checkDdos_min:
        result = userDAO.setBlackList(user=user)
    elif viewCountList[1] > store.checkDdos_hour:
        result = userDAO.setBlackList(user=user)
    elif viewCountList[2] > store.checkDdos_min:
        result = userDAO.setBlackList(user=user)
    elif viewCountList[3] > store.checkDdos_hour:
        result = userDAO.setBlackList(user=user)
    return result
    
def checkBlackList(user):
    '''
    client가 블랙리스트에 포함되어있는지 확인
    parameter: user객체(userDTO)
    return: 블랙리스트라면 True, 아니라면 False(bool)
    '''
    result = False
    blackList = userDAO.getBlackList()
    if user.getNo() in blackList:
        result = True
    elif user.getIp() in blackList:
        result = True
    return result

def checkSessionTimeOver(user):
    '''
    세션 만료 여부 확인
    parameter: user객체(userDTO)
    return: 만료 True, 아니면 False(bool)
    '''
    result = False
    if user.getNo() != 0:
        sessionTime = userDAO.getSessionTimeByUserNo(user.getNo())
        now = datetime.now()
        if now > sessionTime:
            result = True
        else:
            # timeover가 아니라면 세션시간 갱신
            userDAO.updateSessionTime(user=user)
    return result