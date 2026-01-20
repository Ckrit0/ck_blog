class UserDTO:
    def __init__(self):
        self.no = 0
        self.email = None
        self.ip = None
        self.pw = None
        self.state = 0
        self.lastDate = None
        self.joinDate = None
    
    def setUser(self,dbResult):
        self.no = dbResult[0]
        self.email = dbResult[1]
        self.pw = dbResult[2]
        self.state = dbResult[3]
        self.lastDate = dbResult[4]
        self.joinDate = dbResult[5]

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

    def getNo(self):
        return self.no
    
    def getPlaneEmail(self):
        return self.email

    def getEmail(self):
        if self.state == 0:
            return '비회원'
        elif self.state == 1:
            return self.email + "(미인증)"
        elif self.state == 3:
            return '탈퇴한 회원'
        return self.email
    
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