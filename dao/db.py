import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
dbInfo = {
    'host' : os.environ.get("dbIp"),
    'port' : int(os.environ.get("dbPort")),
    'user' : os.environ.get("dbUser"),
    'password' : os.environ.get("dbPw"),
    'database' : os.environ.get("dbDatabase")
}

def __getCursor():
    global dbInfo
    con = None
    cur = None
    try:
        con = pymysql.connect(
          host=dbInfo['host'],
          port=dbInfo['port'],
          user=dbInfo['user'],
          password=dbInfo['password'],
          database=dbInfo['database']
        )
        cur = con.cursor()
    except Exception as e:
        print('Connect Error:',e)
    return con, cur

def getData(sql):
    data = []
    con, cur = __getCursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            for r in row:
                data.append(r)
    except Exception as e:
        print(e)
    finally:
        con.close()
    return data

def setData(sql):
    result = False
    con, cur = __getCursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
    return result

def setDatas(sqlList):
    result = False
    con, cur = __getCursor()
    try:
        for sql in sqlList:
            cur.execute(sql)
        result = cur.fetchall()
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()
    return result

def setUser(user):
    pass
def setBoard(board):
    pass
def setLike(user):
    pass
def setComment(comment):
    pass
def setBlackList(user):
    pass
def setSession(user):
    pass
def setImage(image):
    pass

def updateUser(user):
    pass
def updateBoard(board):
    pass
def updateComment(comment):
    pass
def updateSessionDate(user):
    pass

def getUserByEmailAndPw(email,pw):
    pass
def getUserByUserNo(uno):
    pass
def getBoardNoList():
    pass
def getTitleListByBoardNoList(boardNoList):
    pass
def getBoardByBoardNo(bno):
    pass
def getLike(bno):
    pass
def getCommentNoListByBoardNo(bno):
    pass
def getCommentByCommentNo(cono):
    pass
def getBlackList():
    pass
def getSessionKeyByUserNo(uno):
    pass
def getImageByImageNo(ino):
    pass