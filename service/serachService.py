import copy

def getFormattedKeyword(keyword):
    '''
    검색어 가공(앞 뒤 공백 제거, 두칸 이상의 공백이면 한칸으로)
    parameter: 검색어(String)
    return: 가공된검색어(String), 공백제외글자수(int)
    '''
    formattedKeyword = keyword.strip()
    while formattedKeyword.find('  ') >= 0:
        formattedKeyword = formattedKeyword.replace('  ',' ')
    keywordLength = 0
    for word in formattedKeyword:
        if word != ' ':
            keywordLength = keywordLength + 1
    return formattedKeyword, keywordLength