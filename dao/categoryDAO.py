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
    cOrder = category.getOrder()
    sql = f'INSERT INTO category(c_name,c_upper,c_order) VALUES("{cName}",'
    if cUpper == None:
        sql += f'Null, {cOrder})'
    else:
        sql += f'"{cUpper}",{cOrder})'
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
return: 카테고리객체 리스트([[상위리스트,[하위리스트...]]...])
'''
def getCategoryList():
    categoryList = []
    sql = 'SELECT * from category WHERE c_upper IS NULL'
    parentCategoryList = db.getData(sql=sql)
    for parentCategory in parentCategoryList:
        pc = categoryDTO.CategoryDTO()
        pc.setCategory(parentCategory[0],parentCategory[1],parentCategory[2],parentCategory[3])
        tempList = []
        sql = f'SELECT * from category WHERE c_upper={pc.getNo()}'
        childCategoryList = db.getData(sql=sql)
        for childCategory in childCategoryList:
            cc = categoryDTO.CategoryDTO()
            cc.setCategory(childCategory[0],childCategory[1],childCategory[2],childCategory[3])
            tempList.append(cc)
        childList = []
        for i in range(len(tempList)):
            for j in range(len(tempList)):
                if tempList[j].getOrder() == i+1:
                    childList.append(tempList[j])
        categoryList.append([pc,childList])
    result = []
    for i in range(len(categoryList)):
        for j in range(len(categoryList)):
            if categoryList[j][0].getOrder() == i+1:
                result.append(categoryList[j])
    return result

'''
카테고리 삭제하기
parameter: 카테고리객체(categoryDTO)
return: 
'''
def deleteCategory(category):
    sql = f''