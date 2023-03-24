//pop up on hover over elements of class 'bed' that shows id of bed

$(document).ready(function() {
    $('.bed').hover(function() {
        $(this).attr('title', $(this).attr('id'));
    });
}

//display time on click
$(document).ready(function() {
    $('#time').click(function() {
        var now = new Date();
        var time = now.toLocaleTimeString();
        $('#time').html(time);
    });
}   