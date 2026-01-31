from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response, flash
from dao import userDAO, categoryDAO, boardDAO, commentDAO
from service import store, validate, logger, userService, boardService, categoryService, serachService
import os, datetime
from werkzeug.utils import secure_filename

###########################
##### Flask 기본 설정 #####
###########################
app = Flask(__name__)
app.config["SECRET_KEY"] = store.secret_key
app.config["UPLOAD_FOLDER"] = store.imageUploadDirectory
app.config['MAX_CONTENT_LENGTH'] = store.imageSize


################################
##### 메인 페이지, Service #####
################################
def getTemplateData(req):
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=req.cookies.get('sessionKey'),ip=req.remote_addr)
    categoryList = categoryDAO.getCategoryList()
    recentlyTitleList = userDAO.getRecentlyTitleList_user(clientUser)
    return clientUser, categoryList, recentlyTitleList

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
    pageList = boardDAO.getPageList_all()
    
    # 공지사항 가져오기. 현재 DB 연결 없이 강제로 보냄
    notice = [
        '안녕하세요 어차피 블로그를 운영할 계획이면 내가 만들자고 시작한 블로그입니다.',
        '해당 블로그의 전체 코드는 깃허브(https://github.com/Ckrit0/ck_blog)에서 확인이 가능합니다.',
        '서버의 정기 재부팅 시각은 월요일 오전 4시입니다. 일시적으로 접속이 불가능할 수 있습니다.',
        '현재는 제작중이라 서버가 자주 불안정할 예정입니다.',
        '아직 도메인도 없습니다.',
        '이 글도 DB랑 연결 안하고 그냥 디자인 잡기 위해 생으로 입력한 글입니다.',
        '대충 이정도 분량으로 디자인을 잡으면 될 것 같습니다.',
        '기타 문의사항은 제작자(ckrit3@gmail.com)으로 부탁드립니다.',
        '감사합니다.'
    ]
    
    # 뷰 설정하기
    userDAO.setView(user=clientUser, url=request.path)
    
    return render_template('main.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        notice=notice,
        pageList=pageList
    )

#############################
######## 메인 핸들러 ########
#############################

@app.route("/getTitleListOnBoardByPage/<page>", methods=["POST"])
def getTitleListOnMainByPageHandler(page):
    titleList = boardDAO.getTitleList_all(page=page)
    return jsonify(titleList)

#############################
######## 유저 페이지 ########
#############################

@app.route("/join")
def joinPage():
    # 템플릿 정보 가져오기
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    
    # 이미 로그인 되어있는 경우
    if clientUser.getNo() != 0:
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE['기로그인'])
        return resp
    
    # 뷰 설정하기
    userDAO.setView(user=clientUser,url=request.path)

    return render_template('join.html',
        clientUser = clientUser,
        categoryList = categoryList,
        recentlyTitleList = recentlyTitleList
    )

@app.route("/user/<userNo>")
def userPage(userNo):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)

    # 대상 유저정보
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

    # 뷰 설정하기
    userDAO.setView(user=clientUser,url=request.path)

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


@app.route("/find")
def findPage():
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    # 뷰 설정하기
    userDAO.setView(user=clientUser,url=request.path)
    return render_template('find.html')

#############################
######## 유저 핸들러 ########
#############################

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
    except Exception as e:
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']])
        log = logger.Logger()
        log.setLog(store.LOG_NAME['유저'],f"login error: {e}")
    return resp

@app.route("/logout", methods=["POST"])
def logoutHandler():
    resp = make_response(redirect(url_for('main')))
    
    # 쿠키 삭제
    resp.delete_cookie('sessionKey')
    
    # alert 메시지 생성
    flash(store.USER_MESSAGE[store.USER_RESULT_CODE['로그아웃']])
    return resp

@app.route("/join", methods=["POST"])
def joinHandler():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
    resp = make_response(redirect(url_for('main')))
    
    # 이미 로그인 되어있는 경우
    if clientUser.getNo() != 0:
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['기로그인']])
        return resp
    
    # form data 가져오기
    email = request.form["joinEmail"]
    pw = request.form["joinPw"]
    confirm = request.form["joinConfirm"]
    verify = request.form["joinVerify"]

    result = userDAO.setUser(email=email, pw=pw, confirm=confirm, verify=verify)
    flash(store.getUserResult(result))
    return resp

