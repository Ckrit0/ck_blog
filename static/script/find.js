let findForm = document.getElementById('findForm')
let findEmailInput = document.getElementById('findEmailInput')
let findCodeInput = document.getElementById('findCodeInput')
let findSendBtn = document.getElementById('findSendBtn')
let findCheckBtn = document.getElementById('findCheckBtn')
let findPwInput = document.getElementById('findPwInput')
let findPwDiv = document.getElementById('findPwDiv')
let findConfirmInput = document.getElementById('findConfirmInput')
let findConfirmDiv = document.getElementById('findConfirmDiv')
let findSubmitBtn = document.getElementById('findSubmitBtn')
let findCancelBtn = document.getElementById('findCancelBtn')

/**
 * 비밀번호 정규식 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
function checkPwRegex(){
    let pattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/
    let pw = findPwInput.value
    if(findConfirmInput.value != ''){
        checkConfirm()
    }
    if(pattern.test(pw)){
        findPwDiv.innerHTML = '✅'
    }else{
        findPwDiv.innerHTML = '영어,숫자,특수문자 포함된 8~16자리로 설정'
    }
}

/**
 * 비밀번호 확인 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
function checkConfirm(){
    let pw = findPwInput.value
    let confirm = findConfirmInput.value
    let pattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/
    if(pw === confirm){
        findConfirmDiv.innerHTML = '✅'
        if(pattern.test(confirm)){
            turnActive(findSubmitBtn)
        }
    }else{
        findConfirmDiv.innerHTML = '비밀번호가 다릅니다.'
    }
}

/**
 * 인증 코드 메일 발송 요청
 */
findSendBtn.addEventListener('click',()=>{
    findSendBtn.innerHTML = '<span class="spiner">🌀</span>'
    fetch("/sendMail", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: findEmailInput.value
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result[0] == 15){
                turnDisabled(findEmailInput)
                turnActive(findCodeInput)
                turnDisabled(findSendBtn)
                turnActive(findCheckBtn)
                findCodeInput.focus()
                findSendBtn.innerHTML = '발송완료'
                alert(result[1])
            }else{
                findSendBtn.innerHTML = '메일발송'
                alert(result[1])
            }
        });
})

/**
 * 인증 코드 확인 요청
 */
findCheckBtn.addEventListener('click',()=>{
    findCheckBtn.innerHTML = '<span class="spiner">🌀</span>'
    fetch("/matchVerify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: findEmailInput.value,
                verify: findCodeInput.value
            }),
            })
            .then((response) => response.json())
            .then((result) => {
                function verifyReset(){
                    findCheckBtn.innerHTML = '코드확인'
                    findSendBtn.innerHTML = '메일발송'
                    turnActive(findEmailInput)
                    turnActive(findSendBtn)
                    turnDisabled(findCodeInput)
                }
                alert(result[1])
                if(result[0] == 11){
                    findCheckBtn.innerHTML = '코드일치'
                    turnDisabled(findCodeInput)
                    turnDisabled(findCheckBtn)
                    turnActive(findPwInput)
                    turnActive(findConfirmInput)
                    findPwInput.focus()
                }else if(result[0] == 13){
                    verifyReset()
                }else{
                    turnDisabled(findCheckBtn)                 
                    verifyReset()                 
                }
            });
})

/**
 * 비밀번호 변경 버튼 클릭
 */
findSubmitBtn.addEventListener('click',()=>{
    findSubmitBtn.innerHTML = '<span class="spiner">🌀</span>'
    turnActive(findEmailInput)
    turnActive(findCodeInput)
    findForm.submit()
})

/* 이벤트 리스너 */
findEmailInput.addEventListener('keydown',(e)=>{
    if(e.key == 'Enter'){
        findSendBtn.click()
    }
})

findCodeInput.addEventListener('keydown',(e)=>{
    if(e.key == 'Enter'){
        findCheckBtn.click()
    }
})

findPwInput.addEventListener('input',()=>{
    checkPwRegex()
})

findConfirmInput.addEventListener('input',()=>{
    checkConfirm()
})

/**
 * 초기 포커스 이메일 input
 */
findEmailInput.focus()