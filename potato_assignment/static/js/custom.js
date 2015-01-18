$(document).ready(function () {

window.setTimeout(function() {
    $(".page-alert").fadeTo(100, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 3000);

});