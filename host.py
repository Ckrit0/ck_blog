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

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )