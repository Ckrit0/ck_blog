



/* changePwModal */
function changePwModalInit(){
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
}

if(document.getElementById('changePwOpenBtn') !== null){
    changePwModalInit()
}