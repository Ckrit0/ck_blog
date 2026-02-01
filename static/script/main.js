let mainListTable = document.getElementById('mainListTable')
let mainNowPage = document.getElementById('mainNowPage')
let pagingUl = document.getElementById('mainPagingUl')
let pageLiList = document.getElementsByClassName('pages')

/**
 * 전체 최근목록 가져와서 element 추가
 * @param setPageNum
 */
function setMainList(setPageNum){
    if(setPageNum <= 0){
        setPageNum = 1
    }else if(setPageNum > pagingUl.children.length - 2){
        setPageNum = pagingUl.children.length - 2
    }
    mainNowPage.innerHTML = setPageNum
    
    url = "/getTitleListOnBoardByPage/" + setPageNum
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
                let tr1 = getNewElement('tr',['tableUpper','tableLower'])
                let subject = getNewElement('td',['tableBodyItem', 'tableSubject'],contentsList[0])
                let view = getNewElement('td',['tableBodyItem', 'tableView'],contentsList[1])
                let like = getNewElement('td',['tableBodyItem', 'tableLike'],contentsList[2])
                let comment = getNewElement('td',['tableBodyItem', 'tableComment'],contentsList[3])
                tr1.onclick = function(){
                    window.location.href="/board/" + bno
                }
                appendItemList(tr1,[subject,view,like,comment])
                appendItemList(boxElement,[tr1])
            }
            mainListTable.innerHTML = ''
            let tHead = getNewElement('thead')
            let tr = getNewElement('tr',['tableUpper','tableLower'])
            let subject = getNewElement('th',['tableHeaderItem', 'tableSubject', 'center'],'글')
            let view = getNewElement('th',['tableHeaderItem', 'tableView'],'조회')
            let like = getNewElement('th',['tableHeaderItem', 'tableLike'],'공감')
            let comment = getNewElement('th',['tableHeaderItem', 'tableComment'],'댓글')
            appendItemList(tr,[subject,view,like,comment])
            tHead.appendChild(tr)
            mainListTable.appendChild(tHead)

            if(result.length == 0){
                let tr = getNewElement('tr',['tableUpper', 'tableLower'])
                let td = getNewElement('td',['tableBodyItem'],'검색결과가 없습니다.')
                tr.appendChild(td)
                titlesListTable.appendChild(tr)
            }else{
                let tBody = document.createElement('tbody')
                for(let i in result){
                    setTableLine(tBody, [result[i][1],result[i][2],result[i][3],result[i][4]],result[i][0])
                }
                mainListTable.appendChild(tBody)
            }
        });
    setMainPagingList(setPageNum)
}

function setMainPagingList(showPage){
    function getShowList(showPage, totalPage){
        if(showPage < 3){
            return ['1','2','3','4','5','[next]']
        }else if(showPage > totalPage - 2){
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
    let totalPage = pagingUl.children
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
    for(let i=0;i<pagingUl.children.length;i++){
        if(pagingUl.children[i].innerHTML == mainNowPage.innerHTML){
            pagingUl.children[i].style['font-size'] = '30px'
            pagingUl.children[i].style['vertical-align'] = 'bottom'
        }else{
            pagingUl.children[i].style['font-size'] = '20px'
            pagingUl.children[i].style['align-self'] = 'end'
        }
    }
}

function mainPrevPage(){
    setMainList(parseInt(mainNowPage.innerHTML)-5)
}

function mainNextPage(){
    setMainList(parseInt(mainNowPage.innerHTML)+5)
}

setMainList(mainNowPage.innerHTML)
