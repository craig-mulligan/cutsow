$('.editProfile').click(function(event) {
    $('input').prop("disabled", false);
});

$('#id_image').change(function(){
    var newsrc = $(this).val();
    console.log(newsrc);
    $(this).next("img").remove();
});

var screenheight = $(window).height();
$("#longmenu").height(screenheight);

$('.follow').click(function(){
      console.log('am i called');

        $.ajax({
            type: "POST",
            url: "/feed/follow/",
            dataType: "json",
            data: { 
            	"designer": $(this).data('designer'),
            	"follower": $(this).data('user')

            },
            success: function(data) {
                alert(data.message);
            }
        });
});

function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 