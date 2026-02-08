let adminCheckImageBtn = document.getElementById('adminCheckImageBtn')
let adminDeleteDummyBtn = document.getElementById('adminDeleteDummyBtn')
let adminRebootBtn = document.getElementById('adminRebootBtn')
let adminNoticeTextarea = document.getElementById('adminNoticeTextarea')
let adminNoticeBtn = document.getElementById('adminNoticeBtn')
let adminCategoryDiv = document.getElementById('adminCategoryDiv')
let adminCateBtn = document.getElementById('adminCateBtn')

adminCheckImageBtn.addEventListener('click',()=>{
    fetch("/adminCheckImage", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            alert('현재는 기능이 동작하지 않도록 설정되어 있습니다. 반환값: ' + result)
            // alert(result + '개의 파일이 정리되었습니다.')
        });
})
adminDeleteDummyBtn.addEventListener('click',()=>{
    fetch("/adminDeleteDummy", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            alert('현재는 기능이 동작하지 않도록 설정되어 있습니다. 반환값: ' + result)
            // alert(result + '개의 파일이 삭제되었습니다.')
        });
})
adminRebootBtn.addEventListener('click',()=>{
    fetch("/adminReboot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            
        }),
        })
    alert('현재는 기능이 동작하지 않도록 설정되어 있습니다.')
})

adminNoticeBtn.addEventListener('click',()=>{
    let newNotice = adminNoticeTextarea.value
    fetch("/adminModNotice", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            notice: newNotice
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(!result){
                adminNoticeTextarea.value = adminNoticeTextarea.innerHTML
                alert('공지 변경 실패')
            }
        });
})

function setCateId(){
    target = adminCategoryDiv.children
    for(let i in target){
        if(i == target.length-1){
            target[i].id = "parent_new"
        }else{
            let targetIdStr = String(target[i].id)
            target[i].id = targetIdStr.slice(0,targetIdStr.lastIndexOf('_')) + '_' + (parseInt(i)+1)
            let childrenCate = target[i].children[1]
            targetIdStr = String(childrenCate.id)
            childrenCate.id = targetIdStr.slice(0,targetIdStr.lastIndexOf('_')) + '_' + (parseInt(i)+1)
            let targetChildrenDivList = childrenCate.children
            for(let j in targetChildrenDivList){
                targetIdStr = String(targetChildrenDivList[j].id)
                targetChildrenDivList[j].id = targetIdStr.slice(0,targetIdStr.lastIndexOf('_')) + '_' + (parseInt(j)+1)
                
            }
            targetIdStr = String(target[i].children[2].id)
            target[i].children[2].id = targetIdStr.slice(0,targetIdStr.lastIndexOf('_')) + '_' + (parseInt(i)+1)
        }
    }
}

function changeParentCategoryName(target){
    let newName = prompt("변경할 카테고리명")
    let childenList = target.cloneNode(true).children
    childenList[0].innerHTML=newName
    target.innerHTML=''
    while(childenList.length != 0){
        target.appendChild(childenList[0])
        target.innerHTML += ' '
    }
}

function changeChildCategoryName(target){
    let newName = prompt("변경할 카테고리명")
    let childenList = target.cloneNode(true).children
    let count = childenList[0].innerHTML.split('(')[1]
    childenList[0].innerHTML=newName + '(' + count
    target.innerHTML=''
    while(childenList.length != 0){
        target.appendChild(childenList[0])
        target.innerHTML += ' '
    }
}

function moveParentCategoryDiv(parentDiv_id,heading){
    let parentChildrenList = Array.from(adminCategoryDiv.children)
    let fromIndex = parseInt(parentDiv_id.split('_')[1]) - 1
    let toIndex = 0
    if(heading == 'up'){
        if(fromIndex === 0){
            return
        }
        toIndex = fromIndex - 1
    }else{
        if(fromIndex >= parentChildrenList.length-2){
            return
        }
        toIndex = fromIndex +1
    }
    adminCategoryDiv.innerHTML = ''
    for(let i=0;i<parentChildrenList.length;i++){
        if(i==toIndex){
            adminCategoryDiv.appendChild(parentChildrenList[fromIndex])
        }else if(i==fromIndex){
            adminCategoryDiv.appendChild(parentChildrenList[toIndex])
        }else{
            adminCategoryDiv.appendChild(parentChildrenList[i])
        }
    }
    setCateId()
}

function moveChildCategoryDiv(childDiv_id,heading){
    let childDiv = document.getElementById(childDiv_id).parentElement
    let childChildrenList = Array.from(childDiv.children)
    let fromIndex = parseInt(childDiv_id.split('_')[3])-1
    let toIndex = 0
    if(heading == 'up'){
        if(fromIndex === 0){
            return
        }
        toIndex = fromIndex - 1
    }else{
        if(fromIndex >= childChildrenList.length-1){
            return
        }
        toIndex = fromIndex +1
    }
    childDiv.innerHTML = ''
    for(let i=0;i<childChildrenList.length;i++){
        if(i==toIndex){
            childDiv.appendChild(childChildrenList[fromIndex])
        }else if(i==fromIndex){
            childDiv.appendChild(childChildrenList[toIndex])
        }else{
            childDiv.appendChild(childChildrenList[i])
        }
    }
    setCateId()
}

function deleteCategory(target){
    if(confirm("카테고리에 저장된 글이 모두 삭제됩니다.")){
        target.remove()
    }
    setCateId()
}

function newParentCategory(){
    let targetDiv = adminCategoryDiv
    let cateName = prompt('생성할 카테고리 명')
    let cateOrder = targetDiv.children.length
    if(cateName == ''){
        return
    }

    let newCateNameSpan = document.createElement('span')
    newCateNameSpan.innerHTML = cateName
    let newCateModSpan = document.createElement('span')
    newCateModSpan.classList.add('adminChildPointer')
    newCateModSpan.innerHTML = '✏️'
    newCateModSpan.onclick = function(){
        changeParentCategoryName(this.parentElement)
    }
    let newCateDelSpan = document.createElement('span')
    newCateDelSpan.classList.add('adminChildPointer')
    newCateDelSpan.innerHTML = '❌'
    newCateDelSpan.onclick = function(){
        deleteCategory(this.parentElement.parentElement)
    }
    let newCateUpSpan = document.createElement('span')
    newCateUpSpan.classList.add('adminChildPointer')
    newCateUpSpan.innerHTML = '⬆️'
    newCateUpSpan.onclick = function(){
        moveParentCategoryDiv(this.parentElement.parentElement.id,'up')
    }
    let newCateDownSpan = document.createElement('span')
    newCateDownSpan.classList.add('adminChildPointer')
    newCateDownSpan.innerHTML = '⬇️'
    newCateDownSpan.onclick = function(){
        moveParentCategoryDiv(this.parentElement.parentElement.id,'down')
    }

    let newCateNameDiv = document.createElement('div')
    newCateNameDiv.id = "parentName_new" + cateOrder
    newCateNameDiv.classList.add('adminParentName')
    newCateNameDiv.appendChild(newCateNameSpan)
    newCateNameDiv.appendChild(newCateModSpan)
    newCateNameDiv.appendChild(newCateDelSpan)
    newCateNameDiv.appendChild(newCateUpSpan)
    newCateNameDiv.appendChild(newCateDownSpan)

    let newChildDiv = document.createElement('div')
    newChildDiv.id = "child_" + cateOrder

    let newChildNewDiv = document.createElement('div')
    newChildNewDiv.id = "child_new_" + cateOrder
    newChildNewDiv.classList.add('adminChildPointer')
    newChildNewDiv.classList.add('child_new')
    newChildNewDiv.innerHTML = "+"
    newChildNewDiv.onclick = function(){
        newChildCategory(this)
    }

    let newCateDiv = document.createElement('div')
    newCateDiv.id = "parent_" + cateOrder
    newCateDiv.classList.add('adminParentCateDiv')
    newCateDiv.appendChild(newCateNameDiv)
    newCateDiv.appendChild(newChildDiv)
    newCateDiv.appendChild(newChildNewDiv)

    targetDiv.insertBefore(newCateDiv,document.getElementById('parent_new'))
    setCateId()
}

function newChildCategory(clickedBtn){
    let targetDiv = clickedBtn.parentElement.children[1]
    let cateOrder = targetDiv.children.length + 1
    let parent_no = clickedBtn.parentElement.children[0].id.split('_')[1]
    let cateName = prompt('생성할 카테고리 명')
    if(cateName == ''){
        return
    }

    let newCateNameSpan = document.createElement('span')
    newCateNameSpan.innerHTML = cateName + "(new)"
    let newCateModSpan = document.createElement('span')
    newCateModSpan.classList.add('adminChildPointer')
    newCateModSpan.innerHTML = '✏️'
    newCateModSpan.onclick = function(){
        changeChildCategoryName(this.parentElement)
    }
    let newCateDelSpan = document.createElement('span')
    newCateDelSpan.classList.add('adminChildPointer')
    newCateDelSpan.innerHTML = '❌'
    newCateDelSpan.onclick = function(){
        deleteCategory(this.parentElement.parentElement)
    }
    let newCateUpSpan = document.createElement('span')
    newCateUpSpan.classList.add('adminChildPointer')
    newCateUpSpan.innerHTML = '⬆️'
    newCateUpSpan.onclick = function(){
        moveChildCategoryDiv(this.parentElement.id,'up')
    }
    let newCateDownSpan = document.createElement('span')
    newCateDownSpan.classList.add('adminChildPointer')
    newCateDownSpan.innerHTML = '⬇️'
    newCateDownSpan.onclick = function(){
        moveChildCategoryDiv(this.parentElement.id,'down')
    }

    let newCateDiv = document.createElement('div')
    newCateDiv.id = "childName_" + parent_no + "_new_" + cateOrder
    newCateDiv.classList.add('adminChildName')
    newCateDiv.appendChild(newCateNameSpan)
    newCateDiv.appendChild(newCateModSpan)
    newCateDiv.appendChild(newCateDelSpan)
    newCateDiv.appendChild(newCateUpSpan)
    newCateDiv.appendChild(newCateDownSpan)

    targetDiv.appendChild(newCateDiv)
    setCateId()
}

adminCateBtn.addEventListener('click',()=>{
    function getDTOList(parentList){
        let result = []
        for(let i=0;i<parentList.length;i++){
            if(parentList[i].id == 'parent_new'){
                continue
            }
            let parentDTOList = []
            let p_cno = parentList[i].children[0].id.split('_')[1]
            let p_cname = parentList[i].children[0].children[0].innerHTML
            let p_cupper = ""
            let p_corder = parentList[i].id.split('_')[1]
            let p_dto = [p_cno,p_cname,p_cupper,p_corder]
            parentDTOList.push(p_dto)

            let childList = parentList[i].children[1].children
            let childDTOList = []
            for(let j=0;j<childList.length;j++){
                let c_cno = childList[j].id.split('_')[2]
                let c_cname = childList[j].children[0].innerHTML.split('(')[0]
                let c_cupper = childList[j].id.split('_')[1]
                let c_corder = childList[j].id.split('_')[3]
                let c_dto = [c_cno,c_cname,c_cupper,c_corder]
                childDTOList.push(c_dto)
            }
            parentDTOList.push(childDTOList)
            result.push(parentDTOList)
        }
        return result
    }
    setCateId()
    let parentList = adminCategoryDiv.children
    let dtoList = getDTOList(parentList)
    fetch("/adminModCate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            dtoList: dtoList
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result){
                window.location.href = '/admin'
            }else{
                alert('카테고리 변경에 실패하였습니다.')
            }
        });
}) 