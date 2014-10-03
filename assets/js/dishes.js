$(function(){
	var time = 400;
	$(".dish").each(function(index){
		if (index <= 4) {
			time += 50*index;
		} else {
			time += 50;
		}
		$(this).addClass('viewed').animate({left: 0},time);
	});
	$(window).scroll(function(){
		if (!$('.more').length) {
			$(window).unbind('scroll');
		}
		if ($(window).scrollTop() + $(window).height() == $(document).height()) {
			var more = $('.more');
			$.get(more.attr('href'), function(data){
				more.remove();
				$('.main').append($(data).find('.dish'));
				var time = 400;
				$(".dish:not(.viewed)").each(function(index){
					if (index <= 4) {
						time += 50*index;
					} else {
						time += 50;
					}
					$(this).animate({left: 0},time);
				});
			});
		}
	});
});