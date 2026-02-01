let nowSearchPageDiv = document.getElementById('nowSearchPageDiv')
let searchPagingUl = document.getElementById('searchPagingUl')
let searchKeywordDiv = document.getElementById('searchKeywordDiv')
let searchListTable = document.getElementById('searchListTable')

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
            function getNewElement(tagName,classList=[],innerHTML=''){
                let newElement = document.createElement(tagName)
                for(let i=0;i<classList.length;i++){
                    newElement.classList.add(classList[i])
                }
                newElement.innerHTML = innerHTML
                return newElement
            }
            function appendItemList(itemBox, itemList){
                for(let i=0;i<itemList.length;i++){
                    itemBox.appendChild(itemList[i])
                }
            }
            /**
             * response 데이터로 페이지에 들어갈 내용 추가하기
             * @param {boolean} isHead 헤더인지 아닌지 여부
             * @param {Element} boxElement 여기에 추가할거임
             * @param {Array} contentsList 카테고리, 제목, 조회수, 공감수, 댓글수, 내용 순
             * @param {int} bno onclick 넣기위함. undefined시 넣지 않음
             */
            function setTableLine(boxElement, contentsList, bno){
                let tr1 = getNewElement('tr',['tableUpper'])
                let subject = getNewElement('td',['tableBodyItem', 'tableSubject'],'[' + contentsList[0] + '] ' + contentsList[1])
                let view = getNewElement('td',['tableBodyItem', 'tableView'],contentsList[2])
                view.rowSpan = 2
                let like = getNewElement('td',['tableBodyItem', 'tableLike'],contentsList[3])
                like.rowSpan = 2
                let comment = getNewElement('td',['tableBodyItem', 'tableComment'],contentsList[4])
                comment.rowSpan = 2
                tr1.onclick = function(){
                    window.location.href="/board/" + bno
                }
                appendItemList(tr1,[subject,view,like,comment])
                let tr2 = getNewElement('tr',['tableLower'])
                let contents = getNewElement('td',['tableBodyItem', 'tableContents'],contentsList[5])
                tr2.appendChild(contents)
                tr2.onclick = function(){
                    window.location.href="/board/" + bno
                }
                appendItemList(boxElement,[tr1,tr2])
            }
            searchListTable.innerHTML = ''
            let tHead = getNewElement('thead')
            let tr = getNewElement('tr',['tableUpper','tableLower'])
            let subject = getNewElement('th',['tableHeaderItem', 'tableSubject', 'center'],'글')
            let view = getNewElement('th',['tableHeaderItem', 'tableView'],'조회')
            let like = getNewElement('th',['tableHeaderItem', 'tableLike'],'공감')
            let comment = getNewElement('th',['tableHeaderItem', 'tableComment'],'댓글')
            appendItemList(tr,[subject,view,like,comment])
            tHead.appendChild(tr)
            searchListTable.appendChild(tHead)

            if(result.length == 0){
                let tr = document.createElement('tr')
                let td = document.createElement('td')
                td.classList.add('tableBodyItem')
                td.innerHTML = '검색 결과가 없습니다.'
                tr.appendChild(td)
                searchListTable.appendChild(tr)
            }else{
                let tBody = document.createElement('tbody')
                for(let i in result){
                    setTableLine(tBody, [result[i][5],result[i][1],result[i][2],result[i][3],result[i][6],result[i][4]],result[i][0])
                }
                searchListTable.appendChild(tBody)
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