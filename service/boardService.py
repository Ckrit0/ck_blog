from service import db, store
from dao import boardDAO
import os, shutil

def shortTitle(boardTitle):
    '''
    제목이 너무 길면 줄여주는 함수
    parameter: 글제목(String)
    return: 줄여진 글제목(String)
    '''
    if len(boardTitle) > 12:
        boardTitle = boardTitle[0:12] + '...'
    return boardTitle

def middleTitle(boardTitle):
    '''
    제목이 너무 길면 줄여주는 함수
    parameter: 글제목(String)
    return: 줄여진 글제목(String)
    '''
    if len(boardTitle) > 40:
        boardTitle = boardTitle[0:40] + '...'
    return boardTitle

def checkIsLiked(user, board):
    '''
    유저가 해당 게시글을 좋아요 했는지 확인
    parameter: 유저객체(userDTO), 글객체(boardDTO)
    return: 좋아요 했으면 True, 아니면 False
    '''
    sql = f''''''
    if user.getNo() == 0:
        sql = f'''SELECT count(*) FROM likes WHERE l_ip = "{user.getIp()}" AND b_no = {board.getNo()}'''
    else:
        sql = f'''SELECT count(*) FROM likes WHERE u_no = {user.getNo()} AND b_no = {board.getNo()}'''
    result = db.getData(sql=sql)[0][0]
    if result == 0:
        return False
    return True

def deleteUpload(bno):
    '''
    게시글 삭제시 업로드 된 이미지 삭제
    parameter: 글번호
    return: 성공 True, 실패 False
    '''
    contents = boardDAO.getBoardByBoardNo(bno=bno).getContents()
    splitContents = contents.split('<img src="')
    target = []
    if len(splitContents) == 1:
        return True
    for i in range(len(splitContents)):
        if i == 0:
            continue
        targetPath = splitContents[i].split('">')[0].split('/')
        targetName = targetPath[len(targetPath)-1]
        target.append(targetName)
    try:
        for name in target:
            nowPath = os.path.join(store.imageUploadDirectory, name)
            newPath = os.path.join(store.imageDeleteDirectory, name)
            shutil.move(nowPath, newPath)
    except Exception as e:
        print(e)
    return True
