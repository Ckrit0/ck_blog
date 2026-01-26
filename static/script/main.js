let mainListUl = document.getElementById('mainListUl')
let mainNowPage = document.getElementById('mainNowPage')
let pageLiList = document.getElementsByClassName('pages')

/**
 * 전체 최근목록 가져와서 element 추가
 * @param setPageNum
 */
function setMainList(setPageNum){
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
    for(let i=0;i<pageLiList.length;i++){
        if(pageLiList[i].innerHTML == mainNowPage.innerHTML){
            pageLiList[i].style['font-size'] = '30px'
            pageLiList[i].style['vertical-align'] = 'bottom'
        }else{
            pageLiList[i].style['font-size'] = '20px'
            pageLiList[i].style['align-self'] = 'end'
        }
    }
}

setMainList(mainNowPage.innerHTML)