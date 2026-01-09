from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from service import store
from dao import userDAO
from service import validate

app = Flask(__name__)

@app.before_request
def validateCheck():
    clientUser = userDAO.getUserBySessionKey(sessionKey=request.cookies.get('sessionKey'))
    clientIp = request.remote_addr
    if validate.checkBlackList(clientUser,clientIp):
        abort(403)

@app.route("/")
def main():
    return render_template('main.html')

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