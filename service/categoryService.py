
def getCategoryNameByCnoInCategoryList(cList,cno):
    '''
    카테고리 리스트에서 cno의 이름 찾기
    parameter: cList([categoryDTO,...]), cno (int)
    return: 결과가 있으면 카테고리명, 없으면 공란
    '''
    for categoryList in cList:
        for category in categoryList[1]:
            if category.getNo() == cno:
                return category.getName()
    return ""