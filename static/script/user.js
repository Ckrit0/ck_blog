
/**
 * 유저 모달 초기화
 */
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
    
    /**
     * changePwModal 초기화
     */
    function resetPwModal(){
        userNowPwInput.value = ''
        userNewPwInput.value = ''
        userNewConfirmInput.value = ''
        userChangePwInfo.value = '영어,숫자,특수문자 포함된 8~16자리로 설정'
        changePwModal.style['display'] = 'none'
    }

    /**
     * changePwModal 열기
     */
    changePwOpenBtn.addEventListener('click',()=>{
        changePwModal.style['display'] = 'inline-grid'
        resetVerifyModal()
        resetLeaveModal()
    })

    /**
     * 엔터키로 다음 input으로 이동
     */
    userNowPwInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            userNewPwInput.focus()
        }
    })

    /**
     * 엔터키로 다음 input으로 이동
     */
    userNewPwInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            userNewConfirmInput.focus()
        }
    })

    /**
     * 엔터키로 변경하기 버튼 클릭
     */
    userNewConfirmInput.addEventListener('keydown',(e)=>{
        if(e.key=="Enter"){
            changePwSubmitBtn.click()
        }
    })

    /**
     * 비밀번호 변경 요청
     */
    changePwSubmitBtn.addEventListener('click',()=>{
        changePwSubmitBtn.innerHTML = '<span class="spiner">🌀</span>'
        let userNowPw = userNowPwInput.value
        let userNewPw = userNewPwInput.value
        let userNewConfirm = userNewConfirmInput.value

        if(userNowPw == '' || userNewPw == '' || userNewConfirm == ''){
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

        fetch("/changePwByNowPw", {
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
            alert(result[1])
            if(result[0] == 8){
                resetPwModal()
            }
            changePwSubmitBtn.innerHTML = '변경하기'
            return
        });
    })

    /**
     * 비밀번호 변경 모달 닫기
     */
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

    /**
     * userVerifyModal 초기화
     */
    function resetVerifyModal(){
        if(userVerifyConfirmBtn !== null){
            turnDisabled(userVerifyConfirmBtn)
            userVerifyInput.value = ''
            userVerifyModal.style['display'] = 'none'
        }
    }

    /**
     * userVerifyModal 열기
     */
    if(userVerifyOpenBtn !== null){
        userVerifyOpenBtn.addEventListener('click',()=>{
            userVerifyModal.style['display'] = 'inline-grid'
            resetPwModal()
            resetLeaveModal()
        })
    }

    /**
     * 엔터키로 인증코드 확인
     */
    if(userVerifyInput !== null){
        userVerifyInput.addEventListener('keydown',(e)=>{
            if(e.key == 'Enter'){
                userVerifyConfirmBtn.click()
            }
        })
    }

    /**
     * 인증코드 확인 요청
     */
    if(userVerifyConfirmBtn !== null){
        userVerifyConfirmBtn.addEventListener('click',()=>{
            userVerifyConfirmBtn.innerHTML = '<span class="spiner">🌀</span>'
            let userEmail = document.getElementById('userEmail').innerText
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
                    alert(result[1])
                    if(result[0] == 11){
                        resetVerifyModal()
                    }else if(result[0] == 13){
                        userVerifyInput.value = ''
                    }else{
                        userVerifyInput.value = ''
                        turnDisabled(userVerifyConfirmBtn)
                    }
                });
        })
    }

    /**
     * 인증 메일 발송 요청
     */
    if(userVerifyMailBtn !== null){
        userVerifyMailBtn.addEventListener('click',()=>{
            userVerifyMailBtn.innerHTML = '<span class="spiner">🌀</span>'
            let userEmail = document.getElementById('userEmail').innerText
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
                alert(result[1])
                if(result[0] == 15){
                    turnActive(userVerifyConfirmBtn)
                    userVerifyInput.focus()
                }
                userVerifyMailBtn.innerHTML = '메일발송'
            });
        })
    }

    /**
     * userVerifyModal 닫기
     */
    if(userVerifyCancelBtn !== null){
        userVerifyCancelBtn.addEventListener('click',()=>{
            resetVerifyModal()
        })
    }

    /* userLeaveModal */
    let userLeaveOpenBtn = document.getElementById('userLeaveOpenBtn')
    let userLeaveModal = document.getElementById('userLeaveModal')
    let userLeavePw = document.getElementById('userLeavePw')
    let userLeaveSubmitBtn = document.getElementById('userLeaveSubmitBtn')
    let userLeaveCancelBtn = document.getElementById('userLeaveCancelBtn')

    /**
     * userLeaveModal 초기화
     */
    function resetLeaveModal(){
        userLeavePw.value = ''
        userLeaveModal.style['display'] = 'none'
    }

    /**
     * userLeaveModal 열기
     */
    userLeaveOpenBtn.addEventListener('click',()=>{
        userLeaveModal.style['display'] = 'inline-block'
        resetPwModal()
        resetVerifyModal()
    })
    
    /**
     * 회원탈퇴 요청
     */
    userLeaveSubmitBtn.addEventListener('click',()=>{
        let userEmail = document.getElementById('userEmail').innerText
        fetch("/leave", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                userEmail : userEmail,
                userPw : userLeavePw.value
            }),
            })
            .then((response) => response.json())
            .then((result) => {
                alert(result[1])
                if(result[0] == 10){
                    window.location.href='/'
                }
                return
            });
    })

    /**
     * userLeaveModal 닫기
     */
    userLeaveCancelBtn.addEventListener('click',()=>{
        resetLeaveModal()
    })
}

/**
 * 본인 화면이면 유저 모달 초기화
 */
if(document.getElementById('changePwOpenBtn') !== null){
    userModalInit()
}