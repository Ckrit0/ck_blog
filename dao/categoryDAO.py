from dto import categoryDTO
from service import db, store

####################################################################################################
####################################### Get Category Object ########################################
####################################################################################################
def getCategoryList():
    '''
    카테고리 리스트 가져오기
    return: 카테고리객체 리스트([[상위리스트,[하위리스트...]]...])
    '''
    categoryList = []
    sql = f'''SELECT * from category WHERE c_upper IS NULL'''
    parentCategoryList = db.getData(sql=sql)
    for parentCategory in parentCategoryList:
        pc = categoryDTO.CategoryDTO()
        pc.setCategory(parentCategory[0],parentCategory[1],parentCategory[2],parentCategory[3])
        tempList = []
        sql = f'''SELECT * from category WHERE c_upper={pc.getNo()}'''
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

def getWritableCategoryList(user):
    '''
    유저별 글 작성이 가능한 카테고리 목록 가져오기
    parameter: 유저객체(userDTO)
    return: 작성가능 카테고리 리스트([categoryDTO,...]])
    '''
    '''
    지금은 그냥 하드코딩으로 함. 권한용 DB 테이블 만들어야할듯
    '''
    wholeCategoryList = getCategoryList()
    writableCategoryList = []
    if user.getState() == store.USER_STATE_CODE['관리자']:
        for Pcategory in wholeCategoryList:
            for category in Pcategory[1]:
                writableCategoryList.append(category)
    elif user.getState() == store.USER_STATE_CODE['비회원']:
        writableCategoryList = []
    elif user.getState() == store.USER_STATE_CODE['탈퇴']:
        writableCategoryList = []
    elif user.getState() == store.USER_STATE_CODE['블랙리스트']:
        writableCategoryList = []
    else:
        for Pcategory in wholeCategoryList:
            for category in Pcategory[1]:
                if category.getNo() == 5:
                    writableCategoryList.append(category)
    return writableCategoryList

####################################################################################################
####################################### Set Category Object ########################################
####################################################################################################
def setCategory(category):
    '''
    카테고리 추가하기
    parameter: 카테고리객체(categoryDTO)
    return: 
    '''
    cName = category.getName()
    cUpper = category.getUpper()
    cOrder = category.getOrder()
    sql = f'''INSERT INTO category(c_name,c_upper,c_order) VALUES("{cName}",'''
    if cUpper == None:
        sql += f'''Null, {cOrder})'''
    else:
        sql += f'''"{cUpper}",{cOrder})'''
    result = db.setData(sql=sql)
    return result

def updateCategory(category):
    '''
    카테고리 수정하기
    parameter: 카테고리객체(categoryDTO)
    return: 성공/실패(True/False)
    '''
    cno = category.getNo()
    cName = category.getName()
    cUpper = category.getUpper()
    cOrder = category.getOrder()
    sql = f'''UPDATE category SET c_name="{cName}", c_upper={cUpper}, c_order={cOrder} WHERE c_no={cno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True

def deleteCategory(category):
    '''
    카테고리 삭제하기
    parameter: 카테고리객체(categoryDTO)
    return: 성공/실패(True/False)
    '''
    cno = category.getNo()
    sql = f'''DELETE FROM category WHERE c_no={cno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True