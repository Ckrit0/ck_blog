let adminCheckImageBtn = document.getElementById('adminCheckImageBtn')
let adminDeleteDummyBtn = document.getElementById('adminDeleteDummyBtn')
let adminRebootBtn = document.getElementById('adminRebootBtn')
let adminNoticeTextarea = document.getElementById('adminNoticeTextarea')
let adminNoticeBtn = document.getElementById('adminNoticeBtn')

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