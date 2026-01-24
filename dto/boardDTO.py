from service import userService, boardService

class BoardDTO:
    def __init__(self):
        self.no = None
        self.uno = None
        self.cno = None
        self.date = None
        self.title = None
        self.content = None
        self.isDelete = 0
        self.ip = None
        self.uEmail = None
        self.uState = 0
        self.view = None
        self.like = None
    
    def setBoardByDbResult(self,dbResult):
        self.no = dbResult[0]
        self.uno = dbResult[1]
        self.cno = dbResult[2]
        self.date = dbResult[3]
        self.title = dbResult[4]
        self.content = dbResult[5]
        self.isDelete = dbResult[6]
        self.ip = dbResult[7]
        self.uEmail = dbResult[8]
        self.uState = dbResult[9]
        self.view = dbResult[10]
        self.like = dbResult[11]

    def setNo(self,no):
        self.no = no
    
    def setUserNo(self,uno):
        self.uno = uno

    def setCategoryNo(self,cno):
        self.cno = cno

    def setDate(self,date):
        self.date = date
    
    def setTitle(self,title):
        self.title = title

    def setContent(self,content):
        self.content = content

    def setIsDelete(self,isDelete):
        self.isDelete = isDelete

    def setIp(self,ip):
        self.ip = ip
    
    def setUEmail(self,uEmail):
        self.uEmail = uEmail
    
    def setUState(self,uState):
        self.uState = uState

    def setLike(self,like):
        self.like = like
    
    def setView(self,view):
        self.view = view
        
    def getNo(self):
        return self.no

    def getUserNo(self):
        return self.uno
        
    def getCategoryNo(self):
        return self.cno
    
    def getDate(self):
        return self.date
    
    def getTitle(self):
        return self.title
    
    def getShortTitle(self):
        return boardService.shortTitle(self.title)
    
    def getContents(self):
        return self.content
    
    def getIsDelete(self):
        return self.isDelete
    
    def getIp(self):
        return self.ip
    
    def getMarkingIp(self):
        return userService.markingIp(self.ip)
            
    def getUserEmail(self):
        return self.uEmail
    
    def getMarkingEmail(self):
        print(self.uState)
        return userService.markingEmail(self.uEmail, self.uState)
    
    def getUserState(self):
        return self.uState

    def getView(self):
        return self.view
    
    def getLike(self):
        return self.like
