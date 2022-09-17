console.log("alive");

const UPLOADFORM = document.getElementById('upload-form');
const INPUTIMG  = document.getElementById('id_picture');
console.log(UPLOADFORM);

let progressBar = document.getElementById('progress-box');
let terminate = document.getElementById('cancel-box');

const csrf = document.getElementsByName('csrfmiddlewaretoken');

INPUTIMG.addEventListener('change', function(){
    progressBar.classList.remove('not-visible');
    terminate.classList.remove('not-visible');
})