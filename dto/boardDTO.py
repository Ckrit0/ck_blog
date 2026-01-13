from dao import userDAO

class BoardDTO:
    def __init__(self):
        self.no = None
        self.uno = None
        self.cno = None
        self.date = None
        self.title = None
        self.content = None
        self.view = None
        self.like = None
    
    def setBoard(self,uno,cno,title,content,no=None,date=None,view=None,like=None,isDelete=0):
        self.no = no
        self.uno = uno
        self.cno = cno
        self.date = date
        self.title = title
        self.content = content
        self.view = view
        self.like = like
        self.isDelete = isDelete

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

    def setLike(self,like):
        self.like = like
    
    def setView(self,view):
        self.view = view
    
    def setIsDelete(self,isDelete):
        self.isDelete = isDelete
    
    def getNo(self):
        return self.no

    def getUserNo(self):
        return self.uno
    
    def getUserEmail(self):
        return userDAO.getUserByUserNo(self.uno).getEmail()
    
    def getCategoryNo(self):
        return self.cno
    
    def getDate(self):
        return self.date
    
    def getTitle(self):
        return self.title
    
    def getContents(self):
        return self.content
    
    def getView(self):
        return self.view
    
    def getLike(self):
        return self.like

    def getIsDelete(self):
        return self.isDelete