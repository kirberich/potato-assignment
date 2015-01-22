$(function() {
    $("#id_tags").select2({
        tags: true
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

    function doneTyping () {
        //do something
        $.ajax({
            url: $('#search-form').attr("action"),
            type: 'GET',
            data: $('#search-form').serializeArray(),
            success: function(response) {
                $("#content-wrapper").html($(response).find("#content-wrapper").html());
            }
        });
    }

    $("body").on("click", "#close-search", function(){
        $("#search-wrapper").empty();
        $("#content-wrapper").show();
    });

    var typingTimer;
    var doneTypingInterval = 500;

    //on keyup, start the countdown
    $("#search-input").keyup(function(){
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    //on keydown, clear the countdown
    $("#search-input").keydown(function(){
        clearTimeout(typingTimer);
    });

    $('#search-form').on("submit", function(evt){
        evt.preventDefault();
        doneTyping();
    });
});