@app.route("/checkMail", methods=["POST"])
def checkMailHandler():
    email = request.json["joinEmail"]
    sameEmailUsers = userDAO.getUserByEmailAddress(email)
    return jsonify(sameEmailUsers)

@app.route("/sendMail", methods=["POST"])
def sendMailHandler():
    email = request.json["joinEmail"]
    result = userService.sendMail(email=email)
    return jsonify([result, store.USER_MESSAGE[result]])

@app.route("/matchVerify", methods=["POST"])
def matchVerifyHandler():
    email = request.json["joinEmail"]
    verify = request.json["joinVerify"]
    result = userService.matchVerify(email=email, code=verify)
    return jsonify(result)
    
@app.route("/changePw", methods=["POST"])
def changePwHandler():
    # 클라이언트 정보 가져오기
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    
    # form data 가져오기
    userNowPw = request.json["userNowPw"]
    userNewPw = request.json["userNewPw"]
    userNewConfirm = request.json["userNewConfirm"]

    result = userDAO.updateUserPassword(user=clientUser, nowPw=userNowPw, newPw=userNewPw, newConfirm=userNewConfirm)
    return jsonify([result, store.USER_MESSAGE[result]])

@app.route("/getVerify", methods=["POST"])
def getVerifyHandler():
    email = request.json["userEmail"]
    verify = request.json["userVerify"]
    result = userService.matchVerify(email=email, code=verify)
    userNo = userDAO.getUserByEmailAddress(email=email)[0][0]
    if result == 0:
        dbResult = userDAO.updateUserState(uno=userNo,u_state=store.USER_STATE_CODE['인증'])
        if dbResult == 0:
            return jsonify(store.USER_RESULT_CODE['실패-unknown'])
    return jsonify([result, store.USER_MESSAGE[result]])

@app.route("/leave", methods=["POST"])
def leaveHandler():
    email = request.json["userEmail"]
    pw = request.json["userPw"]
    userNo = userDAO.getUserByEmailAddress(email=email)[0][0]
    result = userDAO.leaveUser(uno=userNo, pw=pw)
    resp = jsonify([result, store.USER_MESSAGE[result]])
    if result == store.USER_RESULT_CODE['회원 탈퇴 성공']:
        # 쿠키 삭제
        resp.delete_cookie('sessionKey')
    return resp

#############################
######### 글 페이지 #########
#############################
@app.route("/board/<bno>")
def boardPage(bno):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)

    # 데이터 가져오기
    targetBoard = boardDAO.getBoardByBoardNo(bno=bno)
    isLiked = boardService.checkIsLiked(user=clientUser, board=targetBoard)
    cName = categoryService.getCategoryNameByCnoInCategoryList(cList=categoryList,cno=targetBoard.getCategoryNo())
    pageList = boardDAO.getPageList_category(targetBoard.getCategoryNo())
    nowPage = boardDAO.getPageOfCategory(board=targetBoard)
    isWritable = validate.checkWritableCategory(user=clientUser,cno=targetBoard.getCategoryNo())

    resp = make_response(render_template('board.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        targetBoard=targetBoard,
        isLiked=isLiked,
        cName=cName,
        pageList=pageList,
        nowPage=nowPage,
        isWritable=isWritable
    ))

    if targetBoard.getIsDelete() == 1:
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['삭제된글']])
        return resp

    # 뷰 설정하기
    userDAO.setView(user=clientUser, bno=targetBoard.getNo(), url=request.path)

    return resp

@app.route('/write/<nowCate>')
def writeBoardPage(nowCate):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    if not validate.checkWritePagePermission(user=clientUser):
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    # 글 작성 가능한 카테고리 리스트로 변경
    writableCategoryList = categoryDAO.getWritableCategoryList(user=clientUser)
    if len(writableCategoryList) == 0:
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    # 뷰 설정하기
    userDAO.setView(user=clientUser,url=request.path)

    return render_template('write.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        nowCate=int(nowCate),
        writableCategoryList=writableCategoryList
    )

