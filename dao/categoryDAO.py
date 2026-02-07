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
def __setParentCategory(category):
    '''
    상위 카테고리 추가하고 해당 cno 받기
    parameter: 카테고리객체(categoryDTO)
    return: 추가된 cno(int)
    '''
    cName = category.getName()
    cOrder = category.getOrder()
    sql = f'''INSERT INTO category(c_name,c_upper,c_order) VALUES("{cName}", Null, {cOrder})'''
    dbResult = db.setData(sql=sql)
    result = None
    if dbResult != 0:
        sql = f'''SELECT MAX(c_no) FROM category'''
        result = db.setData(sql=sql)
    return result

def modCategory(categoryList):
    '''
    페이지에서 보내준 리스트로 카테고리 설정하기
    parameter: [[[부모번호,부모이름,부모상위,부모정렬],[[자식번호,자식이름,자식상위,자식정렬],...]],...]
    return: 성공/실패(True/False)
    '''
    def getCategoryListByCategoryList(categoryList):
        result = []
        for cateList in categoryList:
            pCateDtoList = []
            pCateDto = categoryDTO.CategoryDTO()
            pCateDto.setNo(cateList[0][0])
            pCateDto.setName(cateList[0][1])
            pCateDto.setOrder(cateList[0][3])
            pCateDtoList.append(pCateDto)
            cCateDtoList = []
            for cCateList in cateList[1]:
                cCateDto = categoryDTO.CategoryDTO()
                cCateDto.setNo(cCateList[0])
                cCateDto.setName(cCateList[1])
                cCateDto.setUpper(cCateList[2])
                cCateDto.setOrder(cCateList[3])
                cCateDtoList.append(cCateDto)
            pCateDtoList.append(cCateDtoList)
            result.append(pCateDtoList)
        return result
    
    def getDeleteCateNoList(nowCateList, newCateList):
        def getCateNoList(categoryList):
            cateNoList = []
            for cate in categoryList:
                try:
                    cateNoList.append(int(cate[0].getNo()))
                except:
                    pass
                for childCate in cate[1]:
                    try:
                        cateNoList.append(int(childCate.getNo()))
                    except:
                        pass
            return cateNoList

        result = []
        nowCateNoList = getCateNoList(nowCateList)
        newCateNoList = getCateNoList(newCateList)
        nowCateNoList.sort()
        newCateNoList.sort()
        for nowCateNo in nowCateNoList:
            try:
                newCateNoList.index(nowCateNo)
            except:
                result.append(nowCateNo)
        return result
    
    def getInsertedCateDtoList(newCateList):
        result = []
        for newCate in newCateList:
            if newCate[0].getNo()[:3] == 'new':
                parentNo = __setParentCategory(newCate[0])
            for newChildCate in newCate[1]:
                if newChildCate.getNo()[:3] == 'new':
                    if newCate[0].getNo()[:3] == 'new':
                        newChildCate.setUpper(parentNo)
                    result.append(newChildCate)
        return result
    
    def getChangedCateDtoList(nowCateList, newCateList, deletedNoList, insertedDtoList):
        result = []
        # nowCateList에서 deletedNoList 제외
        targetNowCateList = []
        for nowCate in nowCateList:
            try:
                deletedNoList.index(nowCate[0].getNo())
            except:
                targetNowCateList.append(nowCate[0])
            for nowChildCate in nowCate[1]:
                try:
                    deletedNoList.index(nowChildCate.getNo())
                except:
                    targetNowCateList.append(nowChildCate)
        # newCateList에서 insertedDtoList 제외
        targetNewCateList = []
        for newCate in newCateList:
            try:
                insertedDtoList.index(newCate[0])
            except:
                targetNewCateList.append(newCate[0])
            for newChildCate in newCate[1]:
                try:
                    insertedDtoList.index(newChildCate)
                except:
                    targetNewCateList.append(newChildCate)
        # 두 리스트에서 no가 같은 것끼리 비교하여 변경된 DTO 확인
        for nowCate in targetNowCateList:
            for newCate in targetNewCateList:
                try:
                    int(newCate.getNo())
                except:
                    continue
                if nowCate.getNo() == int(newCate.getNo()):
                    if nowCate.getName() == newCate.getName() and nowCate.getOrder() == int(newCate.getOrder()):
                        pass
                    else:
                        result.append(newCate)
        return result
    
    sqlList = []

    nowCateList = getCategoryList()
    newCateList = getCategoryListByCategoryList(categoryList)

    # 지워진 카테고리 확인
    deletedNoList = getDeleteCateNoList(nowCateList=nowCateList,newCateList=newCateList)
    for deletedNo in deletedNoList:
        sqlList.append(f'''DELETE FROM category WHERE c_no={deletedNo}''')
    
    # 추가된 카테고리 확인
    insertedDtoList = getInsertedCateDtoList(newCateList=newCateList)
    for insertedDto in insertedDtoList:
        sql = f'''INSERT INTO category(c_name,c_upper,c_order) VALUES("{insertedDto.getName()}",'''
        if insertedDto.getUpper() == None:
            sql += f'''NULL, {insertedDto.getOrder()})'''
        else:
            sql += f'''{insertedDto.getUpper()},{insertedDto.getOrder()})'''
        sqlList.append(sql)
    
    # 변경된 카테고리 확인
    changedDtoList = getChangedCateDtoList(nowCateList=nowCateList,newCateList=newCateList,deletedNoList=deletedNoList,insertedDtoList=insertedDtoList)
    for changedDto in changedDtoList:
        sql = f'''UPDATE category SET c_name="{changedDto.getName()}", '''
        if changedDto.getUpper() == None:
            sql += f'''c_upper=NULL, c_order={changedDto.getOrder()} WHERE c_no={changedDto.getNo()}'''
        else:
            sql += f'''c_upper={changedDto.getUpper()}, c_order={changedDto.getOrder()} WHERE c_no={changedDto.getNo()}'''
        sqlList.append(sql)

    result = db.setDatas(sqlList=sqlList)
    if result != 0:
        return True
    return False