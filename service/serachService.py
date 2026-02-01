from dao import categoryDAO
from service import store
import re, html

def getFormattedKeyword(keyword):
    '''
    검색어 가공(앞 뒤 공백 제거, 두칸 이상의 공백이면 한칸으로)
    parameter: 검색어(String)
    return: 검색어 이중리스트([[검색어,가중치]...]), 공백제외글자수(int)
    '''
    formattedKeyword = keyword.strip()
    formattedKeyword = re.sub(r"\s+", " ", formattedKeyword)
    keywordLength = 0
    for word in formattedKeyword:
        if word != ' ':
            keywordLength = keywordLength + 1
    keywordList = []
    # 키워드 통째로 넣기
    keywordList.append([formattedKeyword,store.searchWeight[0]])
    # 키워드를 단어별로 넣기
    for keyword in formattedKeyword.split(' '):
        keywordList.append([keyword,store.searchWeight[1]])
    # 키워드를 글자별로 넣기
    for keyword in formattedKeyword:
        if keyword == ' ':
            continue
        keywordList.append([keyword,store.searchWeight[2]])
    return keywordList, keywordLength




def setSearchStandard(searchBoardList, keywordList):
    '''
    검색된 글목록을 검색창에 표시하기에 알맞게 수정
    parameter: 검색결과 글객체 리스트(List), 키워드 리스트(List)
    return: 수정된 검색결과 글객체 리스트(List)
    '''
    def setContents(contents, keywordList):
        def deleteTag(contents,startTag,endTag):
            while True:
                start_idx = contents.find(startTag)
                if start_idx == -1:
                    return contents
                end_idx = contents.find(endTag, start_idx + len(startTag))
                if end_idx == -1:
                    return contents
                end_idx += len(endTag)
                contents = contents[:start_idx] + contents[end_idx:]
        
        # HTML 엔티티 문자 변경
        contents = html.unescape(contents)
        # figure 태그 삭제
        contents = deleteTag(contents=contents,startTag='<figure',endTag='</figure>')
        # img 태그 삭제
        contents = deleteTag(contents=contents,startTag='<img src=',endTag='>')

        # P태그가 있으면, 내부 문구만 contentList로 만들기
        contentList = []
        startTag = '<p>'
        endTag = '</p>'
        while True:
            start_idx = contents.find(startTag)
            if start_idx == -1:
                break
            start_idx += len(startTag)
            end_idx = contents.find(endTag, start_idx)
            if end_idx == -1:
                break
            contentList.append(contents[start_idx:end_idx])
            end_idx += len(endTag)
            contents = contents[end_idx:]
        
        # P태그가 없으면, 전체 문구를 contentList에 추가함
        if contentList == []:
            contentList.append(contents)

        # 키워드의 내용을 span태그로 감싸고, 해당 문구를 result에 추가함.
        result = ''
        for keyword in keywordList:
            for i in range(len(contentList)):
                if contentList[i].find(keyword[0]) >= 0:
                    if result != '':
                        result + '...'
                    result += contentList[i].replace(keyword[0],"<span class='bolder font20'>" + keyword[0] + "</span>")
                    contentList[i] = '' # 동일 문자열이 중복으로 포함되는 것을 방지
        
        # result의 내용이 없으면 전체 글을 넣음
        if result == '':
            for content in contentList:
                result += content
        
        # result의 내용이 너무 길면 잘라냄
        if len(result) >= store.searchWordCount:
            result = result[:store.searchWordCount] + '...'
        
        # result에 span이 안닫혔으면, 그냥 span을 닫아줌
        if result.rfind("<span class='bolder'>") > result.rfind("</span>"):
            result += "</span>"
        return result
    
    for board in searchBoardList:
        board.setTitle(setContents(contents=board.getTitle(), keywordList=keywordList))
        board.setContent(setContents(contents=board.getContents(), keywordList=keywordList))
    result = []
    for i in range(len(searchBoardList)):
        tempList = []
        tempList.append(searchBoardList[i].getNo())
        tempList.append(searchBoardList[i].getTitle())
        tempList.append(searchBoardList[i].getView())
        tempList.append(searchBoardList[i].getLike())
        tempList.append(searchBoardList[i].getContents())
        tempList.append(categoryDAO.getCategoryNameByCno(searchBoardList[i].getCategoryNo()))
        tempList.append(searchBoardList[i].getCommentCount())
        result.append(tempList)
    return result