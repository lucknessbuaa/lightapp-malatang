jQuery.fx.interval = 50;
$(function(){
	var time = 400;
	var csrftoken = getCookie('csrftoken');

	$("#dtBox").DateTimePicker({
		'dateTimeFormat':'yyyy-MM-dd HH:mm:ss',
		'titleContentDateTime':'选择日期时间',
		'setButtonContent':'确定',
		'clearButtonContent':'取消'
	});
	$(".info").each(function(index){
		if (index <= 4) {
			time += 50*index;
		} else {
			time += 50;
		}
		$(this).addClass('viewed').animate({left: 0},time);
	});
	$("#send").click(function(){
		var _this = this;
		if ($(_this).hasClass('disabled')) {
			return;
		}
		var mobile = $('#mobile').val();
		if (!mobile.match(/^\d{11}$/)) {
			alert('请正确输入手机号');
			return;
		}
		
		$.ajax({
			url: 'order',
			type: 'post',
			data: {'mobile':mobile},
			headers: {'X-CSRFToken': csrftoken},
			success: function(data){
				if (data=='-1') {alert('发送失败');}
			},
			error: function(){
				alert('服务器错误');
			}
		});

		var DELAY = 30;
		$(_this).text('重新获取('+DELAY+')').addClass('disabled');
		var now = new Date();
		var timer = setInterval(function(){
			time = new Date();
			remain = DELAY - Math.floor((time - now)/1000);
			if (remain > 0) {
				$(_this).text('重新获取('+remain+')');
			} else {
				$(_this).text('重新获取').removeClass('disabled');
				clearInterval(timer);
			}
		},500);
	});
	$("#submit").click(function(){
		var _this = this;
		if ($(_this).hasClass('disabled')) {
			return;
		}
		$(_this).addClass('disabled');

		var deadline = $("#time").val();
		var location = $("#location").val();
		var contact = $("#contact").val();
		var mobile = $("#mobile").val();
		var code = $("#code").val();
		var number = parseInt($("#number").val()) || 0;
		var items = localStorage.getItem("items");

		if (!deadline || !location || !contact || !mobile || !code || !number || !mobile.match(/^\d{11}$/)) {
			alert('请正确填写信息');
			$(_this).removeClass('disabled');
			return;
		}
		if (!items) {
			alert('请选择菜品');
			$(_this).removeClass('disabled');
			return;
		}

		$.ajax({
			url: 'order',
			type: 'post',
			data: {
				'deadline':deadline,
				'location':location,
				'contact':contact,
				'mobile':mobile,
				'code':code,
				'number':number,
				'items':items
			},
			headers: {'X-CSRFToken': csrftoken},
			success: function(data){
				if ('error' in data) {
					alert(data.msg);
					$(_this).removeClass('disabled');
				} else {
					localStorage.setItem("items","");
					window.location.href='order/complete?order='+data.id;
				}
			},
			error: function(){
				alert('服务器错误');
				$(_this).removeClass('disabled');
			}
		});
	});

	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
});