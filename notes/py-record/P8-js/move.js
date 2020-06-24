function getByClass(oParent, sClass){
	var aEle=oParent.getElementsByTagName('*');
	var aResult=[];
	
	for(var i=0;i<aEle.length;i++)
	{
		if(aEle[i].className==sClass)
		{
			aResult.push(aEle[i]);
		}
	}
	
	return aResult;
}

function getStyle(obj, attribute){
				if(obj.currentStyle){
					return obj.currentStyle[attribute];
				}
				else{
					return getComputedStyle(obj,null)[attribute];
				}
			}

function startMove(obj,json,func){
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
			var speed=(json[attribute]-attri_value)/5;
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
			if(func){func();}
		}
	},30);
}

function getPos(ev){
	var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
	var scrollLeft=document.documentElement.scrollLeft||document.body.scrollLeft;
	return {x:ev.clientX+scrollLeft, y:ev.clientY+scrollTop}
}