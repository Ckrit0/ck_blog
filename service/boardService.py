from service import db

def shortTitle(boardTitle):
    '''
    제목이 너무 길면 줄여주는 함수
    parameter: 글제목(String)
    return: 줄여진 글제목(String)
    '''
    if len(boardTitle) > 15:
        boardTitle = boardTitle[0:15] + '...'
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