@app.route('/writeBoard', methods=['POST'])
def saveBoard():
    # 템플릿 정보
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)

    # 데이터 수집
    selectCategory = request.form.get('selectCategory')
    title = request.form.get('title')
    content = request.form.get('content')

    # 글 작성 가능여부 확인
    if not validate.checkWritableCategory(user=clientUser,cno=int(selectCategory)):
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    result = boardDAO.setBoard(
        uno=clientUser.getNo(),
        cno=selectCategory,
        ip=clientUser.getIp(),
        title=title,
        contents=content
    )

    resp = ''
    if result:
        bno = boardDAO.getRecentlyBoardNoByUserNo(clientUser.getNo())
        resp = make_response(redirect(url_for('boardPage', bno=bno)))
    else:
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']])
    return resp

@app.route('/modify/<bno>')
def modifyBoardPage(bno):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)
    board = boardDAO.getBoardByBoardNo(bno=bno)
    
    # 작성자 확인 (관리자는 삭제 권한은 있지만 수정 권한은 없음)
    if clientUser.getNo() != board.getUserNo():
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    # 글 작성 가능한 카테고리 리스트로 변경
    writableCategoryList = categoryDAO.getWritableCategoryList(user=clientUser)
    if len(writableCategoryList) == 0:
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    # 뷰 설정하기
    userDAO.setView(user=clientUser,url=request.path)

    return render_template('modify.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        nowCate=board.getCategoryNo(),
        writableCategoryList=writableCategoryList,
        board=board
    )

@app.route('/modifyBoard/<bno>', methods=['POST'])
def modifyBoard(bno):
    # 템플릿 정보
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)

    # 데이터 수집
    bno = int(bno)
    selectCategory = request.form.get('selectCategory')
    title = request.form.get('title')
    content = request.form.get('content')

    # 글 작성 가능여부 확인
    if not validate.checkWritableCategory(user=clientUser,cno=int(selectCategory)):
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    # board 객체 셋팅
    board = boardDAO.getBoardByBoardNo(bno=bno)
    board.setCategoryNo(cno=int(selectCategory))
    board.setTitle(title=title)
    board.setContent(content=content)
    board.setIp(clientUser.getIp())

    result = boardDAO.updateBoard(board=board)
    resp = ''
    if result:
        resp = make_response(redirect(url_for('boardPage', bno=bno)))
    else:
        resp = make_response(redirect(url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']])
    return resp

@app.route('/deleteBoard/<bno>')
def deleteBoard(bno):
    # 템플릿 정보
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)

    resp = make_response(redirect(url_for('main')))

    if clientUser.getState() == store.USER_STATE_CODE['관리자']:
        pass
    elif clientUser.getNo() != boardDAO.getBoardByBoardNo(bno=bno).getUserNo():
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']])
        return resp
    
    result = boardDAO.deleteBoard(bno=bno)
    if result:
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['글삭제성공']])
    else:
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']])
    return resp

