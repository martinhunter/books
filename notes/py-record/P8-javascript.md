事件： onclick, onmouseover

解决兼容性问题：document.getElementById('div1')而不直接使用div1

设置变量： var oVarname = document.getElementById('div1')

onmouseover="document.getElementById('div1').display='none';"

<script>
  function func_name(){
  document.getElementById('div1').display='none';
  }
</script>
onmouseover="func_name()"

#### 操作属性
传入的参数name和value都是值，name不能直接传入style.name，需要加[]。
所有以.property调用的属性都可用['property']代替
function setStyle(name, value){
  var oDiv=document.getElementById('div1');
  oDiv.style.name=value; /\*此处的name是style的属性而非传入的变量name\*/
  oDiv.style.['name']=value; /\*此处的name依然是style的属性而非传入的变量name\*/
  oDiv.style.[name]=value; /正确方法：\*变量name可以当作style的属性使用\*/
}
onclick="setStyle('width', '400px')"
  
#### 提取行间事件：
oBtn.clock=func_name;
oBtn.clock=function(){
}

window.onload=function(){}  页面加载完成后运行
aDiv=document.getElementByTagName('div') 获得一个数组
aDiv[0].style.background='red' 选取数组中的1个元素
aDiv[i].index=i 设置元素的序列
 
this: 当前发生事件的元素
aBtn[i].onclick=function(){
  for(var i=0;i<aBtn.length;i++){
  aBtn[i].className='';
  }
  this.className='active';
};

aBtn[i].innerHTML='<h2>'+(this.index+1)+'月活动</h2><p>'+cont[this.index]+'</p>';

***

***

### 数据类型
interger(i)
function(fn)
object(o)
array(a)
regexp(re)
variant(v)

数字类型转换：往右直到非数字。parseInt(var_name),parseFloat()
判断是否为数字： isNaN()

#### 函数传参
arguments等同于python中的args，是一个数组。
arguments.length

取非行间样式（不能用来设置）
* obj.currentStyle[attr]  // 仅适用IE
* getComputedStyle(obj, false)[attr]  // false处可以是任意值。

#### 数组的使用
定义： var arr=[12, 8, 5, 9];
属性： arr.length=0; 可以清空数组

arr.push(element); 从尾部添加
arr.unshift(element); 从头部添加
arr.pop(element); 从尾部删除
arr.shift(element); 从头部删除
arr.splice(起始位置, 要删除的元素数量,'要添加的元素1' ,'要添加的元素2','要添加的元素3');
arr.sort(function(n1, n2){return n1-n2;}); 返回值负数则前后不交换，否则交换来达到排序的目的
arr.concat(arr2); 连接2个数组
arr.join(分隔符);  元素组成字符串

### 变量类型
number、string‘boolean、undefined、object、array、function

类型抓换 parseInt(var)

字符串兼容性问题：
str[0]改为str.charAt(0)

***

## DOM(document)
标签=元素=节点

选取子节点-> children
选取父节点-> parentNode
获得由position属性的父节点对象（默认为body）：offsetParent

选取首尾节点：firstElementChild,lastElementChild
选取相邻节点：nextElementSibling，previousElementSibling


```html
<script>
    var oUl=document.getElementById('uul');
    oUl.childNodes[i].nodeType;  //childNodes有兼容性问题
    oUl.children[i].nodeType;  //只取元素节点，无兼容性问题
    oUl.children[i].style.width='200px';
    //nodeType==3 -> 文本节点
    //nodeType==1 -> 元素节点
    
    if(oUl.firstElementChild){
        oUl.firstElementChild.style.width='200px'  //用于chrome，IE9
    }
    else{
        oUl.firstChild.style.width='200px'  //用于IE7
    }
    
    //获取子节点中所有符合类名的元素
    function gbClass(oParent, sClass){
        var aResult=[];
        var aEle=oParent.getElementByTagName('*');  // *获得所有
        for(var i=0;i<aEla.length; i++){
            if(aEle[i].className==sClass){
                aResult.push(aEle[i]);
            }
        }
        return aResult;
    }
    
    var aClassNeeded=gbClass(oUl, 'oneClass');
</script>
<body>
    asbda  ->文本节点
    <div></div>  -> 元素节点
</body>
```

操纵元素属性3种方式：
* oDiv.style.display="block"
* oDiv.style["display"]="block"
* oDiv.setAttribute("display","block")

获取：getAttribute("display")
移除：removeAttribute("display")

