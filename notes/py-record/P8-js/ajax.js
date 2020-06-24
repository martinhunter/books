// 使用方式
// ajax('a.txt',function(str){
// 	alert(str);
// },function(failInfo){
// 	alert(failInfo);
// });

function ajax(url,funsuc,funfail){
	// 1.创建ajax对象
	if(window.XDomainRequest){
		var oAjax=new XMLHttpRequest();
	}else{
		var oAjax=new ActiveXObject("Microsoft.XMLHTTP");
	}
	// 2.连接服务器
	oAjax.open('GET',url+'?t='+new Date().getTime(),true);
	// 3.发送请求
	oAjax.send();
	// 4.等待接收
	oAjax.onreadystatechange=function{
		// =4表示完成接收并解析数据
		if(oAjax.readyState==4){
			if(oAjax.status==200){
				funsuc(oAjax.responseText);
			}else{
				if(funfail){
					funfail(oAjax.status);
				}
			}
			
		}
	}
}