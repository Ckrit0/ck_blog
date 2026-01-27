from dto import boardDTO
from service import db, store, boardService
import math

#################################################################################################
####################################### Get Board Object ########################################
#################################################################################################
def getTitleList_all(page):
    '''
    전체 글제목 목록 가져오기
    parameter: 페이지(int)
    return: 해당 페이지의 [글 번호(int), 제목(String), 조회수(int), 좋아요수(int)]의 리스트
    '''
    page = int(page)
    limit = store.PAGE_COUNT['메인']
    offset = limit * (page-1)
    sql = f'''SELECT b.b_no, b.b_title, \
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no) \
            FROM board b WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT {limit} OFFSET {offset}'''
    result = db.getData(sql=sql)
    for data in result:
        data[1] = boardService.middleTitle(data[1])
    return result

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

def getTitleList_cathgory(cno, page=1):
    '''
    카테고리별 글목록 가져오기
    parameter: 카테고리번호(cono), 페이지(int)
    return: 해당 페이지의 [글 번호(int), 제목(String), 조회수(int), 좋아요수(int)]의 리스트
    '''
    cno = int(cno)
    page = int(page)
    limit = store.PAGE_COUNT['카테고리']
    offset = limit * (page-1)
    sql = f'''SELECT b.b_no, b.b_title, \
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views v WHERE v.b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes l WHERE l.b_no=b.b_no) \
            FROM board b WHERE b.c_no={cno} AND b.b_isdelete=0 \
            ORDER BY b.b_no DESC LIMIT {limit} OFFSET {offset}'''
    result = db.getData(sql=sql)
    for titleData in result:
        titleData[1] = boardService.middleTitle(titleData[1])
    return result

def getPageList_category(cno):
    '''
    카테고리별 페이지 리스트 가져오기
    parameter: 카테고리번호(cono)
    return: 페이지 리스트(list)
    '''
    pageList = []
    sql = f'''SELECT count(*) FROM board WHERE c_no={cno} AND b_isdelete=0'''
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['카테고리'])
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
    page = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['카테고리']) + 1
    return page

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
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no) \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE b.b_no = {bno} AND b.b_isdelete=0'''
    result = db.getData(sql=sql)[0]
    board.setBoardByDbResult(dbResult=result)
    return board

def getRecentlyBoard():
    '''
    마지막 게시글 가져오기
    return: 마지막 글 객체(boardDTO)
    '''
    board = boardDTO.BoardDTO()
    sql = f'''
        SELECT b.*, u.u_email, u.u_state, \
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no) \
        FROM board b \
        JOIN user u \
        ON b.u_no = u.u_no \
        WHERE b.b_isdelete=0 \
        ORDER BY b.b_no DESC LIMIT 1'''
    result = db.getData(sql=sql)[0]
    board.setBoardByDbResult(dbResult=result)
    return board

def getBoardCountByUserNo(uno):
    '''
    유저별 작성한 글 갯수 가져오기
    parameter: 유저번호(int)
    return: 작성한 글 갯수(int)
    '''
    sql = f'''SELECT count(*) FROM board WHERE u_no = {uno} AND b_isdelete = 0'''
    result = db.getData(sql=sql)
    return result[0][0]

def getRecentlyBoardList(uno):
    '''
    유저별 작성한 최신글 목록 가져오기
    parameter: 유저번호(int)
    return: 글 목록 리스트([boardDTO,....])
    '''
    result = []
    sql = f'''
        SELECT b.*, u.u_email, u.u_state, \
            (SELECT count(DISTINCT u_no) + count(DISTINCT v_ip) FROM views WHERE b_no=b.b_no), \
            (SELECT count(DISTINCT u_no) + count(DISTINCT l_ip) FROM likes WHERE b_no=b.b_no) \
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



'''
이미지번호로 이미지객체 가져오기
parameter: 이미지번호(int)
return: 이미지객체
'''
def getImageByImageNo(ino):
    image = None
    sql = f''''''
    return image

#################################################################################################
####################################### Set Board Object ########################################
#################################################################################################

def setBoard(uno,cno,title,contents,ip):
    '''
    글 작성하기
    parameter: 글객체(boardDTO)
    return: 성공 True, 실패 False (bool)
    '''
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
    bContents = board.getContents()
    sql = f'''UPDATE board SET c_no={cno}, b_title="{bTitle}", b_contents="{bContents}" WHERE b_no={board.getNo()}'''
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

def deleteBoard(board):
    '''
    글 삭제하기 (b_isdelete를 1로 update)
    parameter: 글객체(boardDTO)
    return: 성공 True, 실패 False (bool)
    '''
    sql = f'''UPDATE board SET b_isdelete = 1 WHERE b_no = {board.getNo()}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
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

