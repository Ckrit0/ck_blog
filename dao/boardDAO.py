from dto import boardDTO
from service import db

'''
글 작성하기
parameter: 글객체(boardDTO)
return: 
'''
def setBoard(board):
    pass

'''
이미지 저장하기
parameter: 글객체(boardDTO), 이미지객체(타입미정)
return: 
'''
def setImage(board,image):
    pass

'''
조회 설정하기.(최근 본 글 목록에서 볼 수 있도록 모두 저장)
parameter: user객체(userDTO)
return: 
'''
def setView(user):
    pass

'''
좋아요 설정하기.(유저번호 또는 IP가 겹치면 토글)
parameter: user객체(userDTO)
return: 
'''
def setLike(user):
    pass

'''
글 수정하기
parameter: 글객체(boardDTO)
return: 
'''
def updateBoard(board):
    pass

'''
전체 글목록 가져오기
parameter: 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_all(category, page):
    boardNoAndTitleList = []
    return boardNoAndTitleList

'''
카테고리별 글목록 가져오기
parameter: 카테고리객체(categoryDTO), 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_cathgory(category, page):
    boardNoAndTitleList = []
    return boardNoAndTitleList

'''
글 앞뒤 글목록 가져오기
parameter: 글객체(boardDTO), 페이지(int)
return: 해당 페이지의 [글 번호(int), 제목(String)]의 리스트
'''
def getTitleList_board(board, page):
    boardNoAndTitleList = []
    return boardNoAndTitleList

'''
글번호로 글 가져오기
parameter: 글번호(int)
return: 글 객체(boardDTO)
'''
def getBoardByBoardNo(bno):
    board = boardDTO.BoardDTO()
    return board

'''
이미지번호로 이미지객체 가져오기
parameter: 이미지번호(int)
return: 이미지객체
'''
def getImageByImageNo(ino):
    image = None
    return image

'''
글번호로 조회수 가져오기 (겹치는 이메일/아이피는 1회만)
parameter: 글번호(int)
return: 조회수(int)
'''
def getViewByBoardNo(bno):
    view = 0
    return view

'''
글 번호로 좋아요수 가져오기
parameter: 글번호(int)
return: 좋아요수(int)
'''
def getLikeByBoardNo(bno):
    like = 0
    return like

'''
글 삭제하기 (b_isdelete를 1로 update)
parameter: 글객체(boardDTO)
return: 
'''
def deleteBoard(board):
    pass

'''
이미지번호로 이미지 삭제하기
parameter: 이미지번호(int)
return: 
'''
def deleteImage(ino):
    pass
