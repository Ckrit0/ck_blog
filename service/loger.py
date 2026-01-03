from datetime import datetime
import pytz
import os
from service import store

class Loger:
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super().__new__(cls=cls)
        return cls.instance
    
    def __init__(self):
        self.logPath = store.logPath

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

    def setLog(self,logName,log):
        dirPath = self.logPath + '/' + logName + '/'
        fileName = self.__getLogDate() + '_' + logName
        logLine = self.__getLogDate() + '_' + self.__getLogTime() + ' ' + log
        self.__appendLine(dirPath=dirPath,fileName=fileName,line=logLine)