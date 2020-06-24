window.onload=function(){
				// alert(12321);
				oDiv=document.getElementById('anib');
				// oDiv.timer1=null;
				oDiv2=document.getElementById('an2');
				// oDiv2.timer1=null;

				oDiv2.onclick=oDiv.onclick=function (){
					pAnima(this,{'width':500,'height':210});
				}
				
			}
			function getStyle(obj, attribute){
				if(obj.currentStyle){
					return obj.currentStyle[attribute];
				}
				else{
					return getComputedStyle(obj,null)[attribute];
				}
			}
			function pAnima(obj,json,func){
				clearInterval(obj.timer1);
				obj.timer1=setInterval(function(){
					var bStop=true;
					for (var attribute in json){
						if(attribute=='opacity'){
							var attri_value=Math.round(parseFloat(getStyle(obj,attribute))*100);
						}
						else{
							var attri_value=parseInt(getStyle(obj,attribute));
						}
						var speed=(json[attribute]-attri_value)/10;
						speed=speed>0?Math.ceil(speed):Math.floor(speed);
						if(attri_value!=json[attribute]){
							bStop=false;
						}
						if(attribute=='opacity'){
							obj.style.filter='alpha(opacity:'+(attri_value+speed)+')';
							obj.style.opacity=(attri_value+speed)/100;
						}
						else{
							obj.style[attribute]=attri_value+speed+'px';
						}
					}
					if(bStop){
						clearInterval(obj.timer1);
						if(func){func()}
					}
				},500);
			}

