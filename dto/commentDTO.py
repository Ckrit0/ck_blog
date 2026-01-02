class CommentDTO:
    def __init__(self):
        self.no = None
        self.bno = None
        self.uno = None
        self.ip = None
        self.comment = None
        self.upper = None
        self.isDelete = None
    
    def setCommntAll(self,no,bno,uno,ip,comment,upper,isDelete):
        self.no = no
        self.bno = bno
        self.uno = uno
        self.ip = ip
        self.comment = comment
        self.upper = upper
        self.isDelete = isDelete

    def setNo(self,no):
        self.no = no
        
    def setBoardNo(self,bno):
        self.bno = bno

    def setUserNo(self,uno):
        self.uno = uno

    def setIp(self,ip):
        self.ip = ip
    
    def setComment(self,comment):
        self.comment = comment
    
    def setUpper(self,upper):
        self.upper = upper
    
    def setIsDelete(self,isDelete):
        self.isDelete

    def getNo(self):
        return self.no
    
    def getBoardNo(self):
        return self.bno
    
    def getUserNo(self):
        return self.uno
    
    def getIP(self):
        return self.ip
    
    def getComment(self):
        return self.comment
    
    def getUpper(self):
        return self.upper
    
    def getIsDelete(self):
        return self.isDelete