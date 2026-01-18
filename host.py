from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response, flash
from dao import userDAO, categoryDAO, boardDAO, commentDAO
from service import store, validate

app = Flask(__name__)
app.config["SECRET_KEY"] = store.secret_key

@app.before_request
def validateCheck():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
    # Ddos 여부 판단
    if validate.checkDdos(clientUser):
        abort(403)
    
    # blackList에 있는지 확인
    elif validate.checkBlackList(clientUser):
        abort(403)
    
    # 세션 만료 확인
    elif validate.checkSessionTimeOver(clientUser): #
        if clientUser.getNo() != 0:
            resp = make_response(redirect(request.referrer or url_for('main')))
            
            # 쿠키 삭제
            resp.delete_cookie('sessionKey')
            
            # 메시지 생성
            flash(store.sessionTimeOut_msg)
            return resp
    

@app.route("/")
def main():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
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

@app.route("/login", methods=["POST"])
def loginHandler():
    resp = make_response(redirect(request.referrer or url_for('main')))
    try:
        # 데이터 가져오기
        email = request.form["email"]
        pw = request.form["pw"]
        sessionKey = userDAO.getSessionKeyByEmailAndPw(email=email,pw=pw,ip=request.remote_addr)
        
        # 쿠키 설정
        if sessionKey:
            resp.set_cookie(
                key='sessionKey',
                value=sessionKey,
                max_age=3600*store.sessionTime,
                secure=False,
                samesite='Lax',
                httponly=True)
    except:
        # 메시지 생성
        flash(store.failToLogin_msg)
    return resp

@app.route("/logout", methods=["POST"])
def logoutHandler():
    resp = make_response(redirect(request.referrer or url_for('main')))
    
    # 쿠키 삭제
    resp.delete_cookie('sessionKey')
    
    # 메시지 생성
    flash(store.logout_msg)
    return resp

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