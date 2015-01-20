$(function() {
    $("#id_tags").select2({
        tags: true
    });
    $('#add_comment_submit').on("click", function(evt) {
        evt.preventDefault();
        $.ajax({
            url: $('#add_comment_form').attr('action'),
            type: 'POST',
            data: $('#add_comment_form').serialize(),
            dataType: 'json',
            success: function(response) {
                response = JSON.parse(response);
                if(response.success){
                    $('#add_comment_form')[0].reset();
                    $('.form-error').remove();
                    $('#comments').prepend('<article>' +
                                            '<h3>' + response.title + '</h3>' +
                                            '<p>' + response.text + '</p>' +
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
    $(".delete-link").on("click", function(evt){
        evt.preventDefault();
        var dialog_id = $(this).data("dialog");
        alert(dialog_id);
        $("#" + dialog_id).dialog({
          resizable: false,
          height:140,
          modal: true,
          buttons: {
            "Delete item": function() {
                $.ajax({
                    // TODO!!!!!!!!!!!!!!!!!!
                    url: $(this).attr("href"),
                    type: 'POST',
                    dataType: 'json',
                    context: dialog_id,
                    success: function(response) {
                        $("#" + dialog_id).dialog( "close" );
                    }
                });
             },
            Cancel: function() {
              $( this ).dialog( "close" );
            }
          }
        });
    });
});