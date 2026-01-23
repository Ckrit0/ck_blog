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

/**
 * 이메일 정규식 검사
 */
function checkEmailRegex(){
    let pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    let email = joinEmailInput.value
    if(pattern.test(email)){
        turnActive(joinEmailBtn)
    }else{
        turnDisabled(joinEmailBtn)
    }
}

/**
 * 비밀번호 정규식 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
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

/**
 * 비밀번호 확인 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
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

/**
 * 이메일 확인 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
function checkUseEmail(){
    if(joinEmailBtn.innerHTML == '✅'){
        return true
    }else{
        return false
    }
}

/**
 * 인증 코드 확인 검사
 * @returns 성공이면 true, 실패이면 false (boolean)
 */
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

/**
 * 이메일 입력 검사
 */
joinEmailInput.addEventListener('input',()=>{
    checkEmailRegex()
})

/**
 * 엔터키로 이메일 확인 버튼 클릭
 */
joinEmailInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinEmailBtn.click()
    }
})

/**
 * 이메일 중복 확인 요청
 */
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

/**
 * 비밀번호 정규식 검사
 */
joinPwInput.addEventListener('input',()=>{
    checkPwRegex()
})

/**
 * 엔터키로 다음 input으로 이동
 */
joinPwInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinConfirmInput.focus()
    }
})

/**
 * 비밀번호 확인 검사
 */
joinConfirmInput.addEventListener('input',()=>{
    checkConfirm()
})

/**
 * 엔터키로 가입하기 버튼 클릭
 */
joinConfirmInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinCommitBtn.click()
    }
})

/**
 * 엔터키로 인증 코드 확인 버튼 클릭
 */
joinVerifyInput.addEventListener('keydown',(e)=>{
    if(e.key=="Enter"){
        joinVerifyCheckBtn.click()
    }
})

/**
 * 인증 코드 메일 발송 요청
 */
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
            alert(result[1])
            if(result[0] == 15){
                turnActive(joinVerifyInput)
                turnActive(joinVerifyCheckBtn)
                turnDisabled(joinVerifySendBtn)
                joinVerifyInput.focus()
            }
            joinVerifySendBtn.innerHTML = 'send'
        });
})

/**
 * 인증 코드 확인 요청
 */
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
                alert(result[1])
                if(result[0] == 11){
                    joinVerifyCheckBtn.innerHTML = '<span id="joinVerifyCheckBtn" class="joinWarning joinChecked">✅</span>'
                    turnDisabled(joinVerifyInput)
                }else if(result[0] == 13){
                    verifyReset()
                }else{
                    turnDisabled(joinVerifyCheckBtn)                 
                    verifyReset()                 
                }
            });
})

/**
 * 가입하기 버튼 클릭
 */
joinCommitBtn.addEventListener('click',()=>{
    joinCommitBtn.innerHTML = joinBtnSpiner
    turnActive(joinEmailInput)
    turnActive(joinVerifyInput)
    document.getElementById('joinForm').submit()
})

/**
 * 초기 포커스 이메일 input
 */
joinEmailInput.focus()