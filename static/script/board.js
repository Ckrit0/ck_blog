let likeMarkSpan = document.getElementById('likeMarkSpan')
let likeCountSpan = document.getElementById('likeCountSpan')
let boardNoDiv = document.getElementById('boardNoDiv')
let nowCnoDiv = document.getElementById('nowCnoDiv')
let nowPageDiv = document.getElementById('nowPageDiv')
let categoryTitlesListUl = document.getElementById('titlesUl')
let titleLiList = document.getElementsByClassName('titles')
let boardPagingUl = document.getElementById('boardPagingUl')
let pageLiList = document.getElementsByClassName('pages')
let commentTextarea = document.getElementById('commentTextarea')
let commentInputBtn = document.getElementById('commentInputBtn')
let commentParentDiv = document.getElementById('commentParentDiv')


/**
 * 좋아요 표시하기
 */
function setLike(){
    fetch("/setLike", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: boardNoDiv.innerHTML
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            likeCountSpan.innerHTML = result[2]
            if(result[0]){
                likeMarkSpan.innerHTML = '❤️'
                boardNoDiv.outerHTML = ''
            }else{
                alert(result[1])
            }
        });
}

/**
 * 카테고리 최근목록 가져와서 element 추가
 * @param setPageNum
 */
function setCateList(setPageNum){
    setPageNum = parseInt(setPageNum)
    if(setPageNum <= 0){
        setPageNum = 1
    }else if(setPageNum > boardPagingUl.children.length - 2){
        setPageNum = boardPagingUl.children.length - 2
    }
    nowPageDiv.innerHTML = setPageNum
    let bno = boardNoDiv.innerHTML
    let cno = nowCnoDiv.innerHTML
    
    url = "/getTitleListOnBoardByPage/" + cno + "/" + setPageNum
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: bno
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            categoryTitlesListUl.innerHTML = ''
            for(let i in result){
                if(result[i][0] == bno){
                    var item = document.createElement('li')
                    item.classList.add("boardTitles")
                    item.innerHTML = result[i][1] + ' 👁️ ' + result[i][2] + ' ❤️ ' + result[i][3] + ' (현재글)' 
                    categoryTitlesListUl.appendChild(item)                    
                }else{
                    var item = document.createElement('li')
                    item.classList.add("boardTitles")
                    item.classList.add("pointer")
                    item.onclick = function(){
                        window.location.href="/board/" + result[i][0]
                    }
                    item.innerHTML = result[i][1] + ' 👁️ ' + result[i][2] + ' ❤️ ' + result[i][3]
                    categoryTitlesListUl.appendChild(item)                    
                }
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
    let totalPage = boardPagingUl.children
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
    for(let i=0;i<boardPagingUl.children.length;i++){
        if(boardPagingUl.children[i].innerHTML == nowPageDiv.innerHTML){
            boardPagingUl.children[i].style['font-size'] = '30px'
            boardPagingUl.children[i].style['vertical-align'] = 'bottom'
        }else{
            boardPagingUl.children[i].style['font-size'] = '20px'
            boardPagingUl.children[i].style['align-self'] = 'end'
        }
    }
}

/**
 * 이전 페이지 버튼 눌렀을 때 동작
 */
function boardPrevPage(){
    setCateList(parseInt(nowPageDiv.innerHTML)-5)
}

/**
 * 다음 페이지 눌렀을 때 동작
 */
function boardNextPage(){
    setCateList(parseInt(nowPageDiv.innerHTML)+5)
}

/**
 * 상위 댓글 가져와서 element 추가
 */
function getParentComment(){
    let bno = boardNoDiv.innerHTML
    url = '/getParentComment'
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: bno
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            commentParentDiv.innerHTML = ''
            for(let i=0;i<result.length;i++){
                let liElement = document.createElement('li')

                let spanElement_email = document.createElement('span')
                let spanElement_ip = document.createElement('span')
                let spanElement_date = document.createElement('span')
                let spanElement_contents = document.createElement('span')
                let spanElement_getChild = document.createElement('span')
                let spanElement_setChild = document.createElement('span')
                let childCommentUl = document.createElement('ul')
                let commentTextarea = document.createElement('textarea')
                let commentInputBtn = document.createElement('button')
                
                spanElement_email.classList.add('commentEmail')
                spanElement_email.onclick = function(){
                    window.location.href='/user/' + result[i][2]
                }
                spanElement_email.innerHTML = result[i][8]
                liElement.appendChild(spanElement_email)
                
                spanElement_ip.classList.add('commentIp')
                spanElement_ip.innerHTML = '(' + result[i][3] + ')'
                liElement.appendChild(spanElement_ip)
                
                spanElement_date.classList.add('commentDate')
                spanElement_date.innerHTML = result[i][5]
                liElement.appendChild(spanElement_date)
                
                spanElement_contents.classList.add('commentContents')
                spanElement_contents.innerHTML = result[i][4]
                if(result[i][7] == 1){
                    spanElement_contents.classList.add('deleted')
                }else if(result[i][12]){
                    let removeBtn = document.createElement('span')
                    removeBtn.classList.add('commentRemove')
                    removeBtn.innerHTML = '삭제'
                    removeBtn.onclick = function(){
                        removeComment(result[i][0])
                    }
                    spanElement_contents.appendChild(removeBtn)
                }
                liElement.appendChild(spanElement_contents)
                
                spanElement_getChild.id = "getChildBtn_" + result[i][0]
                spanElement_getChild.classList.add('commentGetChild')
                spanElement_getChild.innerHTML = '답글(' + result[i][11] + ')'
                spanElement_getChild.onclick = function(){
                    getChildComment(result[i][0])
                }
                liElement.appendChild(spanElement_getChild)
                
                spanElement_setChild.classList.add('commentSetChild')
                spanElement_setChild.innerHTML = '답글등록'
                spanElement_setChild.onclick = function(){
                    commentTextarea.style['display'] = ''
                    commentInputBtn.style['display'] = ''
                }
                liElement.appendChild(spanElement_setChild)

                childCommentUl.id = "childComment_" + result[i][0]
                childCommentUl.classList.add("subCommentUl")
                liElement.appendChild(childCommentUl)
                
                commentTextarea.id = "commentTextarea" + result[i][0]
                commentTextarea.classList.add("commentTextarea")
                commentTextarea.style['display'] = 'none'
                commentTextarea.addEventListener('input',()=>{
                commentInputBtn.innerHTML = '등록 (' + commentTextarea.value.length + '/1000 자)'
                })
                liElement.appendChild(commentTextarea)
                
                commentInputBtn.id = "commentInputBtn" + result[i][0]
                commentInputBtn.classList.add("commentInputBtn")
                commentInputBtn.innerHTML = '등록 (0/1000자)'
                commentInputBtn.onclick = function(){
                    insertComment(result[i][0])
                    commentTextarea.style['display'] = 'none'
                    commentInputBtn.style['display'] = 'none'
                }
                commentInputBtn.style['display'] = 'none'
                liElement.appendChild(commentInputBtn)
                
                commentParentDiv.appendChild(liElement)
            }
        });
}

