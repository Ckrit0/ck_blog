class CategoryDTO:
    def __init__(self):
        self.no = None
        self.name = None
        self.upper = None
    
    def setCategory(self,no,name,upper):
        self.no = no
        self.name = name
        self.upper = upper
    
    def setNo(self,no):
        self.no = no
    
    def setName(self,name):
        self.name = name
    
    def setUpper(self,upper):
        self.upper = upper
    
    def getNo(self):
        return self.no
    
    def getName(self):
        return self.name
    
    def getUpper(self):
        return self.upper