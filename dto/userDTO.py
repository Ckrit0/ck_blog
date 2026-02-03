from service import store, userService
from datetime import datetime

class UserDTO:
    def __init__(self):
        self.no = 0
        self.email = None
        self.ip = None
        self.pw = None
        self.state = 0
        self.lastDate = None
        self.joinDate = None
        self.leaveDate = None
    
    def setUserByDbResult(self,dbResult):
        self.no = dbResult[0]
        self.email = dbResult[1]
        self.pw = dbResult[2]
        self.state = dbResult[3]
        self.lastDate = dbResult[4]
        self.joinDate = dbResult[5]
        self.leaveDate = dbResult[6]

    def setNo(self,no):
        self.no = no

    def setEmail(self,email):
        self.email = email

    def setIp(self,ip):
        self.ip = ip

    def setPw(self,pw):
        self.pw = pw

    def setState(self,state):
        self.state = state

    def setLastDate(self,lastDate):
        self.lastDate = lastDate

    def setJoinDate(self,joinDate):
        self.joinDate = joinDate
    
    def setLeaveDate(self,leaveDate):
        self.leaveDate = leaveDate

    def getNo(self):
        return self.no
    
    def getEmail(self):
        return self.email

    def getMaskingEmail(self):
        return userService.maskingEmail(self.email, self.state)
    
    def getIp(self):
        return self.ip
    
    def getMaskingIp(self):
        return userService.maskingIp(self.ip)
    
    def getPw(self):
        return self.pw
    
    def getState(self):
        return self.state
    
    def getLastDate(self):
        return self.lastDate
    
    def getJoinDate(self):
        return self.joinDate
    
    def getFormatJoinDate(self):
        return self.joinDate.strftime("%Y-%m-%d")
    
    def getLeaveDate(self):
        return self.leaveDate