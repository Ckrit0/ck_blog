from service import db, store
import psutil, platform, os
from datetime import datetime

def getSystemInfo():
    '''
    서버의 CPU, MEM, Storage 상태를 확인
    return: 서버 상태 딕셔너리(Dict.)
    '''
    def setUptimeFormat(uptime):
        uptimeString = ''
        if uptime.days != 0:
            uptimeString += str(uptime.days) + ' days '
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        seconds = uptime.seconds % 60
        uptimeString += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        return uptimeString
    os = platform.system()
    cpuUsage = psutil.cpu_percent(interval=1) # cpu 사용율(%)
    virtualMemory = psutil.virtual_memory()
    totalMem = round(virtualMemory.total / (1024**3),2)  # 총 메모리(GB)
    usedMem = round(virtualMemory.used / (1024**3),2) # 사용중 메모리
    storage = psutil.disk_usage('/')
    totalStorage = round(storage.total / (1024**3),2) # 총 용량(GB)
    usedStorage = round(storage.used / (1024**3),2) # 사용중 용량
    bootTime = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - bootTime
    uptime = setUptimeFormat(uptime)
    systemInfo = {
        'os':os,
        'cpuUsage': cpuUsage,
        'totalMem': totalMem,
        'usedMem': usedMem,
        'totalStorage': totalStorage,
        'usedStorage': usedStorage,
        'bootTime': bootTime.strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': uptime
    }
    return systemInfo

def reboot():
    os.system("sudo reboot")
    return

def checkImage():
    '''
    이미지를 역할에 맞는 디렉토리로 이동
    return: 정리한 이미지 갯수(int)
    '''
    # 1. 모든 이미지파일명을 가져와서 리스트로 만든다.
    # 2. 모든 글을 가져와서 image src 내부 주소를 delete여부를 구분하여 리스트로 만든다.
    # 3. 두 리스트를 비교하여 현재 글에 쓰이는 이미지와 삭제된 이미지와, dummy 이미지를 구분하여 파일을 이동한다.
    return 1

def deleteDummy():
    '''
    더미 폴더에 있는 이미지 삭제
    return: 삭제한 이미지 갯수(int)
    '''
    return 1