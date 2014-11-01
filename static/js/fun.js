

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