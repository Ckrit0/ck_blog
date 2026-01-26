let mainListUl = document.getElementById('mainListUl')
let mainNowPage = document.getElementById('mainNowPage')
let mainPagingUl = document.getElementById('mainPagingUl')
let pageLiList = document.getElementsByClassName('pages')

/**
 * 전체 최근목록 가져와서 element 추가
 * @param setPageNum
 */
function setMainList(setPageNum){
    if(setPageNum < 0){
        setPageNum = 1
    }else if(setPageNum > mainPagingUl.children.length - 2){
        setPageNum = mainPagingUl.children.length - 2
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
            mainListUl.innerHTML = ''
            for(let i in result){
                var item = document.createElement('li')
                item.classList.add("pointer")
                item.onclick = function(){
                    window.location.href="/board/" + result[i][0]
                }
                item.innerHTML = result[i][1] + ' 👁️ ' + result[i][2] + ' ❤️ ' + result[i][3]
                mainListUl.appendChild(item)
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
    let totalPage = mainPagingUl.children
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
    for(let i=0;i<mainPagingUl.children.length;i++){
        if(mainPagingUl.children[i].innerHTML == mainNowPage.innerHTML){
            mainPagingUl.children[i].style['font-size'] = '30px'
            mainPagingUl.children[i].style['vertical-align'] = 'bottom'
        }else{
            mainPagingUl.children[i].style['font-size'] = '20px'
            mainPagingUl.children[i].style['align-self'] = 'end'
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
