jQuery.fx.interval = 50;
$(function(){
	var time = 400;
	$(".dish").each(function(index){
		if (index <= 4) {
			time += 50*index;
		} else if (time <= 2000) {
			time += 50;
		}
		$(this).addClass('viewed').animate({left: 0},time);
	});
});