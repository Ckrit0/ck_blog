from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response, flash
from dao import userDAO, categoryDAO, boardDAO, commentDAO
from service import store, validate

app = Flask(__name__)
app.config["SECRET_KEY"] = store.secret_key

def getTemplateData(req):
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=req.cookies.get('sessionKey'),ip=req.remote_addr)
    categoryList = categoryDAO.getCategoryList()
    recentlyTitleList = boardDAO.getRecentlyTitleList_user(clientUser)
    return clientUser, categoryList, recentlyTitleList

##########################
##### validate와 메인 #####
##########################

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
            flash(store.USER_MESSAGE['세션만료'])
            return resp
    

@app.route("/")
def main():
    # 템플릿 정보 가져오기
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    
    # 메인페이지 데이터 가져오기
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

##########################
######## 유저 관련 ########
##########################

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
        # alert 메시지 생성
        flash(store.USER_MESSAGE['로그인실패'])
    return resp

@app.route("/logout", methods=["POST"])
def logoutHandler():
    resp = make_response(redirect(request.referrer or url_for('main')))
    
    # 쿠키 삭제
    resp.delete_cookie('sessionKey')
    
    # alert 메시지 생성
    flash(store.USER_MESSAGE['로그아웃'])
    return resp

@app.route("/join")
def joinPage():
    # 템플릿 정보 가져오기
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    
    # 이미 로그인 되어있는 경우
    if clientUser.getNo() != 0:
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE['기로그인'])
        return resp
    
    # 뷰 설정
    userDAO.setView(clientUser)

    return render_template('join.html',
        clientUser = clientUser,
        categoryList = categoryList,
        recentlyTitleList = recentlyTitleList
    )

@app.route("/join", methods=["POST"])
def joinHandler():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
    resp = make_response(redirect(url_for('main')))
    
    # 이미 로그인 되어있는 경우
    if clientUser.getNo() != 0:
        flash(store.USER_MESSAGE['기로그인'])
        return resp
    
    # form data 가져오기
    email = request.form["joinEmail"]
    pw = request.form["joinPw"]
    confirm = request.form["joinConfirm"]
    verify = request.form["joinVerify"]

    result = userDAO.setUser(email=email, pw=pw, confirm=confirm, verify=verify)
    flash(store.getJoinResult(result))
    return resp

@app.route("/checkMail", methods=["POST"])
def checkMailHandler():
    email = request.json["joinEmail"]
    sameEmailUsers = userDAO.getUserByEmailAddress(email)
    return jsonify(sameEmailUsers)

@app.route("/sendMail", methods=["POST"])
def sendMailHandler():
    email = request.json["joinEmail"]
    result = userDAO.sendMail(email=email)
    return jsonify(result)

@app.route("/matchVerify", methods=["POST"])
def matchVerifyHandler():
    email = request.json["joinEmail"]
    verify = request.json["joinVerify"]
    result = userDAO.matchVerify(email=email, code=verify)
    return jsonify(result)

@app.route("/user/<userNo>")
def userPage(userNo):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    # 유저정보
    targetUser = userDAO.getUserByUserNo(uno=userNo)
    if targetUser.getState() == 0:
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash("유저를 찾을 수 없습니다.")
        return resp
    # 마지막 세션시간
    targetUserLastSessionTime = userDAO.getSessionTimeByUserNo(uno=targetUser.getNo()).strftime("%Y-%m-%d")
    # 작성한 글 갯수
    targetUserBoardCount = boardDAO.getBoardCountByUserNo(uno=targetUser.getNo())
    # 작성한 댓글 갯수
    targetUserCommentCount = commentDAO.getCommentCountByUserNo(uno=targetUser.getNo())
    # 작성한 최근글 목록
    targetUserBoardList = boardDAO.getRecentlyBoardList(uno=targetUser.getNo())
    # 작성한 최근댓글 목록
    targetUserCommentList = commentDAO.getRecentlyCommentList(uno=targetUser.getNo())

    return render_template('user.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        targetUser=targetUser,
        targetUserLastSessionTime=targetUserLastSessionTime,
        targetUserBoardCount=targetUserBoardCount,
        targetUserCommentCount=targetUserCommentCount,
        targetUserBoardList=targetUserBoardList,
        targetUserCommentList=targetUserCommentList
    )
    
@app.route("/changePw", methods=["POST"])
def changePwHandler():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
    # form data 가져오기
    userNowPw = request.json["userNowPw"]
    userNewPw = request.json["userNewPw"]
    userNewConfirm = request.json["userNewConfirm"]

    result = userDAO.updateUserPassword(user=clientUser, nowPw=userNowPw, newPw=userNewPw, newConfirm=userNewConfirm)
    return jsonify(result)

@app.route("/getVerify", methods=["POST"])
def getVerifyHandler():
    email = request.json["userEmail"]
    verify = request.json["userVerify"]
    result = userDAO.matchVerify(email=email, code=verify)
    userNo = userDAO.getUserByEmailAddress(email=email)[0][0]
    if result == 0:
        dbResult = userDAO.updateUserState(uno=userNo,u_state=store.USER_STATE_CODE['인증'])
        if dbResult == 0:
            return jsonify(store.USER_RESULT_CODE['실패-unknown'])
    return jsonify(result)

@app.route("/leave", methods=["POST"])
def leaveHandler():
    email = request.json["userEmail"]
    pw = request.json["userPw"]
    userNo = userDAO.getUserByEmailAddress(email=email)[0][0]
    result = userDAO.leaveUser(uno=userNo, pw=pw)
    resp = jsonify(result)
    if result == store.USER_RESULT_CODE['회원 탈퇴 성공']:
        # 쿠키 삭제
        resp.delete_cookie('sessionKey')
    return resp

@app.route("/find")
def findPage():
    return render_template('find.html')

##########################
######### 글 관련 #########
##########################

@app.route("/contents/<contentsNo>")
def contentsPage(contentsNo):
    return render_template('contetns.html', contentsNo=contentsNo)

##########################
######## 검색 관련 ########
##########################

@app.route("/category/<categoryNo>")
def categoryPage(categoryNo):
    return render_template('category.html', categoryNo=categoryNo)

@app.route("/search/<keyword>")
def searchPage(keyword):
    return render_template('search.html', keyword=keyword)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )