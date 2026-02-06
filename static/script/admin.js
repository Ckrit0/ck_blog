let adminCheckImageBtn = document.getElementById('adminCheckImageBtn')
let adminDeleteDummyBtn = document.getElementById('adminDeleteDummyBtn')
let adminRebootBtn = document.getElementById('adminRebootBtn')
let adminNoticeTextarea = document.getElementById('adminNoticeTextarea')
let adminNoticeBtn = document.getElementById('adminNoticeBtn')
let adminCategoryDiv = document.getElementById('adminCategoryDiv')

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

function changeCategoryName(target){
    let newName = prompt("해당 카테고리의 새로운 이름")
    let childenList = target.cloneNode(true).children
    if(childenList[0].innerHTML.indexOf('(') != 0){
        let count = childenList[0].innerHTML.split('(')[1]
        childenList[0].innerHTML=newName + '(' + count
    }else{
        childenList[0].innerHTML=newName
    }
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
            parentChildrenList[fromIndex].id = "parent_" + (toIndex + 1)
            adminCategoryDiv.appendChild(parentChildrenList[fromIndex])
        }else if(i==fromIndex){
            parentChildrenList[toIndex].id = "parent_" + (fromIndex + 1)
            adminCategoryDiv.appendChild(parentChildrenList[toIndex])
        }else{
            adminCategoryDiv.appendChild(parentChildrenList[i])
        }
    }
}

function moveChildCategoryDiv(parentDiv_id,heading){
    let grandParentDiv = document.getElementById(parentDiv_id).parentElement
    let parentChildrenList = Array.from(adminCategoryDiv.children)
    let idTextList = parentDiv_id.split('_')
    let fromIndex = parseInt(idTextList[4]) - 1
    let toIndex = 0
    let idText = idTextList[0] + '_' + idTextList[1] + '_' + idTextList[2] + '_' + idTextList[3] + '_'
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
    grandParentDiv.innerHTML = ''
    for(let i=0;i<parentChildrenList.length;i++){
        if(i==toIndex){
            parentChildrenList[fromIndex].id = idText + (toIndex + 1)
            grandParentDiv.appendChild(parentChildrenList[fromIndex])
        }else if(i==fromIndex){
            parentChildrenList[toIndex].id = idText + (fromIndex + 1)
            grandParentDiv.appendChild(parentChildrenList[toIndex])
        }else{
            grandParentDiv.appendChild(parentChildrenList[i])
        }
    }
}

function deleteCategory(target){
    if(confirm("카테고리에 저장된 글이 모두 삭제됩니다.")){
        target.remove()
    }
}