### 插入元素（改变了innerHTML）
父级创建子节点： document.createElement('li');
父级插入子节点（到最后，会先把元素从原有父节点删除，然后插入新父节点，也可以是原有父节点）： oLis.appendChild(oLis); 
父级插入子节点（再制定位置前）： oUl.insertBefore(新节点,在谁之前); 
父级删除子节点： oUl.removeChild(子节点);  

```html
<script>
    var oUl=document.getElementById('uul');
    
    var oLis=document.createElement('li');
    oLis.innerHTML=oTextarea.value;  // 为新元素添加值。
    oLis.appendChild(oLis);  //创建元素并插入到需要的位置，但与innerHTML不同，不改变原有的其他元素。
    oUl.insertBefore(oLis,aLi[0]);  //在oUl中插入oLias，位于aLi[0]之前
    
</script>
<body>
    maincont
</body>
```

### 文档碎片：提高dom操作性能
> 创建完新元素插入文档碎片，最后再插入页面（避免多次页面重新渲染）

类似1个array,先将要增加的元素加入到oFrag中，然后传递给父级元素

```html
<script>
window.onload=function(){
    var oFrag=document.createDocumentFragment();
    for（var i=0;i<10000; i++){
        pass
        oFrag.appendChild(newelement);
    }
    oUl.appendChild(oFrag);
};
    
</script>
<body>
    <ul id="ull">
    </ul> 
</body>
```

var stri=document.getElementByTag('liId').[1];
str.toLowerCase();
str.search('匹配字符');  //返回匹配到的字符起始位置，是正数，没找到返回-1
str.split('分隔符');  //可以是空格，返回array

排序：
aLi是元素集合，并不完全是array,无法直接使用sort。

```html
array[i]=aLi[i];  // array=[aLi[0],aLi[1],aLi[2]...]
array.sort(function (li1,li2){
    var n1=parseInt(li1.innerHTML);
    var n2=parseInt(li2.innerHTML);
    return n1-n2;
});
// 此时array中的成员已重新排列。例如array=[aLi[2],aLi[1],aLi[4]...]
oUL1.appendChild(array[i]); 

```

### 表单

```html
<form action="http://www.baodu.com/">
    usname:<input type="text" name="user" /><br>
    
    <input type="submit" />
    <input type="reset" />
</form>
```
表单事件 onsubmit, onreset

表单内容验证
* 组织用户输入非法字符 -> 阻止事件
* 输入时、失去焦点时验证 -> onkeyup、onblur
* 提交时检查 -> onsubmit
* 后台数据检查 


## js运动
setInterval：多次点击时，可以开启多个定时器，导致setInterval中的函数被执行多次
先执行一次cleatInterval（yourtimer）确保只有1个定时器。

缓冲运动：speed=（目标值-当前值）/缩放系数 -> 注意：
speed=speed>0?Math.ceil(speed):Math.floor(speed);
为避免speed在-1~1之间时停止运动，需要向上取整和向下取整数。
Math.abs() 获取绝对值。，。/mn
bvasdfghjkltyuiopSD  

#### 页面滚动
offsetWidth: 返回数值，width+padding+border
clientHeight：页面可视区域高度

```html
window.onscroll=function (){
    var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;  //写2种以兼容不同浏览器。
};
```

# JavaScript 运行机制详解：Event Loop（指主线程从"任务(事件）队列"中循环不断地读取事件）
[来源](http://ju.outofmemory.cn/entry/95512)
异步执行的运行机制如下:(只要主线程空了，就会去读取"任务队列")
1. 所有同步任务都在主线程上执行，形成一个执行栈（execution context stack）。
2. 主线程之外，还存在一个"任务队列"（task queue）(event queue)。只要异步任务有了运行结果，就在"任务队列"之中放置一个事件。("任务队列"除了IO设备的事件以外，还包括一些用户产生的事件（比如鼠标点击、页面滚动等等),只要指定过回调函数，这些事件发生时就会进入"任务队列")。
3. 一旦"执行栈"中的所有同步任务执行完毕，系统就会读取"任务队列"，看看里面有哪些事件。哪些对应的异步任务，于是结束等待状态，进入执行栈，开始执行。
4. 主线程不断重复上面的第三步。

> "回调函数"（callback）:就是那些会被主线程挂起来的代码。异步任务必须指定回调函数，当主线程开始执行异步任务，就是执行对应的回调函数。

