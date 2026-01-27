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

'''
SELECT문으로 DATA 가져오기
parameter: SQL문(String)
return: DATA List(List)
'''
def getData(sql):
    # print('db.getData sql:',sql)
    data = []
    con, cur = __getCursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tempList = []
            for r in row:
                tempList.append(r)
            data.append(tempList)
    except Exception as e:
        print(e)
        print(sql)
    finally:
        con.close()
    return data

'''
INSERT, UPDATE, DELETE문 적용시키기
parameter: SQL문(String)
return: 영향을 받은 줄 갯수(int)
'''
def setData(sql):
    result = 0
    con, cur = __getCursor()
    try:
        cur.execute(sql)
        con.commit()
        result = cur.rowcount
    except Exception as e:
        print(e)
        print(sql)
    finally:
        con.close()
    return result

'''
INSERT, UPDATE, DELETE문 여러줄 한번에 적용시키기
parameter: SQL문 List(String List)
return: 영향을 받은 줄 갯수(int)
'''
def setDatas(sqlList):
    result = 0
    con, cur = __getCursor()
    try:
        for sql in sqlList:
            cur.execute(sql)
        con.commit()
        result = cur.rowcount
    except Exception as e:
        print(e)
        print(sql)
    finally:
        con.close()
    return result