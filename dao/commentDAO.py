from dto import commentDTO
from service import db, store, userService

#################################################################################################
###################################### Get Comment Object #######################################
#################################################################################################
def getCommentListByBoardNo(bno):
    '''
    글번호로 댓글객체 리스트 가져오기
    parameter: 글번호(int)
    return: 댓글객체 리스트(List)
    '''
    commentList = []
    sql = f'''\
        SELECT c.*, u.u_email, u.u_state, b.b_title, 0 FROM comment c \
        JOIN user u ON c.u_no = u.u_no \
        JOIN board b ON c.b_no = b.b_no \
        WHERE c.b_no={bno} AND c.co_upper IS NULL \
        ORDER BY c.co_no'''
    parentCommentList = db.getData(sql=sql)
    for parentComment in parentCommentList:
        pc = commentDTO.CommentDTO()
        pc.setCommentByDbResult(dbResult=parentComment)
        tempList = []
        sql = f'''\
            SELECT c.*, u.u_email, u.u_state, b.b_title, 0 FROM comment c \
            JOIN user u ON c.u_no = u.u_no \
            JOIN board b ON c.b_no = b.b_no \
            WHERE c.b_no={bno} AND c.co_upper = {pc.getNo()} \
            ORDER BY c.co_no'''
        childCommentList = db.getData(sql=sql)
        for childComment in childCommentList:
            cc = commentDTO.CommentDTO()
            cc.setCommentByDbResult(dbResult=childComment)
            tempList.append(cc)
        commentList.append([pc,tempList])
    return commentList

def getParentCommentListByBno(bno):
    '''
    글번호로 상위 댓글객체 리스트 가져오기
    parameter: 글번호(int)
    return: 댓글 데이터의 이중 리스트(List)
    '''
    sql = f'''\
        SELECT \
            c.*, u.u_email, u.u_state, b.b_title, \
            (SELECT count(*) FROM comment WHERE co_upper = c.co_no) \
        FROM comment c \
        JOIN user u ON c.u_no = u.u_no \
        JOIN board b ON c.b_no = b.b_no \
        WHERE c.b_no={bno} AND c.co_upper IS NULL \
        ORDER BY c.co_no'''
    f'''(SELECT count(*) FROM comment WHERE co_upper = c.cno)'''
    result = db.getData(sql=sql)
    for r in result:
        r[3] = userService.markingIp(ip=r[3])
        if r[7] == 1:
            r[4] = store.USER_MESSAGE[store.USER_RESULT_CODE['삭제된 댓글']]
        r[8] = userService.markingEmail(email=r[8],state=r[9])
    return result

def getChildCommentListByBnoAndCono(bno, cono):
    '''
    글번호와 상위댓글번호로 하위댓글객체 리스트 가져오기
    parameter: 글번호(int), 상위댓글번호(int)
    return: 댓글 데이터의 이중 리스트(List)
    '''
    sql = f'''\
        SELECT \
            c.*, u.u_email, u.u_state, b.b_title
        FROM comment c \
        JOIN user u ON c.u_no = u.u_no \
        JOIN board b ON c.b_no = b.b_no \
        WHERE c.b_no={bno} AND c.co_upper={cono} \
        ORDER BY c.co_no'''
    f'''(SELECT count(*) FROM comment WHERE co_upper = c.cno)'''
    result = db.getData(sql=sql)
    for r in result:
        r[3] = userService.markingIp(ip=r[3])
        if r[7] == 1:
            r[4] = store.USER_MESSAGE[store.USER_RESULT_CODE['삭제된 댓글']]
        r[8] = userService.markingEmail(email=r[8],state=r[9])
    return result



def getCommentCountByUserNo(uno):
    '''
    유저별 작성한 댓글 갯수 가져오기
    parameter: 유저번호(int)
    return: 작성한 댓글 갯수(int)
    '''
    sql = f'''SELECT count(*) FROM comment WHERE u_no = {uno} AND co_isdelete = 0'''
    result = db.getData(sql=sql)[0][0]
    return result

def getRecentlyCommentList(uno):
    '''
    유저별 작성한 최신댓글 목록 가져오기
    parameter: 유저번호(int)
    return: 댓글 목록 리스트([commentDTO,....])
    '''
    result = []
    sql = f'''\
        SELECT c.*, u.u_email, u.u_state, b.b_title, 0 FROM comment c \
        JOIN user u ON c.u_no = u.u_no \
        JOIN board b ON c.b_no = b.b_no \
        WHERE c.u_no = {uno} \
        ORDER BY c.co_no DESC LIMIT {store.PAGE_COUNT['유저']} OFFSET 0'''
    commentList = db.getData(sql=sql)
    for comment in commentList:
        c = commentDTO.CommentDTO()
        c.setCommentByDbResult(comment)
        result.append(c)
    return result

#################################################################################################
###################################### Set Comment Object #######################################
#################################################################################################
def setComment(comment):
    '''
    댓글 달기
    parameter: 댓글객체(commentDTO)
    return: 실패 True, 성공 False (bool)
    '''
    sql = f'''\
        INSERT INTO comment(b_no,u_no,co_ip,co_comment,co_upper) \
        VALUES(\
            {comment.getBoardNo()},\
            {comment.getUserNo()},\
            "{comment.getIp()}",\
            "{comment.getComment()}",\
            {comment.getUpper()}
        )'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True

'''
댓글 삭제 (co_isdelete를 1로 update)
parameter: 댓글번호(int)
return: 성공 True, 실패 False (bool)
'''
def deleteComment(cono):
    sql = f'''UPDATE comment SET co_isdelete = 1 WHERE co_no = {cono}'''
    result = db.setData(sql=sql)
    if result == 0:
        return False
    return True