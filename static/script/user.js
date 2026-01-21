let userLeaveBtn = document.getElementById('userLeaveBtn')

userLeaveBtn.addEventListener('click',()=>{
    if(!confirm('정말 탈퇴하시겠습니까?')){
        return
    }
    let userPw = prompt('탈퇴하시려면 비밀번호를 입력해주세요.')
    if(userPw == ''){
        return
    }
    let userEmail = document.getElementById('userEmail').innerText.split('(')[0]
    fetch("/leave", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            userEmail : userEmail,
            userPw : userPw
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result == 10){
                window.location.href='/'
                alert('회원 탈퇴에 성공하였습니다.')
            }else if(result == 7){
                alert('비밀번호가 틀렸습니다.')
            }else{
                alert('회원 탈퇴에 실패하였습니다.')
            }
            return
        });
})


function userModalInit(){
    /* changePwModal */
    let changePwOpenBtn = document.getElementById('changePwOpenBtn')
    let changePwModal = document.getElementById('changePwModal')
    let userNowPwInput = document.getElementById('userNowPw')
    let userNewPwInput = document.getElementById('userNewPw')
    let userNewConfirmInput = document.getElementById('userNewConfirm')
    let userChangePwInfo = document.getElementById('userChangePwInfo')
    let changePwSubmitBtn = document.getElementById('changePwSubmitBtn')
    let changePwCancelBtn = document.getElementById('changePwCancelBtn')

    function resetPwModal(){
        userNowPwInput.value = ''
        userNewPwInput.value = ''
        userNewConfirmInput.value = ''
        userChangePwInfo.value = '영어,숫자,특수문자 포함된 8~16자리로 설정'
        changePwModal.style['display'] = 'none'
    }

    changePwOpenBtn.addEventListener('click',()=>{
        changePwModal.style['display'] = 'inline-grid'
        resetVerifyModal()
    })

    userNowPwInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            userNewPwInput.focus()
        }
    })

    userNewPwInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            userNewConfirmInput.focus()
        }
    })


    userNewConfirmInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            changePwSubmitBtn.click()
        }
    })

    changePwSubmitBtn.addEventListener('click',()=>{
        changePwSubmitBtn.innerHTML = '<span class="spiner">🌀</span>'
        let userNowPw = userNowPwInput.value
        let userNewPw = userNewPwInput.value
        let userNewConfirm = userNewConfirmInput.value

        if(userNowPw == ''){
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        }else if(userNewPw == ''){
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        }else if(userNewConfirm == ''){
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        }else if(userNewPw != userNewConfirm){
            alert('비밀번호와 비밀번호 확인이 다릅니다.')
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        }else if(userNowPw == userNewPw){
            alert('사용중인 비밀번호와 같습니다.')
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        }

        fetch("/changePw", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            userNowPw : userNowPw,
            userNewPw : userNewPw,
            userNewConfirm: userNewConfirm
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            if(result == 8){
                alert('비밀번호가 변경되었습니다.')
                resetPwModal()
            }else if(result == 2){
                alert('비밀번호 형식이 잘못되었습니다.')
            }else if(result == 3){
                alert('비밀번호와 확인이 서로 다릅니다.')
            }else if(result == 7){
                alert('사용중인 비밀번호가 틀렸습니다.')
            }else if(result == 9){
                alert('사용중인 비밀번호와 같습니다.')
            }else if(result == 998){
                alert('알 수 없는 이유로 변경에 실패하였습니다.')
            }
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        });
    })

    changePwCancelBtn.addEventListener('click',()=>{
        resetPwModal()
    })

    /* userVerifyModal */
    let userVerifyOpenBtn = document.getElementById('userVerifyOpenBtn')
    let userVerifyModal = document.getElementById('userVerifyModal')
    let userVerifyInput = document.getElementById('userVerifyInput')
    let userVerifyConfirmBtn = document.getElementById('userVerifyConfirmBtn')
    let userVerifyMailBtn = document.getElementById('userVerifyMailBtn')
    let userVerifyCancelBtn = document.getElementById('userVerifyCancelBtn')

    function resetVerifyModal(){
        turnDisabled(userVerifyConfirmBtn)
        userVerifyInput.value = ''
        userVerifyModal.style['display'] = 'none'
    }

    if(userVerifyOpenBtn !== null){
        userVerifyOpenBtn.addEventListener('click',()=>{
            userVerifyModal.style['display'] = 'inline-grid'
            resetPwModal()
        })
    }

    if(userVerifyInput !== null){
        userVerifyInput.addEventListener('keydown',(e)=>{
            if(e.key == 'Enter'){
                userVerifyConfirmBtn.click()
            }
        })
    }

    if(userVerifyConfirmBtn !== null){
        userVerifyConfirmBtn.addEventListener('click',()=>{
            userVerifyConfirmBtn.innerHTML = '<span class="spiner">🌀</span>'
            let userEmail = document.getElementById('userEmail').innerText.split('(')[0]
            let userVerify = userVerifyInput.value
            console.log(userEmail)
            console.log(userVerify)
            fetch("/getVerify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    userEmail: userEmail,
                    userVerify: userVerify
                }),
                })
                .then((response) => response.json())
                .then((result) => {
                    if(result == 0){
                        alert('메일 인증에 성공하였습니다.')
                        resetVerifyModal()
                    }else if(result == 1){
                        userVerifyInput.value = ''
                        turnDisabled(userVerifyConfirmBtn)
                        alert('발급된 코드가 없습니다. 메일 재발송 부탁드립니다.')
                    }else if(result == 2){
                        userVerifyInput.value = ''
                        alert('코드가 일치하지 않습니다. 대소문자를 구분하니 주의 부탁드립니다.')
                    }else if(result == 3){
                        userVerifyInput.value = ''
                        turnDisabled(userVerifyConfirmBtn)
                        alert('시간이 만료되었습니다. 메일 재발송 부탁드립니다.')
                    }else if(result == 99){
                        userVerifyInput.value = ''
                        turnDisabled(userVerifyConfirmBtn)
                        alert('알 수 없는 사유로 실패하였습니다.')
                    }
                });
        })
    }

    if(userVerifyMailBtn !== null){
        userVerifyMailBtn.addEventListener('click',()=>{
            userVerifyMailBtn.innerHTML = '<span class="spiner">🌀</span>'
            let userEmail = document.getElementById('userEmail').innerText.split('(')[0]
            fetch("/sendMail", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    joinEmail: userEmail
                }),
            })
            .then((response) => response.json())
            .then((result) => {
                if(result == 4){
                    turnActive(userVerifyConfirmBtn)
                    userVerifyInput.focus()
                    userVerifyMailBtn.innerHTML = '메일발송'
                    alert('메일이 발송되었습니다. 인증코드는 10분이 지나면 사용이 불가능합니다.')
                }else{
                    userVerifyMailBtn.innerHTML = '메일발송'
                    alert('메일 발송에 실패하였습니다.')
                }
            });
        })
    }

    if(userVerifyCancelBtn !== null){
        userVerifyCancelBtn.addEventListener('click',()=>{
            resetVerifyModal()
        })
    }
}

if(document.getElementById('changePwOpenBtn') !== null){
    userModalInit()
}