#############################
######### 글 핸들러 #########
#############################
@app.route("/setLike", methods=["POST"])
def setLikeHandler():
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    bno = request.json['bno']
    board = boardDAO.getBoardByBoardNo(bno=bno)
    result = boardDAO.setLike(user=clientUser, board=board)
    if result :
        return jsonify([result, store.USER_MESSAGE[store.USER_RESULT_CODE['좋아요 성공']], board.getLike()+1])
    else:
        return jsonify([result, store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']], board.getLike()])

@app.route("/getTitleListOnBoardByPage/<cno>/<page>", methods=["POST"])
def getTitleListOnBoardByPageHandler(cno,page):
    titleList = boardDAO.getTitleList_cathgory(cno=cno,page=page)
    return jsonify(titleList)

@app.route('/upload', methods=['POST'])
def uploadImageHandler():
    file = request.files.get('upload')
    if file:
        filename = secure_filename(file.filename)
        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d%H%M%S') + '_' + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({"uploaded": True, 'url': file_url})
    return jsonify({'error': {'message': '업로드 실패'}}), 400

@app.route("/getParentComment", methods=["POST"])
def getParentCommentHanler():
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    bno = request.json['bno']
    commentList = commentDAO.getParentCommentListByBno(bno=bno, uno=clientUser.getNo(), ustate=clientUser.getState())
    return jsonify(commentList)

@app.route("/getChildComment", methods=["POST"])
def getChildCommentHanler():
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    bno = request.json['bno']
    upperNo = request.json['upperNo']
    commentList = commentDAO.getChildCommentListByBnoAndCono(bno=bno, cono=upperNo, uno=clientUser.getNo(), ustate=clientUser.getState())
    return jsonify(commentList)

@app.route("/insertComment", methods=["POST"])
def insertCommentHanler():
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    bno = request.json['bno']
    upperNo = request.json['upperNo']
    comment = request.json['comment']
    if upperNo == 0:
        upperNo = "NULL"
    result = commentDAO.setComment(bno=bno,uno=clientUser.getNo(),coIp=clientUser.getIp(),comment=comment,upperNo=upperNo)
    if result:
        return jsonify([result])
    return jsonify([result,store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']]])

@app.route("/deleteComment", methods=["POST"])
def deleteCommentHanler():
    clientUser = userDAO.getUserBySessionKey(cookieKey=request.cookies.get('sessionKey'),ip=request.remote_addr)
    cono = request.json['cono']
    result = False
    if clientUser.getState() == store.USER_STATE_CODE['관리자']:
        dbResult = commentDAO.deleteComment(cono=cono)
        if dbResult != 0:
            result = True
    elif commentDAO.isMatch(cono=cono,uno=clientUser.getNo()):
        dbResult = commentDAO.deleteComment(cono=cono)
        if dbResult != 0:
            result = True
    else:
        return jsonify([result,store.USER_MESSAGE[store.USER_RESULT_CODE['권한없음']]])
    return jsonify([result,store.USER_MESSAGE[store.USER_RESULT_CODE['실패-unknown']]])




###############################
######## 카테고리 페이지 ########
###############################
@app.route("/category/<categoryNo>")
def categoryPage(categoryNo):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)

    # 데이터 가져오기
    cName = categoryService.getCategoryNameByCnoInCategoryList(cList=categoryList,cno=int(categoryNo))
    pageList = boardDAO.getPageList_category(int(categoryNo))
    isWritable = validate.checkWritableCategory(user=clientUser,cno=categoryNo)

    # 뷰 설정하기
    userDAO.setView(user=clientUser, url=request.path)

    return render_template('category.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        categoryNo=categoryNo,
        cName=cName,
        pageList=pageList,
        isWritable=isWritable
    )

###############################
######## 카테고리 핸들러 ########
###############################
@app.route("/getTitleListOnCategoryByPage/<cno>/<page>", methods=["POST"])
def getTitleListOnCategoryByPageHandler(cno,page):
    titleList = categoryDAO.getTitleList_cathgoryInCategoryPage(cno=cno,page=page)
    return jsonify(titleList)

#############################
######## 검색 페이지 ########
#############################
@app.route("/search/<keyword>")
def searchPage(keyword):
    # 템플릿 정보
    clientUser, categoryList, recentlyTitleList = getTemplateData(req=request)

    # 키워드 가공 및 키워드 리스트화
    keywordList, keywordLength = serachService.getFormattedKeyword(keyword=keyword)
    
    if keywordLength < 2: # 검색어 부족시
        resp = make_response(redirect(request.referrer or url_for('main')))
        flash(store.USER_MESSAGE[store.USER_RESULT_CODE['검색어 부족']])
        return resp
    
    # 데이터 받아오기
    
    pageList = boardDAO.getPageList_search(keywordList=keywordList)
    
    # 뷰 설정하기
    userDAO.setView(user=clientUser, url=request.path)
    return render_template('search.html',
        clientUser=clientUser,
        categoryList=categoryList,
        recentlyTitleList=recentlyTitleList,
        keyword=keyword,
        pageList=pageList
    )

#############################
######## 검색 핸들러 ########
#############################
@app.route("/getSearchListByPage/<keyword>/<page>", methods=["POST"])
def getSearchListByPageHandler(keyword,page):
    keywordList, keywordLength = serachService.getFormattedKeyword(keyword=keyword)
    searchBoardList = boardDAO.getSearchResult(keywordList=keywordList, page=page)
    searchDataList = serachService.setSearchStandard(searchBoardList=searchBoardList, keywordList=keywordList)
    return jsonify(searchDataList)



#############################
######### Flask App #########
#############################

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )