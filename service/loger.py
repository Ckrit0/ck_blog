from datetime import datetime
import pytz
import os
from service import store

class Loger:
    def __init__(self):
        self.logPath = store.logPath
        if self.logPath.endswith('/'):
            self.logPath = self.logPath[:-1]

    def __getLogDate(self):
        dateStr = ''
        now = datetime.now(tz=pytz.timezone('Asia/Seoul'))
        dateStr += str(now.year)
        dateStr += '-'
        if now.month < 10:
            dateStr += '0' + str(now.month)
        else:
            dateStr += str(now.month)
        dateStr += '-'
        if now.day < 10:
            dateStr += '0' + str(now.day)
        else:
            dateStr += str(now.day)
        return dateStr

    def __getLogTime(self):
        timeStr = ''
        now = datetime.now(tz=pytz.timezone('Asia/Seoul'))
        if now.hour < 10:
            timeStr += '0' + str(now.hour)
        else:
            timeStr += str(now.hour)
        timeStr += ':'
        if now.minute < 10:
            timeStr += '0' + str(now.minute)
        else:
            timeStr += str(now.minute)
        timeStr += ':'
        if now.second < 10:
            timeStr += '0' + str(now.second)
        else:
            timeStr += str(now.second)
        return timeStr

    def __appendLine(self,dirPath,fileName,line):
        os.makedirs(dirPath, exist_ok=True)   
        with open(dirPath + fileName, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    '''
    로그 등록
    로그 위치 및 파일명: store에 등록된 경로/로그명/날짜_로그명
    parameter: 로그명(String), 로그내용(String)
    '''
    def setLog(self,logName,log):
        logDate = self.__getLogDate()
        logTime = self.__getLogTime()
        dirPath = self.logPath + '/' + logName + '/'
        fileName = logDate + '_' + logName
        logLine = logDate + '_' + logTime + ' ' + log
        self.__appendLine(dirPath=dirPath,fileName=fileName,line=logLine)
        return