let nowSearchPageDiv = document.getElementById('nowSearchPageDiv')
let searchPagingUl = document.getElementById('searchPagingUl')
let searchKeywordDiv = document.getElementById('searchKeywordDiv')
let searchListUl = document.getElementById('searchListUl')

/**
 * 검색목록 가져와서 element 추가
 * @param setPageNum
 */
function setSearchList(setPageNum){
    setPageNum = parseInt(setPageNum)
    if(setPageNum <= 0){
        setPageNum = 1
    }else if(setPageNum > searchPagingUl.children.length - 2){
        setPageNum = searchPagingUl.children.length - 2
    }
    nowSearchPageDiv.innerHTML = setPageNum
    let keyword = searchKeywordDiv.innerHTML
    
    url = "/getSearchListByPage/" + keyword + "/" + setPageNum
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            searchListUl.innerHTML = ''
            console.log(result)
            for(let i in result){
                let item = document.createElement('li')
                item.classList.add("pointer")
                item.onclick = function(){
                    window.location.href="/board/" + result[i][0]
                }
                item.innerHTML = '[' + result[i][5] + ']' + result[i][1] + ' 👁️ ' + result[i][2] + ' ❤️ ' + result[i][3]
                let contentsItem = document.createElement('div')
                contentsItem.classList.add("shortContents")
                contentsItem.innerHTML = result[i][4]
                item.appendChild(contentsItem)
                searchListUl.appendChild(item)
            }
        });
    setSearchPagingList(setPageNum)
}

/**
 * 페이징리스트 설정하기
 * @param showPage 
 */
function setSearchPagingList(showPage){
    function getShowList(showPage, totalPage){
        if(showPage < 3){
            return ['1','2','3','4','5','[next]']
        }else if(showPage > totalPage-2){
            return [
                '[prev]',
                String(totalPage-4),
                String(totalPage-3),
                String(totalPage-2),
                String(totalPage-1),
                String(totalPage)
            ]
        }else{
            return [
                '[prev]',
                String(showPage-2),
                String(showPage-1),
                String(showPage),
                String(showPage+1),
                String(showPage+2),
                '[next]'
            ]
        }
    }
    let totalPage = searchPagingUl.children
    if(totalPage.length-2 > 5){
        showList = getShowList(showPage,totalPage.length-2)
        for(let i=0; i<totalPage.length;i++){
            if(showList.indexOf(totalPage[i].innerHTML) >= 0 ){
                totalPage[i].style['display'] = ''
            }else{
                totalPage[i].style['display'] = 'none'
            }
        }
    }else{
        for(let i=0; i<totalPage.length;i++){
            if(['1','2','3','4','5'].indexOf(totalPage[i].innerHTML) >= 0 ){
                totalPage[i].style['display'] = ''
            }else{
                totalPage[i].style['display'] = 'none'
            }
        }
    }
    for(let i=0;i<searchPagingUl.children.length;i++){
        if(searchPagingUl.children[i].innerHTML == nowSearchPageDiv.innerHTML){
            searchPagingUl.children[i].style['font-size'] = '30px'
            searchPagingUl.children[i].style['vertical-align'] = 'bottom'
        }else{
            searchPagingUl.children[i].style['font-size'] = '20px'
            searchPagingUl.children[i].style['align-self'] = 'end'
        }
    }
}

/**
 * 이전 페이지 버튼 눌렀을 때 동작
 */
function searchPrevPage(){
    setSearchList(parseInt(nowSearchPageDiv.innerHTML)-5)
}

/**
 * 다음 페이지 눌렀을 때 동작
 */
function searchNextPage(){
    setSearchList(parseInt(nowSearchPageDiv.innerHTML)+5)
}

// 초기 실행
setSearchList(nowSearchPageDiv.innerHTML)