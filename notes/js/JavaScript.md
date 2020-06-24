## 1.intro

function Lecture(name){this.name = name;}
var lec = new Lecture("js");

1.1 对象:

1. 函数名为一个类对象
2. 函数内为一个构造函数
3. 使用new创建新对象并初始化(调用构造函数)。


1.3 DOM:

作用：快速定位XML层级并操作。


1.4 事件:

作用：处理交互

## 2.面向对象

2.1 *引用*--指向对象实际位置的指针

1. 多变量指向同一对象，对象类型改变，变量随之改变。
2. 引用不指向另一个引用，而是沿着引用链上溯到原来的对象。
3. `var it="str1";var itref=it;var it+="str2";`此时it(即使it是数字也)*指向一个新对象"str1str2"*,itref(引用)依然指向"str1"。

### 2.1.2 判断数据类型(一个对象默认就有constructor属性)

1. typeof obj == "string"; //缺点：不能获得精确的类型；
2. var obj="str1";obj.constructor == String;var obj=new User();obj.constructor == User;//Array,String是构造函数。
*constructor*属性引用原本用来构造该对象的那个函数。

用例：将要被判断的参数的类型构建为一个列表作为参数传入函数。
var lTypes = [String,Number,Array];
`function typedefiner(lTypes,argsToVerify){if()...};`

### 2.1.3 作用域（非全局变量）--由函数(function)划分（不由while，if,for分）

> NOTE:所有属于全局作用域的变量都是window对象的属性。
如果变量没有显式定义(即未加var,有var则window.foo=undefined)，它就是全局定义的。

```javascript
function test(){
    foo = "test";
}
test();
alert(window.foo=="test");
```

### 2.1.4 curry化 == 闭包 == 装饰器 (function(arg){code})();
```
(function(){})()似乎等于new function
```
> NOTE: (function(which){code})(this);如此可等待动态生成的对象，否则闭包直接使用this都为window对象。即闭包内只要有确定值(非形式参数)都会被设置,因此除形参外后续运行时不会被再次传入新值。

