from dto import boardDTO
from service import db
from service import store
import math

'''
글 작성하기
parameter: 글객체(boardDTO)
return: 
'''
def setBoard(board):
    uNo = board.getUserNo()
    cNo = board.getCategoryNo()
    bTitle = board.getTitle()
    bContents = board.getContents()
    sql=f'INSERT INTO board(u_no,c_no,b_title,b_contents) VALUES({uNo},{cNo},"{bTitle}","{bContents}")'
    result = db.setData(sql=sql)
    return result

'''
이미지 저장하기
parameter: 글객체(boardDTO), 이미지객체(타입미정)
return: 
'''
def setImage(board,image):
    sql=f''

'''
조회 설정하기.(최근 본 글 목록에서 볼 수 있도록 모두 저장)
parameter: user객체(userDTO), 글객체(boardDTO)
return: 실패 0, 성공 1 (int)
'''
def setView(user, board):
    sql=f'INSERT INTO views(b_no,u_no,v_ip) VALUES({board.getNo()},{user.getNo()},"{user.getIp()}")'
    result = db.setData(sql=sql)
    return result

'''
좋아요 설정하기.(유저번호 또는 IP가 겹치면 토글)
parameter: user객체(userDTO)
return: 
'''
def setLike(user):
    sql=f''

'''
글 수정하기
parameter: 글객체(boardDTO)
return: 
'''
def updateBoard(board):
    sql=f''

'''
전체 글목록 가져오기
parameter: 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_all(page):
    limit = store.PAGE_COUNT['메인통합']
    offset = limit * (page-1)
    sql=f'SELECT b_no,b_title FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT {limit} OFFSET {offset}'
    result = db.getData(sql=sql)
    return result

'''
전체 페이지 리스트 가져오기
return: 페이지 리스트(list)
'''
def getPageList_all():
    pageList = []
    sql='SELECT count(*) FROM board WHERE b_isdelete=0'
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['메인통합'])
    for i in range(result):
        pageList.append(i+1)
    return pageList

'''
유저별 마지막 읽은 글목록 가져오기
parameter: 유저객체(userDTO)
return: 마지막 본 글 제목 리스트([[글번호(int),글제목(string)]...])
'''
def getRecentlyTitleList_user(user):
    limit = store.PAGE_COUNT['유저별']
    sql=''
    uno = user.getNo()
    if uno == None:
        sql=f'SELECT b.b_no, b.b_title FROM board b\
            JOIN (SELECT DISTINCT b_no FROM views WHERE v_ip = "{user.getIp()}" AND b_no != 0 ORDER BY v_date DESC LIMIT {limit}) v\
            ON b.b_no = v.b_no'
    else:
        sql=f'SELECT b.b_no, b.b_title FROM board b\
            JOIN (SELECT DISTINCT b_no FROM views WHERE u_no = {uno} AND b_no != 0 ORDER BY v_date DESC LIMIT {limit}) v\
            ON b.b_no = v.b_no'
    result = db.getData(sql=sql)
    return result

'''
카테고리별 글목록 가져오기
parameter: 카테고리객체(categoryDTO), 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_cathgory(category, page):
    boardNoAndTitleList = []
    sql=f''
    return boardNoAndTitleList

'''
카테고리 내에서 해당 글의 앞뒤 글목록 가져오기
parameter: 글객체(boardDTO), 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_board(board, page):
    boardNoAndTitleList = []
    sql=f''
    return boardNoAndTitleList

'''
글번호로 글 가져오기
parameter: 글번호(int)
return: 글 객체(boardDTO)
'''
def getBoardByBoardNo(bno):
    board = boardDTO.BoardDTO()
    sql=f''
    return board

'''
마지막 게시글 가져오기
return: 마지막 글 객체(boardDTO)
'''
def getRecentlyBoard():
    board = boardDTO.BoardDTO()
    sql=f'SELECT * FROM board WHERE b_isdelete=0 ORDER BY b_no DESC LIMIT 1 OFFSET 0'
    result = db.getData(sql=sql)
    board.setBoard(
        no=result[0][0],
        uno=result[0][1],
        cno=result[0][2],
        date=result[0][3],
        title=result[0][4],
        content=result[0][5]
    )
    view = getViewByBoardNo(board.getNo())
    board.setView(view=view)
    like = getLikeByBoardNo(board.getNo())
    board.setLike(like=like)
    return board

'''
이미지번호로 이미지객체 가져오기
parameter: 이미지번호(int)
return: 이미지객체
'''
def getImageByImageNo(ino):
    image = None
    sql=f''
    return image

'''
글번호로 조회수 가져오기 (겹치는 이메일/아이피는 1회만)
parameter: 글번호(int)
return: 조회수(int)
'''
def getViewByBoardNo(bno):
    sql=f'SELECT count(DISTINCT v_ip) FROM views WHERE b_no={bno}'
    result = db.getData(sql=sql)
    view = result[0][0]
    return view

'''
글 번호로 좋아요수 가져오기
parameter: 글번호(int)
return: 좋아요수(int)
'''
def getLikeByBoardNo(bno):
    sql=f'SELECT count(DISTINCT l_ip) FROM likes WHERE b_no={bno}'
    result = db.getData(sql=sql)
    like = result[0][0]
    return like

'''
글 삭제하기 (b_isdelete를 1로 update)
parameter: 글객체(boardDTO)
return: 
'''
def deleteBoard(board):
    sql=f''

'''
이미지번호로 이미지 삭제하기
parameter: 이미지번호(int)
return: 
'''
def deleteImage(ino):
    sql=f''

'''
유저별 작성한 글 갯수 가져오기
parameter: 유저번호(int)
return: 작성한 글 갯수(int)
'''
def getBoardCountByUserNo(uno):
    sql=f'SELECT count(*) FROM board WHERE u_no = {uno} AND b_isdelete = 0'
    result = db.getData(sql=sql)
    return result[0][0]

'''
유저별 작성한 최신글 목록 가져오기
parameter: 유저번호(int)
return: 글 목록 리스트([boardDTO,....])
'''
def getRecentlyBoardList(uno):
    result = []
    sql=f'''SELECT * FROM board WHERE u_no = {uno} AND b_isdelete = 0 ORDER BY b_no DESC LIMIT {store.PAGE_COUNT['유저별']} OFFSET 0'''
    boardList = db.getData(sql=sql)
    for board in boardList:
        b = boardDTO.BoardDTO()
        b.setBoard(
            no=board[0],
            uno=board[1],
            cno=board[2],
            date=board[3],
            title=board[4],
            content=board[5],
            isDelete=board[6]
        )
        result.append(b)
    return result