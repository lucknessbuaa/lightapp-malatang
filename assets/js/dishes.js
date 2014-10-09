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

	var update = function(){
		if ($(window).height() >= $(document).height() && $('.more').length) {
			var more = $('.more');
			$.get(more.attr('href'), function(data){
				more.remove();
				$('.main').append($(data).find('.dish')).append($(data).find('.more'));
				$(".dish:not(.viewed)").each(function(index){
					if (index <= 4) {
						time += 50*index;
					} else {
						time += 50;
					}
					$(this).addClass('viewed').animate({left: 0},time);
				});
				update();
			});
		}
	};
	update();

	$(window).scroll(function(){
		if (!$('.more').length) {
			$(window).unbind('scroll');
		}
		if ($(window).scrollTop() + $(window).height() == $(document).height()) {
			var more = $('.more');
			$.get(more.attr('href'), function(data){
				more.remove();
				$('.main').append($(data).find('.dish')).append($(data).find('.more'));
				var time = 400;
				$(".dish:not(.viewed)").each(function(index){
					if (index <= 4) {
						time += 50*index;
					} else {
						time += 50;
					}
					$(this).addClass('viewed').animate({left: 0},time);
				});
			});
		}
	});
});