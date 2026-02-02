from service import store
import psutil
from datetime import datetime, timedelta

def get_system_info():
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
        'cpuUsage': cpuUsage,
        'totalMem': totalMem,
        'usedMem': usedMem,
        'totalStorage': totalStorage,
        'usedStorage': usedStorage,
        'bootTime': bootTime.strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': uptime
    }
    return systemInfo