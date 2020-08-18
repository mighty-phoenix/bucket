$(document).ready(function(){
    if($('.Movie').length===0) {
        $( ".movie-title" ).after( "<div class='small-title'>NOTHING TO DISPLAY!</div>" );
    } else {
        setTimeout(function(){$('.Movie').first().addClass("active")},0);
    }
    if($('.Book').length===0) {
        $( ".book-title" ).after( "<div class='small-title'>NOTHING TO DISPLAY!</div>" );
    } else {
        setTimeout(function(){$('.Book').first().addClass("active")},0);
    }
    if($('.TV').length===0) {
        $( ".tv-title" ).after( "<div class='small-title'>NOTHING TO DISPLAY!</div>" );
    } else {
        setTimeout(function(){$('.TV').first().addClass("active")},0);
    }
})

$('.carousel').carousel({
    interval: 3000
})

$('.carousel .carousel-item').each(function() {
    var minPerSlide = 4;
    var next = $(this).next();
    if (!next.length) {
        next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));

    for (var i = 0; i < minPerSlide; i++) {
        next = next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }

        next.children(':first-child').clone().appendTo($(this));
    }
});
