class User:
    def __init__(self):
        self.no = None
        self.email = None
        self.ip = None
        self.pw = None
        self.state = None
        self.lastDate = None
        self.joinDate = None
    
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
    def getEmail(self):
        return self.email
    def getip(self):
        return self.ip
    def getPw(self):
        return self.pw
    def getState(self):
        return self.state
    def getLastDate(self):
        return self.lastDate
    def getJoinDate(self):
        return self.joinDate