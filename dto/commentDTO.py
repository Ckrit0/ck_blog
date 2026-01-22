from dao import userDAO, boardDAO

class CommentDTO:
    def __init__(self):
        self.no = None
        self.bno = None
        self.uno = None
        self.ip = None
        self.comment = None
        self.upper = None
        self.isDelete = None
        self.userEmail = None
        self.userState = None
        self.boardTitle = None
        
    def setCommentByDbResult(self,dbResult):
        self.no = dbResult[0]
        self.bno = dbResult[1]
        self.uno = dbResult[2]
        self.ip = dbResult[3]
        self.comment = dbResult[4]
        self.date = dbResult[5]
        self.upper = dbResult[6]
        self.isDelete = dbResult[7]
        self.userEmail = dbResult[8]
        self.userState = dbResult[9]
        self.boardTitle = dbResult[10]

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
    
    def getEmail(self):
        return self.userEmail
    
    def getMarkingEmail(self):
        emailParts = self.userEmail.split('@')
        markingEmail = emailParts[0][0:3] + '*' * (len(emailParts[0]) -3) + '@' + emailParts[1]
        return markingEmail
    
    def getBoardTitle(self):
        return self.boardTitle

    def getShortBoardTitle(self):
        boardTitle = self.boardTitle
        if len(boardTitle) > 15:
            boardTitle = boardTitle[0:15] + '...'
        return boardTitle