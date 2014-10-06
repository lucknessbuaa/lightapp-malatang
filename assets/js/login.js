$(function(){
	var time = 400;
	$(".type").each(function(index){
		if (index <= 4) {
			time += 50*index;
		} else {
			time += 50;
		}
		$(this).addClass('viewed').animate({left: 0},time);
	});
});