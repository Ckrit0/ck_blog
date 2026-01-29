let searchInput = document.getElementById('searchInput')
let searchBtn = document.getElementById('searchBtn')

/**
 * 검색 관련
 */
searchInput.addEventListener('keydown',(e)=>{
    if(e.key == "Enter"){
        searchBtn.click()
    }
})

searchBtn.onclick = function(){
    let keyword = searchInput.value.trim()
    while(keyword.indexOf('  ') >= 0){
        keyword = keyword.replaceAll('  ',' ')
    }
    if(keyword.replaceAll(' ','').length == 0){
        return
    }else if(keyword.replaceAll(' ','').length < 2){
        alert("검색은 최소 2글자 이상 입력해야합니다.(공백 제외)")
        return
    }
    window.location.href = '/search/' + keyword
}