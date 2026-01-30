from service import db, store, logger
from dao import boardDAO
import os, shutil, re

def shortTitle(boardTitle):
    '''
    제목이 너무 길면 줄여주는 함수
    parameter: 글제목(String)
    return: 줄여진 글제목(String)
    '''
    if len(boardTitle) > store.shortTitleCount:
        boardTitle = boardTitle[0:store.shortTitleCount] + '...'
    return boardTitle

def middleTitle(boardTitle):
    '''
    제목이 너무 길면 줄여주는 함수
    parameter: 글제목(String)
    return: 줄여진 글제목(String)
    '''
    if len(boardTitle) > store.middleTitleCount:
        boardTitle = boardTitle[0:store.middleTitleCount] + '...'
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
    parameter: 글번호(int)
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
        log = logger.Logger()
        log.setLog(store.LOG_NAME['시스템'],f"delete image error: {e}")
    return True

def shortContents(htmlContents):
    '''
    글 내용을 앞부분의 텍스트만 가져옴
    parameter: 태그가 포함된 전체 글(String)
    return: 태그가 사라지고 줄여진 글(String)
    '''
    # HTML 태그를 찾아 공백으로 대체
    clean_text = re.sub(r'<[^>]+>', ' ', htmlContents)
    # 연속된 공백을 하나의 공백으로 처리
    clean_text = re.sub(r"\s+", " ", clean_text)
    # 앞 뒤 공백 제거
    clean_text = clean_text.strip()
    # 지정된 글자수가 넘어가면 말줄임표
    if len(clean_text) > store.shortWordCount:
        clean_text = clean_text[0:store.shortWordCount] + '...'
    return clean_text