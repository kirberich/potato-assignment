function search () {
    //do something
    $.ajax({
        url: $('#search-form').attr("action"),
        type: 'GET',
        data: $('#search-form').serializeArray(),
        success: function(response) {
            $("#results-container").html($(response).find("#results-container").html());
            //window.history.pushState(url, "", url)
        }
    });
}
$(function() {
    $("#id_tags").select2({
        tags: true
    });

    var typingTimer;

    //on keyup, start the countdown
    $("body").on("keyup", "#search-input", function(){
        clearTimeout(typingTimer);
        typingTimer = setTimeout(search, 500);
    });

    //on keydown, clear the countdown
    $("body").on("keydown", "#search-input", function(){
        clearTimeout(typingTimer);
    });

    $('body').on("submit", "#search-form", function(evt){
        evt.preventDefault();
        search();
    });

    $('#add_comment_submit').on("click", function(evt) {
        evt.preventDefault();
        $.ajax({
            url: $('#add_comment_form').attr('action'),
            type: 'POST',
            data: $('#add_comment_form').serializeArray(),
            dataType: 'json',
            success: function(response) {
                if(response.success){
                    $('#add_comment_form')[0].reset();
                    $('.form-error').remove();
                    $('#comments').prepend('<article>' +
                                            '<h3>' + response.title + '</h3>' +
                                            '<div>' + response.text + '</div>' +
                                            '<span class="meta">commented by: ' + response.author + ' on '+ response.created +'</span>' +
                                        '</article>');
                    $("#comments article:first").hide();
                    $('html, body').animate({scrollTop: $("#comments").offset().top - 50}, 500, function(){$("#comments article:first").slideDown();});
                } else {
                    $('.form-error').remove();
                    for(var error in response.errors.fields) { $('#add_comment_form #id_' + error).before(''+
                                                                    '<div class="form-error alert alert-danger" role="alert">' +
                                                                        '<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>' +
                                                                        '<span class="sr-only">Error:</span>' +
                                                                        '<span>' + response.errors.fields[error] + '</span>' +
                                                                    '</div>');
                    }
                }
            }
        });
    });
});