/**
 * 대댓글 가져와서 element 추가
 * @param upperNo
 */
function getChildComment(upperNo){
    let getChildBtn = document.getElementById('getChildBtn_'+upperNo)
    let bno = boardNoDiv.innerHTML
    let tempString = getChildBtn.innerHTML
    let url = '/getChildComment'
    getChildBtn.innerHTML = '<span class="spiner">🌀</span>'
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: bno,
            upperNo: upperNo
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            let childCommentUl = document.getElementById('childComment_' + upperNo)
            childCommentUl.innerHTML=''
            for(let i=0;i<result.length;i++){
                let liElement = document.createElement('li')
                let spanElement_email = document.createElement('span')
                let spanElement_ip = document.createElement('span')
                let spanElement_date = document.createElement('span')
                let spanElement_contents = document.createElement('span')
                
                spanElement_email.classList.add('commentEmail')
                spanElement_email.onclick = function(){
                    window.location.href='/user/' + result[i][2]
                }
                spanElement_email.innerHTML = result[i][8]
                liElement.appendChild(spanElement_email)
                
                spanElement_ip.classList.add('commentIp')
                spanElement_ip.innerHTML = '(' + result[i][3] + ')'
                liElement.appendChild(spanElement_ip)
                
                spanElement_date.classList.add('commentDate')
                spanElement_date.innerHTML = result[i][5]
                liElement.appendChild(spanElement_date)
                
                spanElement_contents.classList.add('commentContents')
                spanElement_contents.innerHTML = result[i][4]
                if(result[i][7] == 1){
                    spanElement_contents.classList.add('deleted')
                }else if(result[i][11]){
                    let removeBtn = document.createElement('span')
                    removeBtn.classList.add('commentRemove')
                    removeBtn.innerHTML = '삭제'
                    removeBtn.onclick = function(){
                        removeComment(result[i][0])
                    }
                    spanElement_contents.appendChild(removeBtn)
                }
                liElement.appendChild(spanElement_contents)
                
                childCommentUl.appendChild(liElement)
            }
        });
        getChildBtn.innerHTML = tempString
}

/**
 * 댓글 작성기능(upperNo가 0이면 최상위 댓글)
 * @param upperNo 
 */
function insertComment(upperNo){
    comment = ''
    commentTextarea = ''
    commentInputBtn = ''
    if(upperNo == 0){
        commentInputBtn = document.getElementById('commentInputBtn')
        commentTextarea = document.getElementById('commentTextarea')
        comment = commentTextarea.value.trim()
    }else{
        commentInputBtn = document.getElementById('commentInputBtn' + upperNo)
        commentTextarea = document.getElementById('commentTextarea' + upperNo)
        comment = commentTextarea.value.trim()
    }
    if(comment == ''){
        return
    }
    bno = boardNoDiv.innerHTML
    let tempString = commentInputBtn.innerHTML
    let url = '/insertComment'
    commentInputBtn.innerHTML = '<span class="spiner">🌀</span>'
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: bno,
            upperNo: upperNo,
            comment: comment
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result[0]){
                commentTextarea.value = ''
                commentInputBtn.innerHTML = '등록 (0/1000자)'
                if(upperNo==0){
                    getParentComment()
                }else{
                    getChildComment(upperNo)
                }
            }else{
                alert(result[1])
            }
        });
        commentInputBtn.innerHTML = tempString
}

/**
 * 댓글 삭제 기능
 * @param cono 
 */
function removeComment(cono){
    let url = '/deleteComment'
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            cono: cono
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result[0]){
                getParentComment()
            }else{
                alert(result[1])
            }
        });
}


// 이벤트 리스너
commentTextarea.addEventListener('input',()=>{
    commentInputBtn.innerHTML = '등록 (' + commentTextarea.value.length + '/1000 자)'
})

// 초기 실행
setCateList(nowPageDiv.innerHTML)
getParentComment()