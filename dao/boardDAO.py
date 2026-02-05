from dto import boardDTO
from service import db, store, boardService
import math

#################################################################################################
####################################### Get Board Object ########################################
#################################################################################################

########### 글 관련 - 공지 ############
def getNotice():
    '''
    공지사항 가져오기
    boardNo는 0으로 고정, isdelete를 1로 만들어서 다른곳에서 글 가져오는 것을 피하기
    '''
    sql = f'''SELECT b_contents from board where b_no = 0'''
    notice = db.getData(sql=sql)[0][0]    
    return notice

########### 글 관련 - 전체 ############
def getTitleList_all(page):
    '''
    전체 글제목 목록 가져오기
    parameter: 페이지(int)
    return: 해당 페이지의 [글 번호(int), 제목(String), 조회수(int), 좋아요수(int)]의 리스트
    '''
    page = int(page)
    if page == 0:
        return []
    limit = store.PAGE_COUNT['메인']
    offset = limit * (page-1)
    sql = f'''SELECT b.b_no, b.b_title, \
            (SELECT count(*) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
            (SELECT count(*) FROM comment WHERE b_no=b.b_no), \
            c.c_name
            FROM board b JOIN category c ON b.c_no = c.c_no \
            WHERE b.b_isdelete=0 ORDER BY b.b_date DESC LIMIT {limit} OFFSET {offset}'''
    result = db.getData(sql=sql)
    for data in result:
        data[1] = boardService.middleTitle(data[1])
    return result

def getBoardByBoardNo(bno):
    '''
    글번호로 글 가져오기
    parameter: 글번호(int)
    return: 글 객체(boardDTO)
    '''
    board = boardDTO.BoardDTO()
    sql = f'''
        SELECT \
            b.*, u.u_email, u.u_state, \
            (SELECT count(*) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
            (SELECT count(*) FROM comment WHERE b_no=b.b_no) \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE b.b_no = {bno}'''
    result = db.getData(sql=sql)[0]
    board.setBoardByDbResult(dbResult=result)
    return board

def getLikeByBoardNo(bno):
    '''
    글번호로 좋아요 수 가져오기
    parameter: 글번호(int)
    return: 좋아요 수(int)
    '''
    sql = f'''
        SELECT \
            (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no) \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE b.b_no = {bno}'''
    result = db.getData(sql=sql)[0][0]
    return result

def getSearchResult(keywordList, page):
    '''
    검색어로 검색 결과를 찾아옴
    parameter: 검색단어 리스트(list)
    return: 검색된 글객체 리스트([boardDTO,...])
    '''
    page = int(page)
    limit = store.PAGE_COUNT['검색']
    offset = limit * (page-1)
    sql = f'''\
        SELECT b.*, u.u_email, u.u_state, \
        (SELECT count(*) FROM views v WHERE v.b_no=b.b_no), \
        (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
        (SELECT count(*) FROM comment WHERE b_no=b.b_no), \
        ('''
    for keyword in keywordList:
        sql += f'''\
            ((b.b_title LIKE "%{keyword[0]}%")*{keyword[1]}) + ((b.b_contents LIKE "%{keyword[0]}%")*{keyword[1]}) +'''
    sql = sql[:-1]
    sql += f'''\
        ) AS score \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE
            b.b_isdelete=0 AND ('''
    for keyword in keywordList:
        sql += f'''\
            b.b_title LIKE "%{keyword[0]}%" OR b.b_contents LIKE "%{keyword[0]}%" OR'''
    sql = sql[:-2]
    sql += f'''\
        ) ORDER BY score DESC LIMIT {limit} OFFSET {offset}'''
    dbResult = db.getData(sql=sql)
    searchBoardList = []
    for data in dbResult:
        board = boardDTO.BoardDTO()
        board.setBoardByDbResult(dbResult=data)
        searchBoardList.append(board)
    return searchBoardList

########### 글 관련 - 카테고리 ############
def getTitleList_cathgory(cno, page=1):
    '''
    카테고리별 글목록 가져오기
    parameter: 카테고리번호(cono), 페이지(int)
    return: 해당 페이지의 [글 번호(int), 제목(String), 조회수(int), 좋아요수(int), 댓글갯수(int)]의 리스트
    '''
    cno = int(cno)
    page = int(page)
    if page == 0:
        return []
    limit = store.PAGE_COUNT['카테고리']
    offset = limit * (page-1)
    sql = f'''SELECT b.b_no, b.b_title, \
            (SELECT count(*) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
            (SELECT count(*) FROM comment WHERE b_no=b.b_no) \
            FROM board b WHERE b.c_no={cno} AND b.b_isdelete=0 \
            ORDER BY b.b_no DESC LIMIT {limit} OFFSET {offset}'''
    result = db.getData(sql=sql)
    for titleData in result:
        titleData[1] = boardService.middleTitle(titleData[1])
    return result

########### 글 관련 - 유저 ############
def getBoardCountByUserNo(uno):
    '''
    유저별 작성한 글 갯수 가져오기
    parameter: 유저번호(int)
    return: 작성한 글 갯수(int)
    '''
    sql = f'''SELECT count(*) FROM board WHERE u_no = {uno} AND b_isdelete = 0'''
    result = db.getData(sql=sql)
    return result[0][0]

