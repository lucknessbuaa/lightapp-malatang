jQuery.fx.interval = 50;
$(function(){
	var time = 400;
	$(".order").each(function(index){
		if (index <= 4) {
			time += 100*index;
		} else if (time <= 2000) {
			time += 100;
		}
		$(this).addClass('viewed').animate({left: 0},time);
	});
});