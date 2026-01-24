let likeMarkSpan = document.getElementById('likeMarkSpan')
let likeCountSpan = document.getElementById('likeCountSpan')
let boardNoDiv = document.getElementById('boardNoDiv').innerHTML

function setLike(){
    fetch("/setLike", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            bno: boardNoDiv
        }),
        })
        .then((response) => response.json())
        .then((result) => {
            likeCountSpan.innerHTML = result[2]
            if(result[0]){
                likeMarkSpan.innerHTML = '❤️'
                boardNoDiv.outerHTML = ''
            }else{
                alert(result[1])
            }
        });
}
