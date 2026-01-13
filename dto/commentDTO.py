from dao import userDAO

class CommentDTO:
    def __init__(self):
        self.no = None
        self.bno = None
        self.uno = None
        self.ip = None
        self.comment = None
        self.upper = None
        self.isDelete = None
    
    def setCommentAll(self,no,bno,uno,ip,comment,date,upper,isDelete):
        self.no = no
        self.bno = bno
        self.uno = uno
        self.ip = ip
        self.comment = comment
        self.date = date
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

    def setDate(self,date):
        self.date = date
    
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
    
    def getUserEmail(self):
        return userDAO.getUserByUserNo(self.uno).getEmail()
    
    def getIP(self):
        return self.ip
    
    def getMarkingIp(self):
        ipList = self.ip.split('.')
        markingIp = ipList[0] + '.' + ipList[1] + '.' + '*' + '.' + '*'
        return markingIp
    
    def getComment(self):
        if self.isDelete == 1:
            return '삭제되었습니다.'
        return self.comment
    
    def getDate(self):
        return self.date
    
    def getUpper(self):
        return self.upper
    
    def getIsDelete(self):
        return self.isDelete