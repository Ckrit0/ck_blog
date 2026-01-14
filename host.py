from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from dao import userDAO
from dao import categoryDAO
from dao import boardDAO
from dao import commentDAO
from service import store
from service import validate

app = Flask(__name__)

@app.before_request
def validateCheck():
    clientUser = userDAO.getUserBySessionKey(sessionKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    if validate.checkDdos(clientUser):
        abort(403)
    elif validate.checkBlackList(clientUser):
        abort(403)

@app.route("/")
def main():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(sessionKey=request.cookies.get('sessionKey'),ip=request.remote_addr)

    # 데이터 가져오기
    categoryList = categoryDAO.getCategoryList()
    recentlyTitleList = boardDAO.getRecentlyTitleList_user(clientUser)
    titleList = boardDAO.getTitleList_all(1)
    pageList = boardDAO.getPageList_all()
    recentlyboard = boardDAO.getRecentlyBoard()
    commentList = commentDAO.getCommentListByBoardNo(recentlyboard.getNo())
    commentPageList = commentDAO.getCommentPageListByBoardNo(recentlyboard.getNo())
    
    # 뷰 설정하기
    boardDAO.setView(user=clientUser,board=recentlyboard)
    
    return render_template('main.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        titleList=titleList,
        pageList=pageList,
        recentlyboard=recentlyboard,
        commentList=commentList,
        commentPageList=commentPageList
    )

@app.route("/category/<categoryNo>")
def categoryPage(categoryNo):
    return render_template('category.html', categoryNo=categoryNo)

@app.route("/contents/<contentsNo>")
def contentsPage(contentsNo):
    return render_template('contetns.html', contentsNo=contentsNo)

@app.route("/search/<keyword>")
def searchPage(keyword):
    return render_template('search.html', keyword=keyword)

@app.route("/join")
def joinPage():
    return render_template('join.html')

@app.route("/find")
def findPage():
    return render_template('find.html')

@app.route("/user/<userNo>")
def userPage(userNo):
    return render_template('user.html', userNo=userNo)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )