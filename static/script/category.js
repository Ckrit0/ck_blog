let nowCategoryPageDiv = document.getElementById('nowCategoryPageDiv')
let categoryPagingUl = document.getElementById('categoryPagingUl')
let nowCategoryNoDiv = document.getElementById('nowCategoryNoDiv')

/**
 * 카테고리 최근목록 가져와서 element 추가
 * @param setPageNum
 */
function setCategoryList(setPageNum){
    setPageNum = parseInt(setPageNum)
    if(setPageNum <= 0){
        setPageNum = 1
    }else if(setPageNum > categoryPagingUl.children.length - 2){
        setPageNum = categoryPagingUl.children.length - 2
    }
    nowCategoryPageDiv.innerHTML = setPageNum
    let cno = nowCategoryNoDiv.innerHTML
    
    url = "/getTitleListOnCategoryByPage/" + cno + "/" + setPageNum
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
            categoryTitlesListUl.innerHTML = ''
            for(let i in result){
                let item = document.createElement('li')
                item.classList.add("pointer")
                item.onclick = function(){
                    window.location.href="/board/" + result[i][0]
                }
                item.innerHTML = '<span class="bolder">' + result[i][1] + '</span> 👁️ ' + result[i][2] + ' ❤️ ' + result[i][3]
                let contentsItem = document.createElement('div')
                contentsItem.classList.add("shortContents")
                contentsItem.innerHTML = result[i][4]
                item.appendChild(contentsItem)
                categoryTitlesListUl.appendChild(item)
            }
        });
    setBoardPagingList(setPageNum)
}

/**
 * 페이징리스트 설정하기
 * @param showPage 
 */
function setBoardPagingList(showPage){
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
    let totalPage = categoryPagingUl.children
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
    for(let i=0;i<categoryPagingUl.children.length;i++){
        if(categoryPagingUl.children[i].innerHTML == nowCategoryPageDiv.innerHTML){
            categoryPagingUl.children[i].style['font-size'] = '30px'
            categoryPagingUl.children[i].style['vertical-align'] = 'bottom'
        }else{
            categoryPagingUl.children[i].style['font-size'] = '20px'
            categoryPagingUl.children[i].style['align-self'] = 'end'
        }
    }
}

/**
 * 이전 페이지 버튼 눌렀을 때 동작
 */
function categoryPrevPage(){
    setCateList(parseInt(nowCategoryPageDiv.innerHTML)-5)
}

/**
 * 다음 페이지 눌렀을 때 동작
 */
function categoryNextPage(){
    setCateList(parseInt(nowCategoryPageDiv.innerHTML)+5)
}

// 초기 실행
setCategoryList(nowCategoryPageDiv.innerHTML)