### 运行过程
1. for循环置入栈，并被执行，i=0，执行alert(100)，alert出栈
2. lis[0].onclick置入栈，不执行，出栈，置入webapi监听
(若为setInterval(func,1000)则会置入webapi，并生成计时器，在1后自动置入task queue）
3. 执行i++，i=1，执行alert(101)，alert出栈
4. lis[1].onclick置入栈，不执行，出栈，置入webapi监听
5. 执行i++，i=2，执行alert(102)，alert出栈
6. lis[2].onclick置入栈，不执行，出栈，置入webapi监听
7. 循环4次，执行完所有同步任务，此时i=3
8. 若没有点击事件，无事发生。若lis[2]被点击，lis[2].onclick被置入task queue中，lis[1]被点击，
lis[1].onclick被置入task queue中，且排在lis[2]之后。
9. event loop检测到task queue不为空，将lis[2].onclick入栈，执行tupian.src=arr[i]，此时i=3,执行完成后出栈
10. event loop检测到task queue不为空，将lis[1].onclick入栈，执行完成后出栈.
11. event loop检测到task queue为空，等待新任务。


```javascript
for （var i=0；i<arr.length; i++){
    alert(i+100)；
    lis[i].onclick=function(){
        tupian.src=arr[i]
    }
}
//解决方法1，对每个i作为属性存储。
for（var i=0；i<arr.length; i++){
    lis[i].index=i;
    lis[i].onclick=function(){
        tupian.src=arr[this.index];
    }
}
//解决方法2，给事件套自调用函数（闭包函数）
for（var i=0；i<arr.length; i++){
    (function (i){
        lis[i].onclick=function(){
            tupian.src=arr[i];
        }
    })(i)
}
//or
for（var i=0；i<arr.length; i++){
    lis[i].onclick=(function(i){
        return function(){
            tupian.src=arr[i];
        }
    })(i)
}
```

### js事件
事件冒泡，例如元素有onclick函数被触发，onclick事件会传递给父级触发父级的onclick函数，再传递给更上一级，直到触发document的onclick函数。

```html
oBtn.onclick=function(ev){
    var oEvent=ev||event;
    //做一些事情
    oEvent.cancelBubble=true;  //取消冒泡，不触发上层的onclick
}

//获取鼠标位置
function getPos(ev){
    var oEvent=ev||event;
    var scrollTop=document.documentElement.scrollTop||document.body.scrollTop
    var scrollLeft=document.documentElement.scrollLeft||document.body.scrollLeft
    return {x:oEvent.clientX+scrollLeft,y:oEvent.clientY+scrollTop}
}

//获取键盘事件
var document.onkeydown=function(ev){
    var oEvent=ev||event;
    oEvent.keyCode==37
````

##### 默认行为
document.oncontextmenu=function(ev){var oEvent=ev||event;
return false}取消显示鼠标右键内容
oTextarea.onkeydown=function(){return false}文本框现无法输入

```html
oDiv.onmouseup=function (){
    oDiv.onmousemove=null;
    oDiv.onmouseup=null;
}
```

### 面向对象（this）
#### 阶段1
创建空白对象
创建构造函数（构造对象的函数）

```html
function CreateObject(param){
    var obj=new Object();
    obj.name='bl';
    obj.q=param;
    obj.firstFunction=function(){alert(this.name);};
    return obj;
}
var objInstance1=CreateObject('param1');
```
#### 进阶
原型prototype添加方法
构造函数添加属性

```html
function CreateObject(param){
    //创建新对象是系统自动调用var this=new Object();
    
    this.name='bl';
    this.q=param;
    //此时系统自动调用return this;
}
//实例共用prototype方法
CreateObject.prototype.fnClick=function(){
    this.aDiv[oBtn.index].style.display='block';
}
CreateObject.prototype.firstFunction=function(){
    var _this=this;
    //内部有其他调用时需要选择正确的this。
    this.aBtn[i].onclick=function(){
        _this.fnClick();
    }
    alert(this.name);
};
var objInstance1=new CreateObject('param1');
```
#### 使用json创建单个对象

```html
var json={
    name:'name1',
    func1:function(){};
}
json.name;
json.func1();

```
#### 继承

```html
function A(par1,par2){
    this.pro1=par1;
    this.pro2=par2
    }
A.prototype.show=function(){};

function B(od1,od2){
    //使用call,this(即B)代替了A对象，并传入其他参数。实现继承
    A.call(this，od1，od2);
}

//将A原型的所有方法传递给B继承
for (var i in A.prototype){
    B.prototype[i]=A.prototype[i]
}
```