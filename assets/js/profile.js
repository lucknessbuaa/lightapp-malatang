$(function() {
    $('#preorder').click(function(){
        location.href = 'preorder';
    });

    $('#orderlist').click(function(){
        location.href = 'myOrder';
    });

    $('#exit').click(function() {
        location.href = 'exit';
    });

    $('.head img').click(function(){
        location.href = '/app';
    });
});