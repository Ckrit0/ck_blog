from service import store

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

    def getMarkingEmail(self):
        emailParts = self.email.split('@')
        markingEmail = emailParts[0][0:3] + '*' * (len(emailParts[0]) -3) + '@' + emailParts[1]
        if self.state == store.USER_STATE_CODE['비회원']:
            return '비회원'
        elif self.state == store.USER_STATE_CODE['미인증']:
            return markingEmail + "(미인증)"
        elif self.state == store.USER_STATE_CODE['탈퇴']:
            return '(탈퇴한 회원)'
        elif self.state == store.USER_STATE_CODE['차단']:
            return '(차단중인 회원)'
        elif self.state == store.USER_STATE_CODE['관리자']:
            return markingEmail + '(관리자)'
    
    def getIp(self):
        return self.ip
    
    def getMarkingIp(self):
        ipList = self.ip.split('.')
        markingIp = ipList[0] + '.' + ipList[1] + '.' + '*' + '.' + '*'
        return markingIp
    
    def getPw(self):
        return self.pw
    
    def getState(self):
        return self.state
    
    def getLastDate(self):
        return self.lastDate
    
    def getJoinDate(self):
        return self.joinDate
    
    def getLeaveDate(self):
        return self.leaveDate