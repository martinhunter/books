var cont=[
	'1yue1hao',
	'2月内容',
	'3月来了',
	'4月的我',
	'五谷饭呢等',
	'六味地黄丸',
	'七星连珠',
	'八星报喜',
	'九曲十八弯',
	'十分完美',
	'十一月',
	'十二'
]
window.onload=function(){
	var oDiv=document.getElementById('tabl');
	var aLi=oDiv.getElementsByTagName('li');
	var oTxt=oDiv.getElementsByTagName('div')[0];
	
	for(var i=0; i<aLi.length; i++){
		aLi[i].index=i;
		aLi[i].onmouseover=function(){
			for(var i=0; i<aLi.length; i++){
				aLi[i].className=''
			}
			this.className='active';
			oTxt.style.display='block';
			oTxt.innerHTML='<h2>'+(this.index+1)+'月活动</h2><p>'+cont[this.index]+'</p>';
		}
		aLi[i].onmouseout=function(){
			this.className='';
			oTxt.style.display='none';
			
		}
	}
}