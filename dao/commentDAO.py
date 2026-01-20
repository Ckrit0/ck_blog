from dto import commentDTO
from service import db
from service import store
import math

'''
댓글 달기
parameter: 댓글객체(commentDTO)
return: 
'''
def setComment(comment):
    pass

'''
댓글 수정
parameter: 댓글객체(commentDTO)
return: 
'''
def updateComment(comment):
    pass

'''
글번호로 댓글객체 리스트 가져오기
parameter: 글번호(int)
return: 댓글객체 리스트(List)
'''
def getCommentListByBoardNo(bno):
    commentList = []
    sql = f'''SELECT * from comment WHERE b_no={bno} AND co_upper IS NULL ORDER BY co_no DESC LIMIT {store.PAGE_COUNT['댓글']} OFFSET 0'''
    parentCommentList = db.getData(sql=sql)
    for parentComment in parentCommentList:
        pc = commentDTO.CommentDTO()
        pc.setCommentAll(
            parentComment[0],
            parentComment[1],
            parentComment[2],
            parentComment[3],
            parentComment[4],
            parentComment[5],
            parentComment[6],
            parentComment[7]
        )
        tempList = []
        sql = f'''SELECT * from comment WHERE b_no={bno} AND co_upper={pc.getNo()} ORDER BY co_no LIMIT {store.PAGE_COUNT['댓글']} OFFSET 0'''
        childCommentList = db.getData(sql=sql)
        for childComment in childCommentList:
            cc = commentDTO.CommentDTO()
            cc.setCommentAll(
                childComment[0],
                childComment[1],
                childComment[2],
                childComment[3],
                childComment[4],
                childComment[5],
                childComment[6],
                childComment[7]
            )
            tempList.append(cc)
        commentList.append([pc,tempList])
    return commentList

'''
해당 글에 작성된 댓글의 페이지 리스트 가져오기
return: 댓글 페이지 리스트(list)
'''
def getCommentPageListByBoardNo(bno):
    pageList = []
    sql = f'SELECT count(*) FROM comment WHERE b_no = {bno} AND co_upper IS NULL'
    result = math.ceil(db.getData(sql=sql)[0][0]/store.PAGE_COUNT['댓글'])
    for i in range(result):
        pageList.append(i+1)
    return pageList

'''
댓글 삭제 (co_isdelete를 1로 update)
parameter: 댓글객체(commentDTO)
return: 
'''
def deleteComment(comment):
    pass