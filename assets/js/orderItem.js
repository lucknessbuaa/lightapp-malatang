$(function(){
	$(".plus").click(function(){
		var id = $(this).data('id');
		var counter = $('.number[data-id='+id+']');
		var count = parseInt(counter.text()) || 0;
		if (count >= 0) {
			counter.text(count+1);
		} else {
			counter.text(1);
		}
		$('.minus[data-id='+id+']').removeClass('disabled');

		var numberTotal = $('.numberTotal');
		var priceTotal = $('.priceTotal');
		var number = parseInt(numberTotal.text()) || 0;
		var price = parseFloat(priceTotal.text()) || 0;
		var itemPrice = parseFloat($('.itemPrice[data-id='+id+']').text()) || 0;
		if (number >= 0) {
			numberTotal.text(number+1);
			priceTotal.text((price+itemPrice).toFixed(2));
		} else {
			numberTotal.text(1);
			priceTotal.text(itemPrice.toFixed(2));
		}
		if (!$('.total').is(':visible')) {
			$('.total').show();
		}
	});
	$(".minus").click(function(){
		var id = $(this).data('id');
		var counter = $('.number[data-id='+id+']');
		var count = parseInt(counter.text()) || 0;

		if (!$('.minus[data-id='+id+']').hasClass('disabled')) {
			var numberTotal = $('.numberTotal');
			var priceTotal = $('.priceTotal');
			var number = parseInt(numberTotal.text()) || 0;
			var price = parseFloat(priceTotal.text()) || 0;
			var itemPrice = parseFloat($('.itemPrice[data-id='+id+']').text()) || 0;
			if (number >= 2) {
				numberTotal.text(number-1);
				priceTotal.text((price-itemPrice).toFixed(2));
			} else {
				numberTotal.text(0);
				priceTotal.text('0.00');

				if ($('.total').is(':visible')) {
					$('.total').hide();
				}
			}
		}

		if (count >= 2) {
			counter.text(count-1);
		} else {
			counter.text(0);
			$('.minus[data-id='+id+']').addClass('disabled');
		}
	});
	$('#submit').click(function(){
		// cause it was single thread ~~
		localStorage.setItem("items","");
		var items = {};
		$('.number').each(function(index, value){
			if ($(value).text()!='0') {
				items[$(value).data('id')] = +$(value).text();
			};
		});
		if (!items) {
			toastr.warning('请选择菜品');
			return;
		}
		localStorage.setItem("items",JSON.stringify(items));
		location.pathname = 'app/order';
	});
});