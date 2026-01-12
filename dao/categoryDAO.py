from dto import categoryDTO
from service import db

'''
카테고리 추가하기
parameter: 카테고리객체(categoryDTO)
return: 
'''
def setCategory(category):
    cName = category.getName()
    cUpper = category.getUpper()
    sql = f'INSERT INTO category(c_name,c_upper) VALUES("{cName}",'
    if cUpper == None:
        sql += 'Null)'
    else:
        sql += f'"{cUpper}")'
    result = db.setData(sql=sql)
    return result

'''
카테고리 수정하기
parameter: 카테고리객체(categoryDTO)
return: 
'''
def updateCategory(category):
    sql = f''

'''
카테고리 리스트 가져오기
return: 카테고리객체 리스트(List)
'''
def getCategoryList():
    categoryList = []
    sql = f''
    return categoryList

'''
카테고리 삭제하기
parameter: 카테고리객체(categoryDTO)
return: 
'''
def deleteCategory(category):
    sql = f''