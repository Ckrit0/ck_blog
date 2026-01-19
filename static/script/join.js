joinEmailInput = document.getElementById('joinEmailInput')
joinEmailBtn = document.getElementById('joinEmailBtn')
joinPwInput = document.getElementById('joinPwInput')
joinPwCheck = document.getElementById('joinPwCheck')
joinConfirmInput = document.getElementById('joinConfirmInput')
joinConfirmCheck = document.getElementById('joinConfirmCheck')
joinVerifyInput = document.getElementById('joinVerifyInput')
joinVerifySendBtn = document.getElementById('joinVerifySendBtn')
joinVerifyCheckBtn = document.getElementById('joinVerifyCheckBtn')
joinCommitBtn = document.getElementById('joinCommit')

function checkEmailRegex(email){
    let pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return pattern.test(email)
}

function checkPwRegex(pw){
    let pattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/
    return pattern.test(pw)
}

function checkConfirm(pw,confirm){
    return pw === confirm
}

joinEmailInput.addEventListener('input',()=>{
    if(checkEmailRegex(joinEmailInput.value)){
        turnActive(joinEmailBtn)
    }else{
        turnDisabled(joinEmailBtn)
    }
})

joinEmailBtn.addEventListener('click',()=>{
    
})

joinPwInput.addEventListener('input',()=>{
    if(checkPwRegex(joinPwInput.value)){
        joinPwCheck.innerHTML = '✅'
    }else{
        joinPwCheck.innerHTML = '영어,숫자,특수문자 포함된 8~16자리로 설정'
    }
    if(joinConfirmInput.value != ''){
        if(checkConfirm(joinPwInput.value, joinConfirmInput.value)){
            joinConfirmCheck.innerHTML = '✅'
        }else{
            joinConfirmCheck.innerHTML = '비밀번호가 다릅니다.'
        }
    }
})

joinConfirmInput.addEventListener('input',()=>{
    if(checkConfirm(joinPwInput.value, joinConfirmInput.value)){
        joinConfirmCheck.innerHTML = '✅'
    }else{
        joinConfirmCheck.innerHTML = '비밀번호가 다릅니다.'
    }
})

joinVerifySendBtn.addEventListener('click',()=>{

})

joinVerifyCheckBtn.addEventListener('click',()=>{

})

joinEmailInput.focus()