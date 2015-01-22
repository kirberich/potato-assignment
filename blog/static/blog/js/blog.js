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
            type: 'POST',
            data: $('#search-form').serializeArray(),
            dataType: 'json',
            success: function(response) {
                if(response.success){
                    $("#content-wrapper").hide();
                    $("#search-wrapper").html("<div class='container'><div class='row'><div class='col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1'></div></div></div>");
                    $("#search-wrapper .row > div").append("<div class='clearfix'><a href='#' id='close-search' class='btn btn-default pull-right'>" +
                                                           "<span class='glyphicon glyphicon-remove'>Chiudi risultati</span></a>" +
                                                           "<span>" + response.posts.length + " results matched your query</span></div>");
                    for(var i in response.posts)
                    {
                        var post = response.posts[i];
                        tags = "";
                        if(post.tags.length){
                            tags += "<span>Categorized as: </span>";
                        }
                        for(var j in post.tags){
                            var tag = post.tags[j];
                            tags += "<span class='tag label label-primary'><a href='" + tag.url + "'>#" + tag.title + "</a></span>";
                        }
                        comments = "";
                        if(post.comments_count > 0){
                            comments = "<span>Received <span class='badge'>" + post.comments_count + "</span> comments</span>";
                        }
                        var result = "<div class='post-preview'>" +
                                        "<a href='" + post.url + "'><h2 class='post-title'>" + post.title + "</h2></a>" +
                                        "<h3 class='post-subtitle'>" + post.subtitle + "</h3>" +
                                        "<p class='post-meta'>Posted on " + post.created + comments + tags + "</p>" +
                                        "</div>"
                        $("#search-wrapper .row > div").append($(result));
                    }
                }
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
