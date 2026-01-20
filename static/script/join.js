let joinEmailInput = document.getElementById('joinEmailInput')
let joinEmailBtn = document.getElementById('joinEmailBtn')
let joinPwInput = document.getElementById('joinPwInput')
let joinPwCheck = document.getElementById('joinPwCheck')
let joinConfirmInput = document.getElementById('joinConfirmInput')
let joinConfirmCheck = document.getElementById('joinConfirmCheck')
let joinVerifyInput = document.getElementById('joinVerifyInput')
let joinVerifySendBtn = document.getElementById('joinVerifySendBtn')
let joinVerifyCheckBtn = document.getElementById('joinVerifyCheckBtn')
let joinInfoDiv = document.getElementById('joinInfoDiv')
let joinCommitBtn = document.getElementById('joinCommit')

let joinBtnSpiner = '<span class="spiner">🌀</span>'

function checkEmailRegex(){
    let pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    let email = joinEmailInput.value
    if(pattern.test(email)){
        turnActive(joinEmailBtn)
    }else{
        turnDisabled(joinEmailBtn)
    }
}

function checkPwRegex(){
    let pattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/
    let pw = joinPwInput.value
    if(joinConfirmInput.value != ''){
        checkConfirm()
    }
    if(pattern.test(pw)){
        joinPwCheck.innerHTML = '<span class="joinChecked">✅</span>'
        return true
    }else{
        joinPwCheck.innerHTML = '영어,숫자,특수문자 포함된 8~16자리로 설정'
        return false
    }
}

function checkConfirm(){
    let pw = joinPwInput.value
    let confirm = joinConfirmInput.value
    if(pw === confirm){
        joinConfirmCheck.innerHTML = '<span class="joinChecked">✅</span>'
        return true
    }else{
        joinConfirmCheck.innerHTML = '비밀번호가 다릅니다.'
        return false
    }
}

function checkUseEmail(){
    if(joinEmailBtn.innerHTML == '✅'){
        return true
    }else{
        return false
    }
}

function checkVerify(){
    if(joinInfoDiv.innerHTML == '강제 가입의 경우 verify(메일 인증)을 완료해야 가입이 가능합니다.'){
        if(joinVerifyCheckBtn.innerHTML == '✅'){
            return true
        }else{
            return false
        }
    }else{
        return true
    }
}

joinEmailInput.addEventListener('input',()=>{
    checkEmailRegex()
})

joinEmailInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinEmailBtn.click()
    }
})

joinEmailBtn.addEventListener('click',()=>{
    joinEmailBtn.innerHTML = joinBtnSpiner
    fetch("/checkMail", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            joinEmail: joinEmailInput.value
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            function joinContinueCheckEmail(){
                joinEmailBtn.innerHTML = '✅'
                turnDisabled(joinEmailInput)
                turnActive(joinVerifySendBtn)
                turnActive(joinCommitBtn)
                joinPwInput.focus()
            }
            if(result.length == 0){
                joinContinueCheckEmail()
                turnActive(joinCommitBtn)
                joinEmailInput.focus()
            }else{
                joinEmailBtn.innerHTML = 'check'
                if(confirm(result[0][3] + '일에 가입한 아이디가 있습니다. 이전 아이디를 삭제하고 새로 가입하시겠습니까? (인증 필수)')){
                    joinContinueCheckEmail()
                    joinInfoDiv.innerHTML = '강제 가입의 경우 verify(메일 인증)을 완료해야 가입이 가능합니다.'
                    turnActive(joinCommitBtn)
                }else{
                    history.back()
                }
            }
        });
})

joinPwInput.addEventListener('input',()=>{
    checkPwRegex()
})

joinPwInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinConfirmInput.focus()
    }
})

joinConfirmInput.addEventListener('input',()=>{
    checkConfirm()
})

joinConfirmInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinCommitBtn.click()
    }
})

joinVerifyInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinVerifyCheckBtn.click()
    }
})

joinVerifySendBtn.addEventListener('click',()=>{
    joinVerifySendBtn.innerHTML = joinBtnSpiner
    fetch("/sendMail", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            joinEmail: joinEmailInput.value
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result == 4){
                joinVerifySendBtn.innerHTML = 'sent'
                turnActive(joinVerifyInput)
                turnActive(joinVerifyCheckBtn)
                turnDisabled(joinVerifySendBtn)
                joinVerifyInput.focus()
                alert('메일이 발송되었습니다. 인증코드는 10분이 지나면 사용이 불가능합니다.')
            }else{
                joinVerifySendBtn.innerHTML = 'send'
                alert('메일 발송에 실패하였습니다.')
            }
        });
})

joinVerifyCheckBtn.addEventListener('click',()=>{
    joinVerifyCheckBtn.innerHTML = joinBtnSpiner
    fetch("/matchVerify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                joinEmail: joinEmailInput.value,
                joinVerify: joinVerifyInput.value
            }),
            })
            .then((response) => response.json())
            .then((result) => {
                function verifyReset(){
                    joinVerifyCheckBtn.innerHTML = 'check'
                    joinVerifySendBtn.innerHTML = 'send'
                    turnActive(joinVerifySendBtn)
                }
                if(result == 0){
                    joinVerifyCheckBtn.innerHTML = '<span id="joinVerifyCheckBtn" class="joinWarning joinChecked">✅</span>'
                    turnDisabled(joinVerifyInput)
                }else if(result == 1){
                    verifyReset()
                    turnDisabled(joinVerifyCheckBtn)
                    alert('발급된 코드가 없습니다. 메일 재발송 부탁드립니다.')
                }else if(result == 2){
                    verifyReset()
                    alert('코드가 일치하지 않습니다. 대소문자를 구분하니 주의 부탁드립니다.')
                }else if(result == 3){
                    verifyReset()
                    turnDisabled(joinVerifyCheckBtn)
                    alert('시간이 만료되었습니다. 메일 재발송 부탁드립니다.')
                }
            });
})

joinCommitBtn.addEventListener('click',()=>{
    joinCommitBtn.innerHTML = joinBtnSpiner
    turnActive(joinEmailInput)
    turnActive(joinVerifyInput)
    document.getElementById('joinForm').submit()
})

joinEmailInput.focus()