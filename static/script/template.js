let searchInput = document.getElementById('searchInput')
let searchBtn = document.getElementById('searchBtn')
let sidebarBtn = document.getElementById('sidebarBtn')
let sidebar = document.getElementById('sidebar')

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

/**
 * 미디어쿼리 사이드바
 */
let isMenuOpen = false;
function toggleMenu(){
    isMenuOpen = !isMenuOpen
    console.log(isMenuOpen)
    if(isMenuOpen){
        sidebar.style.display = ''
    }else{
        sidebar.style.display = 'none'
    }
}

sidebarBtn.addEventListener('click', toggleMenu)

function checkViewport() {
    if (window.innerWidth <= 805) {
        if(!isMenuOpen){
            sidebar.style.display = 'none'
        }else{
            sidebar.style.display = ''
        }
        sidebarBtn.style.display = ''
        
    } else {
        sidebar.style.display = ''
        sidebarBtn.style.display = 'none'
        isMenuOpen = false
    }
}
window.addEventListener('resize', checkViewport);

checkViewport(); // 초기 실행