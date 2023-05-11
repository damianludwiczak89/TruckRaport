document.addEventListener('DOMContentLoaded', function() {

    // Show button to confirm delete spedition
    document.querySelectorAll('#delete').forEach(function(button) {
        button.onclick = function () {
            let buttons = document.querySelectorAll(`[data-id=${CSS.escape(button.dataset.id)}]`)
        if (buttons[1].style.display == "none") {
            buttons[1].style.display = "block";
        }
        else {
           buttons[1].style.display = "none"
        }};
    });



});