def getRecentlyBoardNoByUserNo(uno):
    '''
    해당 유저의 마지막 게시글 가져오기
    return: 마지막 글 번호(int)
    '''
    sql = f'''SELECT b_no FROM board WHERE b_isdelete=0 AND u_no = {uno} ORDER BY b_no DESC LIMIT 1'''
    result = db.getData(sql=sql)[0][0]
    return result

def getRecentlyBoardList(uno):
    '''
    유저별 작성한 최신글 목록 가져오기
    parameter: 유저번호(int)
    return: 글 목록 리스트([boardDTO,....])
    '''
    result = []
    sql = f'''
        SELECT b.*, u.u_email, u.u_state, \
            (SELECT count(*) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT CASE WHEN u_no != 0 THEN u_no END) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no), \
            (SELECT count(*) FROM comment WHERE b_no=b.b_no) \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE b.u_no = {uno} AND b.b_isdelete = 0 \
        ORDER BY b_no DESC LIMIT {store.PAGE_COUNT['유저']}'''
    boardList = db.getData(sql=sql)
    for b in boardList:
        board = boardDTO.BoardDTO()
        board.setBoardByDbResult(dbResult=b)
        result.append(board)
    return result

######### 페이징 관련 ###########
def getPageList_all():
    '''
    전체 페이지 리스트 가져오기
    return: 페이지 리스트(list)
    '''
    pageList = []
    sql = f'''SELECT count(*) FROM board WHERE b_isdelete=0'''
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['메인'])
    for i in range(result):
        pageList.append(i+1)
    return pageList

def getPageList_search(keywordList):
    '''
    검색화면 페이지 리스트 가져오기
    parameter: 키워드리스트(list)
    return: 페이지 리스트(list)
    '''
    pageList = []
    sql = f'''SELECT count(*) FROM board \
        WHERE \
            b_isdelete=0 AND \
            ('''
    for keyword in keywordList:
        sql += f'''\
            b_title LIKE "%{keyword[0]}%" OR b_contents LIKE "%{keyword[0]}%" OR'''
    sql = sql[:-2] + ')'
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['검색'])
    for i in range(result):
        pageList.append(i+1)
    return pageList

def getPageOfCategory(board):
    '''
    카테고리 내에서 해당 글의 페이지 번호 가져오기
    parameter: 글객체(boardDTO)
    return: 해당 글이 속한 페이지 번호(int)
    '''
    sql = f'''SELECT count(*) FROM board WHERE c_no={board.getCategoryNo()} AND b_isdelete=0 AND b_no > {board.getNo()}'''
    page = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['카테고리'])
    return page




#################################################################################################
####################################### Set Board Object ########################################
#################################################################################################

def setNotice(notice):
    '''
    공지사항 수정하기
    return: 성공 True, 실패 False (bool)
    '''
    sql = f'''UPDATE board SET b_contents="{notice}" WHERE b_no=0'''
    result = db.setData(sql=sql)
    if result != 0:
        return True
    return False

def setBoard(uno,cno,title,contents,ip):
    '''
    글 작성하기
    parameter: 글객체(boardDTO)
    return: 성공 True, 실패 False (bool)
    '''
    if title.strip() == '':
        title = 'untitled'
    contents = contents.replace('"','\\"')
    sql = f'''INSERT INTO board(u_no,c_no,b_title,b_contents,b_ip) VALUES({uno},{cno},"{title}","{contents}","{ip}")'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True

def updateBoard(board):
    '''
    글 수정하기
    parameter: 글객체(boardDTO)
    return: 성공 True, 실패 False (bool)
    '''
    cno = board.getCategoryNo()
    bTitle = board.getTitle()
    bContents = board.getContents().replace('"','\\"')
    bip = board.getIp()
    sql = f'''UPDATE board SET c_no={cno}, b_title="{bTitle}", b_contents="{bContents}", b_ip="{bip}" WHERE b_no={board.getNo()}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True

def changeCategory(board, newCno):
    '''
    글 카테고리 변경하기
    parameter: 글객체(boardDTO), 새로운 카테고리번호(int)
    return: 성공 True, 실패 False (bool)
    '''
    sql = f'''UPDATE board SET c_no={newCno} WHERE b_no={board.getNo()}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True

def deleteBoard(bno):
    '''
    글 삭제하기 (b_isdelete를 1로 update)
    parameter: 글번호(int)
    return: 성공 True, 실패 False (bool)
    '''
    sql = f'''UPDATE board SET b_isdelete = 1 WHERE b_no = {bno}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    boardService.deleteUpload(bno=bno)
    return True

def setLike(user, board):
    '''
    좋아요 설정하기.
    parameter: user객체(userDTO), 글객체(boardDTO)
    return: 성공 True, 실패 False (bool)
    '''
    sql = f'''\
        INSERT INTO likes (b_no, u_no, l_ip) \
        SELECT {board.getNo()}, {user.getNo()}, "{user.getIp()}" FROM DUAL \
        WHERE NOT EXISTS \
        (SELECT 1 FROM likes WHERE b_no = {board.getNo()} AND (u_no = {user.getNo()} OR l_ip = "{user.getIp()}"));'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True


'''
이미지 저장하기
parameter: 글객체(boardDTO), 이미지객체(타입미정)
return: 
'''
def setImage(board,image):
    sql = f''''''

'''
이미지번호로 이미지 삭제하기
parameter: 이미지번호(int)
return: 
'''
def deleteImage(ino):
    sql = f''''''

