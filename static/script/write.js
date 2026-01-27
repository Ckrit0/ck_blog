ClassicEditor
    .create(document.querySelector('#editor'), {
        ckfinder: {
            uploadUrl: '/upload'
        }
    })
    .then(editor => {
        document.querySelector('#submit-btn').addEventListener('click', () => {
            document.querySelector('#content').value = editor.getData();
        });
        document.querySelector('#cancel-btn').addEventListener('click', () => {
            window.history.back()
        });
    })
    .catch(error => { console.error(error); });