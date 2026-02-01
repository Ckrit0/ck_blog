from dto import categoryDTO
from service import db, store, boardService
import math

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
            cc.setCount(db.getData(sql=f"SELECT count(*) FROM board WHERE b_isdelete = 0 AND c_no={cc.getNo()}")[0][0])
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

def getTitleList_cathgoryInCategoryPage(cno, page=1):
    '''
    카테고리별 글목록 가져오기(카테고리페이지)
    parameter: 카테고리번호(cono), 페이지(int)
    return: 해당 페이지의 [글 번호(int), 제목(String), 조회수(int), 좋아요수(int), 내용 앞부분(텍스트)]의 리스트
    '''
    cno = int(cno)
    page = int(page)
    if page == 0:
        return []
    limit = store.PAGE_COUNT['카테고리페이지']
    offset = limit * (page-1)
    sql = f'''SELECT b.b_no, b.b_title, b.b_contents, \
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
            (SELECT count(*) FROM comment WHERE b_no=b.b_no) \
            FROM board b WHERE b.c_no={cno} AND b.b_isdelete=0 \
            ORDER BY b.b_no DESC LIMIT {limit} OFFSET {offset}'''
    result = db.getData(sql=sql)
    for titleData in result:
        titleData[1] = boardService.middleTitle(titleData[1])
        titleData[2] = boardService.shortContents(titleData[2])
    return result

def getPageList_category(cno):
    '''
    카테고리별 페이지 리스트 가져오기
    parameter: 카테고리번호(cono)
    return: 페이지 리스트(list)
    '''
    pageList = []
    sql = f'''SELECT count(*) FROM board WHERE c_no={cno} AND b_isdelete=0'''
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['카테고리페이지'])
    for i in range(result):
        pageList.append(i+1)
    return pageList

def getCategoryNameByCno(cno):
    '''
    카테고리 번호로 카테고리 명 가져오기
    parameter: 카테고리번호(cono)
    return: 카테고리명(String)
    '''
    sql = f'''SELECT c_name FROM category WHERE c_no={cno}'''
    result = db.getData(sql=sql)[0][0]
    return result

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