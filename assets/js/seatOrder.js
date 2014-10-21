$(function(){
	var csrftoken = getCookie('csrftoken');

	$("#dtBox").DateTimePicker({
		'dateTimeFormat':'yyyy-MM-dd HH:mm:ss',
		'titleContentDateTime':'选择日期时间',
		'setButtonContent':'确定',
		'clearButtonContent':'取消'
	});
	$('.plus').click(function(){
		var num = parseInt($("#number").text()) || 0;
		num++;
		if ($('.minus').hasClass('disabled')) {
			$('.minus').removeClass('disabled');
		}
		$("#number").text(num);
	});
	$('.minus').click(function(){
		if ($('.minus').hasClass('disabled')) {
			return;
		}
		var num = parseInt($("#number").text()) || 0;
		num--;
		if (num <= 0) {
			num = 0;
			$('.minus').addClass('disabled');
		}
		$("#number").text(num);
	});
	$("#send").click(function(){
		var _this = this;
		if ($(_this).hasClass('disabled')) {
			return;
		}
		var mobile = $('#mobile').val();
		if (!mobile.match(/^\d{11}$/)) {
			toastr.warning('请正确输入手机号');
			return;
		}
		
		$.ajax({
			url: 'seatOrder',
			type: 'post',
			data: {'mobile':mobile},
			headers: {'X-CSRFToken': csrftoken},
			success: function(data){
				if (data=='-1') {toastr.error('发送失败');}
			},
			error: function(){
				toastr.error('服务器错误');
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

		var date = $("#time").val();
		var contact = $("#contact").val();
		var mobile = $("#mobile").val();
		var code = $("#code").val();
		var number = parseInt($("#number").text()) || 0;

		if (!date || !contact || !mobile || !code || !number || !mobile.match(/^\d{11}$/)) {
			toastr.warning('请正确填写信息');
			$(_this).removeClass('disabled');
			return;
		}

		$.ajax({
			url: 'seatOrder',
			type: 'post',
			data: {
				'date':date,
				'contact':contact,
				'mobile':mobile,
				'code':code,
				'number':number
			},
			headers: {'X-CSRFToken': csrftoken},
			success: function(data){
				if ('error' in data) {
					toastr.error(data.msg);
					$(_this).removeClass('disabled');
				} else {
					toastr.success('订座成功');
					window.location.pathname='/';
				}
			},
			error: function(){
				toastr.error('服务器错误');
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