作用：
1. 通过多层实现，突破(函数)作用域限制，且减少全局变量。
2. 立即自动执行。
3. 内层函数可以引用存在于包围它的外部函数的变量，即使外层函数的执行已经中止。
例：for循环中的计数器i传入内部新创建的闭包函数，闭包函数引用的是i为当前循环中的值。若为非闭包，则由于动态创建函数对象，此时(循环时)内部函数先未被立即调用而是只运行完循环。对象创建后再调用内部的函数，此处i已为定值，之前的i由于未被引用已被丢弃。如下例：
`for(var i=0;i<10;i++){setTimeout(function(){alert(i)},(i+1)*100);}`
[(closure)闭包ref](http://jibbering.com/faq/faq_notes/closures.html)

```javascript
function addGen(num)
{
    return function(num2)
        {
	    return num + num2;
	};
}
var ret = addGen(5); //返回值为匿名函数，且作用域中num=5
var trueret = (ret(3) == 8);
```

### 2.1.5 上下文对象--通过this变量体现，指向当前代码所处对象

> NOTE:直接调用函数时(上下文对象未设定)，默认指向全局对象window

```javascript
var obj=
{
    attr1:5;
    yes:function()
    {
		// this == obj
		this.val = true;
    },
    no:function()
    {
 		this.val = false;
    }
};
alert(obj.val); //显示为undefined
obj.yes();
alert(obj.val == true);
window.no = obj.no; //此处window获得no function
alert(window.val); //显示为undefined
window.no();  //this指向window，已与obj无关，obj.no()对window.val无影响。
alert(obj.val == true);
alert(window.val == false);

// call对特定对象(上下文)调用函数
function changeColor(color)
{
    this.style.color = color;
} 
var object2 = document.getElementById("lis");
changeColor.call(object2,"white");
```

### 2.2 创建对象--成功在于new。js没有类的概念，对象(指函数)本身可用来创建新对象，继承其他对象。原型化继承(prototypal inheritance).

#### 2.2.1 创建对象
* var obj = new Object();
* var obj={};

function method1(){};

//设置属性1:

```
function Object(attr1,attr2,method1)
{
	this.arg1 = attr1;
	this.arg2 = attr2;
	this.method2 = method1;
	this.method2 = function(){};
}
var obj = Object(attr1,attr2,method1);
```

//设置属性2:

```
var obj = {
	arg1:attr1,
	arg2:attr2,
	method2:function(){};
}
```

//设置属性3:

```
obj.arg1 = attr1;
obj.arg2 = attr2;
obj.method2 = function(){};
```

实例都包含constructor属性,并可调用。*instance.constructor == ObjFunc*。

```javascript
function User(attr1){this.attr1 = attr1;}
var me = new User("Mike");
var he = new me.constructor("Blo");
```
#### 2.2.2 公共方法--对象每个实例中都可使用。*构造函数设置属性，原型函数添加方法*
> prototype(原型)属性,包含一个对象，此对象可作为所有新副本的基引用(base reference)。此对象的所有属性能在每个实例中找到。
prototype属性对主对象(函数)添加方法，实例对象则没有prototype属性。(因为其实是对类添加了方法)

```
function Obj(na){this.name = na;};
//prototype的使用,先将传入的参数赋值给this对象，再在新方法中调用此参数。
Obj.prototype.newFunc = function(){alert(this.name); return this.name;}
var ob = new Obj("somename");
//实例其实调用Obj对象的方法，因此上两行交换顺序，此行代码依然执行
ob.newFunc(); 
```

#### 2.2.3 私有方法
将一个函数funA及此函数的调用放到其他函数中，funA此时就是私有方法
[private members](http://javascript.crockford.com/private.html)

#### 2.2.4 特权方法(privileged method)

SUMMARY:不用this指向的属性(方法)(即函数内部变量)为私有属性(方法)，外界不能直接以Obj.prop(调用属性)修改其值。

```
function User(attr1)
{
    var privateVar = 24;
    // func2为特权方法，动态生成(方法在新对象实例化时生成)，运行时添加到对象中，而不是第一次编译时生成
    this.func2 = function(){return privateVar;};
    this.setattr2 = function(Var2){this.privateVar=Var2};
    this.attr1 = attr1;
}
```

#### 2.2.5 静态方法--其他方法以对象的静态属性形式存在，作为一个属性不能在该对象的实例上下文中访问，而只属于主对象本身的上下文中.
优点：保证对象的命名空间整洁
User.staticFunc = function(){};
(此处不需要User.prototype，也不是instance.staticFunc)。

> NOTE:根本方法之一：快速、静态地提供与其他代码的接口，同时保持可理解性。


## 3 *可重用代码*

### 3.1 原型式继承（prototype inheritance)(较适合单继承)--对象的构造函数可以从其他对象中继承方法，其他新对象都可基于原型对象构建。原型(prototype)本身并不从其他原型或构造函数中继承属性，而从实际对象继承属性。

{
//User(构造函数)的原型从Person实际对象中继承属性。
User.prototype = new Person();
new User(); // 此后新User对象都会继承Person对象所有的方法。
}

### 3.1.2 类式继承
[class inherit](crockford.com/javascript/inheritance.html)
[new inherit strategy](http://crockford.com/javascript/prototypal.html)

new f() == f.prototype()
new f() produce a new object that inherits from f.prototype()

```
// an operator that implements true prototypal inheritance.o is an old object.
function object(o){
    function F(){}
    F.prototype = o;
    return new F();
}

//Here is another formulation:
Object.prototype.begetObject = function () {
    function F() {}
    F.prototype = this;
    return new F();
};

var newObject = oldObject.begetObject();

/*The problem with the object function is that it is global, and globals are clearly problematic. The problem with Object.prototype.begetObject is that it trips up incompetent programs, and it can produce unexpected results when begetObject is overridden.
So I now prefer this formulation:
*/
if (typeof Object.create !== 'function') {
    Object.create = function (o) {
        function F() {}
        F.prototype = o;
        return new F();
    };
}
newObject = Object.create(oldObject);
```

### 3.1.X call继承

```
function paren（para1）{
    this.attr1 = para1;
    this.attr2 = 21;
}；

function chil（para2）{
    //使用call使chil获得paren的所有属性,即chil.attr1 = para2;
    paren.call(this, para2);
}；
for (var i in paren.prototype){
    chil.prototype[i] = paren.prototype[i];
}
```

### 3.1.3 命名空间--{}

var Yahoo = {};
Yahoo.utils = {};
Yahoo.utils.Event = {addEventListener: function(){}};
调用命名空间。
Yahoo.utils.Event.addEventListener();
>> [Dojo](dojotoolkit.org),[YUI](developer.yahoo.com/yui/)

### 3.2.2 清理代码-JSLint--使用===，使用代码块{},使用;
null,false,undefined求值结果都为false

=== !== 判断变量的显式值(explicit value)
null == false; 0 == undefined;
null !== false; 0 === 0; 0 !== undefined;

### 3.2.3 压缩代码
1. JSMin
2. Packer
### 3.3 分发--[JSAN](openjsan.org)

### 3.4 测试--JSUnit,J3Unit,Test.Simple

******

## 5. 分离式js

### 5. DOM元素(3种node type)
parentNode,prevSibling,nextSibling,firstChild,lastChild.
document.ElEMENT_NODE == 1;
document.TEXT_NODE == 3;
document.DOCUMENT_NODE == 9;

```
// 为所有HTML DOM元素动态绑定以下新DOM遍历函数,返回下一个元素节点。
HTMLElement.prototype.next=function()
{
    //如此可进行链式调用elm.first().next().next()而非next(next(first(elm)));
    var element=this;
    do{
	element=element.nextSibling;
    }while(element && (element.nodeType != 1);
    return element;
}
```

# 5.3 *浏览器渲染操作顺序*
1. HTML解析完毕
2. 外部脚本和样式表加载完成。
3. 脚本(js)在文档内解析并执行。
4. HTML DOM完全构造。
5. 图片与外部内容加载。
6. 网页加载完成(window.onload)

### 5.3.2 加载问题:header中的脚本先执行则无法调用body中的DOM。
1. 等待整个网页加载完成(图片与外部内容加载，DOM加载完成)再执行脚本。使用addEvent为window.onload绑定回调函数。`addEvent(window,"load",function(){});`
2. 页面中途嵌入的行内脚本只能访问该位置前的DOM，因此在页面最后元素前嵌入行内脚本，检查DOM是否加载完成。
(在header中定义函数，在页面最后运行函数，不推荐)
3. 监听DOM加载状态(DOM可用便调用脚本，而不必等图片加载)

```javascript
function domReady(f)
{
	
	if(domReady.done) return f();
	if(domReady.timer){
		domReady.ready.push(f);
	} else {
		addEvent(window,"load",isDomReady);
		domReady.ready = [f];
		domReady.timer = setInterval(isDomReady,13);
	}
}
function isDomReady(){
	if(domReady.done) return false;
	// alert("ru1");
	if(Document && Document.getElementById && Document.getElementsByTagName && Document.body)
	// if(20)
	{
		clearInterval(domReady.timer);
		domReady.timer = null;
		for(var i=0; i < domReady.ready.length; i++)
		{
			domReady.ready[i]();
		}
		domReady.ready = null;
		domReady.done = true;
	}
}
function tag(name,ele){
	te = Document.getElementByTagname(name);
	return te;
}
// alert(21);
domReady(function(){
	alert(20);

	alert("dom loaded");
	tag("h1")[0].style.border = "4px solid black";
});
```

### 5.4 其他HTML中查找元素：类选择器(遍历搜寻)，css选择器，XPath

```
function hasClass(name, type){
	var r = [];
	var re = new RegExp("(^|\\s)" + name + "(\\s|$)");
	var e = document.getElementsByTagName(type||"*");
	for(var j=0;j<e.length;j++){
		//TODO：需确认e[j]是否能被直接测试。
		if(re.test(e[j])){
			r.push(e[j]);
		}
	}
	return r;
}
```

cssQuery("div > p,form");以css形式选择元素。

$("div.links[p]");css和xpath混合的选择元素


### 5.5 获取元素内部值：innerHTML,element.nodeValue.

### 5.6 操作元素特性(attribute)：一旦加载到DOM，就会自行产生(）表示HTML表单元素的变量formElem的一个新的关联数组。如下例。

用以下方法获取或设置特性，可设置任意名称
* elem.getAttribute("attrName");
* elem.setAttribute("attrName","attrValue");

用以下方法获取或设置已内置的几种特性(相当于)关键字，可能遭遇不兼容
* elem.value
* elem.id
* elem.classname = "clsValue";

<form name="myform" action="" method="POST">...</form>

//以上表单自动生成如下变量但不可被显式引用调用。
formElem.attributes = {
    name: "myform",
    action: "",
    method: "POST"
};

document.getElementByTag("form")[0].getAttribute("method");

```
function attr(elem,name,value)
{
    /* 
    设置或获取属性值，并且以后可通过elem.name来快速获取属性值。
    */
    if(!name || name.constructor != String) return "";
    
    //使用getAttribute需避免获取的属性与关键字冲突。
    name = {'for':'htmlfor','class':'className'}[name] || name;
    if(typeof value != 'undefined'){
        elem[name] = value;
    	//设置文本节点时elem.setAttribute会为false。
    	if(elem.setAttribute){
    	    elem.setAttribute(name,value);
    	}
    }
    return elem[name] || elem.getAttribute(name) || '';
}

function tag(name)
{
    return document.getelementByTag(name);
}
```

### 5.7 修改DOM

> 创建新DOM元素createElement

```
function create(ele)
{
    //测试是否可用命名空间
    return document.createElementNS?
	document.createElementNS('http://www.w3.org/1999/xhtml',ele):
	document.createElement(ele);
}
```

> 创建文本节点：createTextNode('text2');

插入DOM元素1：
* insertBefore
* appendChild.
* 例：parentOfBeforNode.insertBefore(nodeToInsert,beforeNode);
* 例：parentNode.appendChild(nodeToInsert);

function checkElem2(elem)
{
    // 如果只提供了字符串，则转化为文本节点
    return elem && (elem.constructor == String)?document.createTextNode(elem):elem
}

插入DOM元素2：innerHTML

插入DOM元素3：混合插入

```javascript
function checkElem(a)
{
	var r = [];
	if(a.constructor != Array) a=[a];
	for(var i=0;i<a.length;i++)
	{
		if(a[i].constructor == String)
		{
			var div = document.createElement("div");
			div.innerHTML = a[i];
			for(var j=0;j<div.childNodes.length;j++)
			{
				r[r.length] = div.childNodes[j];
			}
		}
		else if(a[i].length)
		{	
			//DOM节点数组
			for(var j=0;j<a[i].length;j++)
			{
				r[r.length] = a[i][j];
			}
		}
		else
		{
			//DOM节点
			r[r.length] = a[i];
		}
	}
        return r;
}

function before(parent,before,elem)
{
    //若只传beforeNode与nodeToInsert也可行。为了传参数按习惯顺序需全部重传值。
    if(elem == null)
    {
	elem = before;
	before = parent;
	parent = before.parentNode;
    }
    var elems = checkElem(elem);
    for(var i=elems.length - 1;i >= 0; i--)
    {
	 parent.insertBefore(elems[i],before);
    }
}
```

### 5.8 删除节点NodeParent.removeChild(NodeToRemove);

```javascript
function remove(elem)
{
    if(elem) elem.parentNode.removeChild(elem);
}
function empty(elem)
{
    while(elem.firstChild) elem.removeChild(elem.firstChild);
}
```

****

## 6 事件Event
javascript的事件模型完全异步。

1. 线程程序：不断检查条件是否满足
<script>
while(!window.loaded()){};
...
</script>
此while会阻塞其后的代码运行，动作不会发生，并直接跳出当前script代码块。

2. 异步程序：使用事件处理函数注册回调函数，事件触发时调用回调函数。

### 6.1 事件调用
2种事件，捕获与冒泡只触发一种。
1. 事件捕获：从document的事件处理函数一直往下到目标元素的处理函数发生，触发，形成树。
2. 事件冒泡：元素重回树中，事件处理函数往上直到document按顺序触发。

```
<body>
    <li>
	<a>link</a>
    </li>
</body>
<script>
    var li = document.getElementsByTagName("li")[0];
    li.onmouseover = function()
    {
	this.style.backgroundColor = 'blue';
    }
    li.onmouseout = function()
    {
	this.style.backgroundColor = 'white';
    }
</script>
```

当鼠标从li移动到a上时，其实发生了li.onmouseout事件，但由于li内部元素a的冒泡，立即触发了li.onmouseover事件。
即使<a>与<li>不在同一位置，鼠标移动到a上时依然会触发onmouseover并冒泡到li上。这是由于此时事件调用忽略了捕获事件阶段，是因为现在绑定监听函数的方式是--通过设置元素的onevent特性，这种方式只支持冒泡，不支持捕获。

```
function stopBubble(e)
{
    //若能传入事件对象，则为非IE浏览器，支持stopPraogatation。
    if(e&&e.stopPropagation){e.stopPropagation();}
    //不能传入则仅有全局事件对象window.event
    else{window.event.cancelBubble = true;}
}

/*
//调用回调函数需传入独立的事件对象e。
elem.onmouseover = function(e)
{
    this.style.border='1px solid red';
    stopBubble(e);
};
*/
```

> NOTE:一般处理键盘鼠标时，要注意阻止冒泡。

#### 6.2.4 事件处理函数的特性
1.以某些方式访问的事件对象包含有关于当前事件的上下文信息,例如键盘敲击(onkeypress)可访问对象的keyCode属性

### 6.2.4 浏览器的默认行为(如右键单击，Ctrl+S保存，点击链接跳转)不能被stopBubble阻止。

```
function stopDefault(e)
{
    if(e&&e.preventDefault) e.preventDefault();
    else window.event.returnValue = false;
    return false;
}
```

在时间处理函数的末尾使用
return stopDefault(e);

### *6.3 绑定事件监听函数*

1. 传统绑定：DOM元素绑定一个函数作为它的属性。

> element2.bindEvent2 = function(){}; //bindEvent2如onkeypress,onsubmit等。
* 优点：简单，可使用this。
* 缺点：无捕获，只能DOM元素1次只能绑定1个函数。且只会调用属性最后赋值的那个函数。

2. DOM绑定：W3C(IE外皆可)，作为每个元素的函数出现，参数3为启用或禁用捕获的布尔标记。

> element2.addEventListener('event2',function(){},false); //event2如submit,keypress,不加on。false(冒泡),true(捕获)
* 优点：可捕获和冒泡，可使用this，事件对象总是通过函数的第一个参数获取。同一个事件名绑定多个函数不会被覆盖。
* 缺点：IE不可用，IE为element.attachEvent('bindEvent2',function(){});IE不支持捕获，IE的this指向window

3. 新事件监听函数[addEvent](dean.edwards.name/Weblog/2005/10/add-event/)
唯一缺点：仅支持冒泡，因为他深入使用了传统绑定。
[addEvent from John Resig](https://johnresig.com/projects/flexible-javascript-events/)
```
//addEvent from John Resig
function addEvent( obj, type, fn ) {
  if ( obj.attachEvent ) {
    obj['e'+type+fn] = fn;
    obj[type+fn] = function(){obj['e'+type+fn]( window.event );}
    //obj[type+fn] = function(){fn( window.event );}如此写，由于fn并未被设为原型，则函数触发时，fn指向window.fn而非obj.etypefn.fn
    obj.attachEvent( 'on'+type, obj[type+fn] );
  } else
    obj.addEventListener( type, fn, false );
}
function removeEvent( obj, type, fn ) {
  if ( obj.detachEvent ) {
    obj.detachEvent( 'on'+type, obj[type+fn] );
    obj[type+fn] = null;
  } else
    obj.removeEventListener( type, fn, false );
}



//将函数设置为对象的一个临时属性，如此函数中的this才指向对象而非window。
obj.tempAttr = function(){};
obj.tempAttr(event);

//antherFunc函数由于只是引用而未复制，因此其默认的this指向window
obj.tempAttr = function(anotherFunc(window.event)；){};
//修改后
obj.anotherAttr = anotherFunc;
obj.tempAttr = function(
    //此刻调用的anotherFunc指向obj而非window
    obj.anotherAttr(window.event)；
    ){};
```

```javascript
function addEvent(element,type,handler)
{
    // param：element，event2，function
    // 不同函数生成不同ID
    if(!handler.$$guid) handler.$$guid = addEvent.guid++;
    // 每个元素建立不同类型事件的表
    if(!element.events) element.events = {};
    var handlers = element.events[type];
    if(!handlers)
    {
	handlers = element.events[type]= {};
	if(element["on"+type]) handlers[0] = element["on"+type];
    }
    handlers[handler.$$guid] = handler;
    element["on"+type] = handleEvent;
}
addEvent.guid = 1;

function handleEvent(event)
{
    var returnValue = true;
    event = event|| fixEvent(window.event);
    var handlers = this.events[event.type];
    for(var i in handlers)
   {
	this.$$handleEvent = handlers[i];
	if(this.$$handleEvent(event)===false) returnValue = false;
    }
    return returnValue;
}
```

事件类型：鼠标，键盘，UI(onfocus,onblur),表单，加载和错误(load,unload,错误事件追踪)。
增加可用性：在ele.onfoucus = ele.onmouseover =function(){};以响应键盘事件

### 分离式脚本编程(确保javascript，css禁用也不会出问题).
1. 检查所有功能函数是否存在。
2. 使用DOM快速统一访问元素。
3. 使用DOM和addEvent为文档动态绑定所有事件。

******

## 7 CSS

```
function getStyle(elem,name)
{
	if(elem.style[name]) return elem.style[name];
	else if(elem.currentStyle) return elem.currentStyle[name];
	else if(document.defaultView&&document.defaultView.getComputedStyle)
	{
		//textAlign需转换为text-align
		name = name.replace(/([A-Z])/g,"-$1");
		name = name.toLowerCase();
		var s = document.defaultView.getComputedStyle(elem,"");
		return s&&s.getPropertyValue(name);
	}
	else 
		return null;
}
```

### 7.1 动态元素

css元素定位
1. static(default value):简单地遵循文档的普通流动(flow),left,top无效
2. relative:遵循flow，left,top有效
3. absolute:跳出普通flow，相对第一个非static的parent元素定位,没有则相对document定位
4. fixed:相对浏览器窗口定位，忽略浏览器滚动条。

```javascript
> NOTE:offset为elem的直接属性。
//获取页面中的位置,elem.offsetParent对象，elem.offsetLeft数值
function pageX(elem)
{
    return elem.offsetParent?
    elem.offsetLeft + pageX(elem.offsetParent):
    elem.offsetLeft;
}
function pageY(elem)
{
    return elem.offsetParent?
    elem.offsetTop + pageY(elem.offsetParent):
    elem.offsetTop;
}

//获取相对父元素的位置,offsetParent不能确保返回真实的parent。
function parentX(elem)
{
    return elem.parentNode == elem.offsetParent?
    elem.offsetLeft:
    pageX(elem)-pageX(elem.parentNode);
}

//获取相对css的位置
function posX(elem)
{
    return parseInt(getStyle(elem,"left"));
}

//设置元素位置（与当前位置无关）
function setX(elem,pos)
{
    elem.style.left = pos + "px";
}

//设置元素相当于当前位置的偏移距离
function addX(elem,pos)
{
    setX(elem,posX(elem)+pos);
}

// 获取高度
function getHeight(elem)
{
    return parseInt(getStyle(elem,"height"));
}

//获取元素高度或已隐藏元素的最大可见高度。
function fullHeight(elem)
{
    if(getStyle(elem,"display") != 'none')
    {
	return elem.offsetHeight || getHeight(elem);
    }
    //display为none则无法获取height，display=''其实是block。
    void old = resetCSS(elem,{
	display:'',
	visibility:'hidden',
	position:'absolute'
    });
    var h = elem.clientHeight || getHeight(elem);
    restoreCSS(elem,old);
    return h;
}
function resetCSS(elem,prop)
{
    //设置新属性并返回element的旧属性。
    var old = {};
    for(var i in prop)
    {
	old[i] = elem.style[i];
	elem.style[i] = prop[i];
    }
    return old;
}
function restoreCSS(elem,prop)
{
    for(var i in prop)
    {
	elem.style[i] = prop[i];
    }
}
```

### 元素可见性
1. visibility:保持元素普通流的属性的相关影响，仅隐藏内容。
2. display:
  * inline:遵循文本的普通流动
  * block:打破文本的普通流动
  * none:完全隐藏，包括位置。

```
function hide(elem)
{
    var status = getStyle(elem,'display');
    if(status != 'none')
    {
	elem.$oldDisplay = status;
	elem.style.display = 'none';
    }
}
function show(elem)
{
    elem.style.display = elem.$oldDisplay || '';
}
```

3. 透明度
function setOpacity(elem,level)
{
    if(elem.filters) elem.style.filters = 'alpha(opacity=' +level +')';
    else elem.style.opacity = level/100;
}

### animation
1. 滑动
function slideDown(elem)
{
    elem.style.height = '0px';
    show(elem);
    var h = fullHeight(elem);
    for(var i = 0; i<=100; i+=5)
    {
	//setTimeout(f,10),setTimeout(f,20)...setTimeout(f,1010)
	//开启多个timeout，传入所有i后开始运行而非每传入i就运行一个timeout。
	(function()
	{
	    var pos = i;
	    setTimeout(function()
	    {
		elem.style.height = pos/100*h + "px";
	    },(pos+1)*10);
	})();
    }
}

### 浏览器信息--鼠标键盘滚动条。

1. 获取光标相对整个页面的位置
function getX(e)
{
    e = e || window.event;
    return e.pageX || e.clientX + document.body.scrollLeft;
}
获取光标相当于当前交互元素的位置
function getElementX(e)
{
    return (e&&e.layerX)||window.event.offsetX;
}

2. 视口:浏览器滚动条内的区域。

```
// 返回页面高度，增加内容可能改变
//elem.scrollHeight;elem的整体高度(不含border)
//elem.scrollLeft;elem当前视口左侧(不含border)相对与elem元素左侧(不含border)的距离。
function pageHeight()
{
    return document.body.scrollHeight;
}
// 返回左边滚动偏移量。
function scrollX()
{
    // 用于IE6/7标准。
    var de = document.documentElement;
    return self.pageXOffset || (de && de.scrollLeft) ||
    document.body.scrollLeft;
}
function scrollY()
{
    // 用于IE6/7标准。
    var de = document.documentElement;
    return self.pageYOffset || (de && de.scrollTop) ||
    document.body.scrollTop;
}
//调整滚动到的位置。
window.scrollTo(0,pageY(document.getElementById("body"));

//获取视口尺寸
function windowHeight()
{
    var de = document.documentElement;
    return self.innerHeight||(de&&de.clientHeight)||
    document.body.clientHeight;
}

//拖放 [DOM-DRAG](boring.youngpup.net/2001/domdrag)
Drag.init(element)
```

## 库
简单库：moo.fx,jQuery

```
//展开并收回
new fx.Height("side",
{
	duration:1000,
	onComplete:function(){
		new fx.Height("side",{duration:1000}).hide();
	}
}).show();

$("#side").slideDown(1000,function()
{
	$(this).slideUp(1000);
});
```

//长宽透明度同时收缩的动画
$("#body").hide("fast");

### DHTML库的王者:[scriptaculous](script.aculo.us),基于Prototype库
prototype.js
scriptaculous.js
effects.js
dragdrop.js

window.onload = function()
{
    // 将ID为list的列表变为可拖动的列表
    Sortable.create('list');
}


## 9 表单处理 属性可被直接调用。

```
//检查输入元素是否键入了信息
function checkRequired(elem)
{
    if(elem.type == "checkbox" || elem.type == "radio")
	return getInputsByName(elem.name).numChecked;
    else return elem.value.length > 0 && elem.value != elem.defaultValue;
}
function getInputByName(checkName)
{
    var results = [];
    results.numChecked = 0;
    var input = document.getElementByTagName("input");
    for(var i=0; i<input.length;i++)
    {
	if(input[i].name = checkName)
	{
	    results.push(input[i]);
	    //已被选中会有checked属性。
	    if(input[i].checked) results.numChecked++;
	}
    }
    return results;
}

window.onload = function()
{
    document.getElementByTagName("form")[0].onsubmit = function()
    {
    var elem = document.getElementById("age");
    if(!checkedRequired(elem))
    {
	alert("require field is empty--age");
	return false;
    }
    var elem = document.getElementById("name");
    if(!checkedRequired(elem))
    {
	alert("require field is empty--name");
	return false;
    }
    };
};
function checkEmail(elem)
{
    return elem.value =='' ||
	/^[a-z0-9_+.-]+\@([a-z0-9-]+\.)+[a-z0-9]{2,4}$/i.test(elem.value);
}
var elem = document.getElementById("email");
if(!checkEmail)
{
    alert("email wrong");
}
function checkUrl(elem)
{
    return elem.value == '' || !elem.value=='http://' ||
	/^http:\/\/([a-z0-9-]+\.)+[a-z0-9]{2,4}.*$/.test(ele.velue);
}
```

### 8.2 表单动态验证

```
//设定表单检验规则
var errMsg = {
    required: {
        msg: "this field is required",
        test: function(obj){
            return obj.value.length>0 || load || obj.value != obj.defaultValue;
        }
    },
    email: {
        msg: "email is not valid",
        test: functino(obj){
            return !obj.value || /^[a-zA-Z0-9_+.-]+\@([a-zA-Z0-9-]+\.)[a-z0-9]{2,4}$/i.test(obj.value);
            }
    }
}
//设置blur时检验，习惯性return true。
element.addEventListener("blur",
    function(){
        return validateBlock();
    });
```

## 9 图库

* lightbox
* thickbox

附录A：
1. var obj = {}; obj不为null，而是object对象，判断为true。

## BOM操作浏览器--如window的属性，document的属性
window.navigator.userAgent
window.location
document.clientX
document.documentElement.scrollLeft

var newWin = window.open('about:blank', '_blank')
document.write会清除所有内容并重写
window.close(); //需先用window.open('close.html')来打开才可调用close

## cookie处理
document.cookie

function setCookie(key, value, expireDay){
	var oDate = new Date();
	oDate.setDate( oDate.getDate() + expireDay );
	document.cookie = key+ '=' + value + '; expires="+ oDate;
}
function getCookie(key){
	var arr = document.cookie.split('; ');
	for(var i = 0; i <arr.length; i++){
		var arr2 = arr[i].split('=');
		if( arr2[0] == key){
			return arr2[1];
		}
	}
	return '';
}

function removeCookie(key){
	setCookie(key,'',-1);
}