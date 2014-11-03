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

// HANDLES THE DASHBOARD MENU ON MOBILE
$('.dashactivate').click(function(){
	var self = $(this);

	if (self.hasClass('active')) {
		self.removeClass('active');
		$("#longmenu").removeClass('active');
		$('.dash').removeClass('active');
	} else {
		self.addClass('active');
		$("#longmenu").addClass('active');
		$('.dash').addClass('active');
	}
})

$('.preorder').click(function(event) {
   $('#preorder_modal').modal('show')
});
 
// get current page
var pathArray = window.location.pathname.split( '/' );
// assign loadmore button type
$('.loadmore').attr( "data-type", pathArray[2]);
if (pathArray[1] == "dashboard") {
    $('#longmenu').find("."+pathArray[2]).addClass('active');
}



// FOLLOW funtion
$('.follow').click(function(){
      var self = $(this),
      	 count = parseInt($(".followcount").text());

        $.ajax({
            type: "POST",
            url: "/feed/follow/",
            dataType: "json",
            data: { 
            	"designer": self.data('designer'),
            	"follower": self.data('user')

            },
            success: function(data) {
            	if (data["message"] == "followed") {
            		var glyph = $(".avatar .glyphicon-thumbs-up");
                	glyph.fadeIn('fast');
                	glyph.fadeOut('slow');
                	self.text('unfollow');
                    self.addClass('active');
                	$(".followcount").text(data["followcount"]);
                } else if (data["message"] == "unfollowed") {
                	var glyph = $(".avatar .glyphicon-thumbs-down");
                	glyph.fadeIn('fast').delay(700).fadeOut('slow');
                	self.text('follow');
                    self.removeClass('active');
                	$(".followcount").text(data["followcount"]);
                }
            }
        });
});

// cut/sow funtion

$(document).on('click', ".dope", function () {
      var self = $(this),
      	  ratingcount = self.closest('.product-wrapper').find(".ratingcount");

            $.ajax({
                type: "POST",
                url: "/feed/dope/",
                dataType: "json",
                data: { 
                    "product": self.data('product'),
                },
                success: function(data) {
                    console.log(data["message"]);
                    if (data["message"] == "dope") {
                        self.html('unDope!<span class="plus-one"> -1</span>');
                        var glyph = self.closest('.product-wrapper').find(".glyphicon-thumbs-up");
                        glyph.fadeIn('fast').delay(700).fadeOut('slow');
                        ratingcount.text(data["rating"]);
                    } else if (data["message"] == "undope") {
                        var glyph = self.closest('.product-wrapper').find(".glyphicon-thumbs-down");
                        glyph.fadeIn('fast').delay(700).fadeOut('slow');
                        self.text('Dope!');
                        ratingcount.text(data["rating"]);
                    }
                }
            });
});

$('.loadmore-notes').click(function(){
      var self = $(this),
          offset = $('tr').length;
          console.log(offset);
            $.ajax({
                type: "POST",
                url: "/dashboard/morenotif",
                dataType: "html",
                data: { 
                    "offset": offset,
                },
                success: function(data) {
                    if (data) {
                        $('table').append(data);
                    } else {
                        self.addClass('disabled').text('No more Notifications')
                    }
                    
                }
            });
});
$(document).on('click', ".loadmore", function () {
      var self = $(this),
          offset = $('.product').length;
            $.ajax({
                type: "POST",
                url: "/feed/loadmore/",
                dataType: "html",
                data: { 
                    "offset": offset,
                    "type": self.data('type')
                },
                success: function(data) {
                    if (data) {
                        $('.productgroup').append(data);
                    } else {
                        self.addClass('disabled').text('No more products')
                    }
                    
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