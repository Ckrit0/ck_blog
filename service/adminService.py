from service import store, logger
from dao import boardDAO
import psutil, platform, os, time, re, shutil
from datetime import datetime

log = logger.Logger()

def watchDog():
    while True:
        systemInfo = getSystemInfo()
        if systemInfo['cpuUsage'] > 80:
            log.setLog(store.LOG_NAME['시스템'], f"CPU 사용율 {systemInfo['cpuUsage']}%")
        if (systemInfo['usedMem'] / systemInfo['totalMem'])*100 > 80:
            log.setLog(store.LOG_NAME['시스템'], f"MEM 사용율 {(systemInfo['usedMem'] / systemInfo['totalMem'])*100}%")
        if (systemInfo['usedStorage'] / systemInfo['totalStorage'])*100 > 80:
            log.setLog(store.LOG_NAME['시스템'], f"Storage 사용율 {(systemInfo['usedStorage'] / systemInfo['totalStorage'])*100}%")
        print(f"watchDog: CPU 사용율: {systemInfo['cpuUsage']}%, MEM 사용율 {(systemInfo['usedMem'] / systemInfo['totalMem'])*100}%, Storage 사용율 {(systemInfo['usedStorage'] / systemInfo['totalStorage'])*100}%")
        time.sleep(3600)

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
    # 이거 서버에서 비밀번호 누르지 않게끔 하는 방법 있나 찾아봐야 함
    # os.system("sudo reboot")
    return

def checkImage():
    '''
    이미지를 역할에 맞는 디렉토리로 이동
    return: [[삭제성공갯수,삭제실패갯수],[더미이동성공갯수,더미이동실패갯수],[필요한 파일이 있는 글번호 리스트]]
    '''
    def moveFiles(fileList, targetDir):
        cnt = [0,0]
        for fileName in fileList:
            src = os.path.join(store.imageUploadDirectory, fileName)
            dst = os.path.join(targetDir, fileName)
            try:
                if os.path.exists(src):
                    shutil.move(src, dst)
                    cnt = [cnt[0]+1,cnt[1]]
            except Exception as e:
                log.setLog(store.LOG_NAME['관리자'],f'파일 이동 실패: {fileName} - {e}')
                cnt = [cnt[0],cnt[1]+1]
        return cnt

    serverFileList = os.listdir(store.imageUploadDirectory)
    allBoardList = boardDAO.getAllBoardForImage()
    boardImageList = []
    for board in allBoardList:
        contents = board.getContents()
        # pattern = r'<img[^>]*src=["\']([^"\']+)["\']' # 모든 이미지 태그 주소
        pattern = r'<img[^>]*src=["\']/static/uploads/([^"\']+)["\']' # 서버에 올라온 이미지 태그 파일명
        image_sources = re.findall(pattern, contents)
        if image_sources == []:
            continue
        
        boardImage = {
            'bno': board.getNo(),
            'isDelete': board.getIsDelete(),
            'imgSrc': image_sources
        }
        boardImageList.append(boardImage)
    
    serverSet = set(serverFileList)
    neededImages = set()
    deletedImages = set()

    for board in boardImageList:
        for src in board['imgSrc']:
            if board['isDelete'] != 0:
                deletedImages.add(src)
            else:
                neededImages.add(src)
    forDeleteFileList = list(deletedImages & serverSet)
    forNeedFileList = list(neededImages - serverSet)
    forDummyFileList = list(serverSet - neededImages - deletedImages - set(['dummy','deleted']))
    deleteCnt = moveFiles(forDeleteFileList,store.imageDeleteDirectory)
    dummyCnt = moveFiles(forDummyFileList,store.imageDummyDirectory)
    needCnt = []
    for needFile in forNeedFileList:
        for board in boardImageList:
            for imgSrc in board['imgSrc']:
                if needFile == imgSrc:
                    needCnt.append(board['bno'])
                    log.setLog(store.LOG_NAME['관리자'],f"파일 없음: 글번호:{board['bno']}, 파일명:{needFile}")
    return [deleteCnt,dummyCnt,needCnt]

def deleteDummy():
    '''
    더미 폴더에 있는 이미지 삭제
    return: 삭제한 이미지 갯수(int)
    '''
    return 1