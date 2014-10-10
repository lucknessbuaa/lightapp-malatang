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
	$(".baiduAuth").click(function(){
		var client_id = $(this).data('id');
		var redirect_uri = window.location.origin+'/app/auth/baidu';
		window.location.href = 'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id='+client_id+'&redirect_uri='+encodeURIComponent(redirect_uri);
	});
	$(".weiboAuth").click(function(){
		var client_id = $(this).data('id');
		var redirect_uri = window.location.origin+'/app/auth/weibo';
		window.location.href = 'https://api.weibo.com/oauth2/authorize?response_type=code&client_id='+client_id+'&redirect_uri='+encodeURIComponent(redirect_uri);
	});
	$(".QQAuth").click(function(){
		var client_id = $(this).data('id');
		var redirect_uri = window.location.origin+'/app/auth/qq';
		window.location.href = 'https://graph.qq.com/oauth2.0/authorize?state=dying&response_type=code&client_id='+client_id+'&redirect_uri='+encodeURIComponent(redirect_uri);
	});

});