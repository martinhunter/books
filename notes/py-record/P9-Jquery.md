## jquery,全部使用函数来进行操作。许多函数操作后返回值为元素对象。因此可继续操作。
使用$(element)选出已有的元素

文档加载
$(document).ready(function(){})简写$(function(){})

链式调用
$('ele1').anonymousfunc1().filter().func1(arg or anotherfunc).func2();
前一个函数的返回值传递给下一个函数。
### jquery selector
格式：$('ele1 ele2 ele3')
例：$('#myId .myClass ul input[name=first]')

解释：选择id为myId下的类名为，myClass下的，ul元素下的，name属性=first的input元素。

#### jquery filter（返回经过筛选的本元素，而非其他元素）
对于jquery selector选出的元素进行过滤。
例：$('div').has('p').not('.class1').filter('.class2').eq(2);
has查看所有子元素（不含本身）是否符合selector的条件，返回元素本身。
filter查看元素本身是否符合selector的条件（因此其中的条件一般是.class或属性[name=xxx],不能是'ul','a'之类)
解释：1.选出所有div。2.在1返回的所有div中选出有p元素（穿透所有子元素）的div。3.在2返回的所有div中选出所有不含class1的div元素。4.在3返回的所有div中选出所有含class2的div元素。5.在4返回的所有div的元素集合中选出第2个元素。

#### jquery filter other obj选择集转移(返回与本元素有某种关系的其他元素）
$('div').prev()
.prevAll();
.next();
.parent('p');=.parent().has('p');  // 选择所有div各自的直接parent元素，并用selector筛选
.children('em');  // 选择所有div各自的直接child元素(不穿透子元素），并用selector筛选
.siblings();
.find('class1')=.children().has('class1');  //返回子元素

#### 对集合中的每一个单独操作
.each(function(index){
  alert($(this).index());
  $(this).animate();
  })
或使用for循环遍历

#### 样式操作(注意属性值可能加上'')
1. 修改：$(obj).css({'color':'red','width':'20px'})
2. 获取obj集合中第一个obj的样式：$objs.css('width')
3. 改类： .addClass("cls") .removeClass("cls1 cls2") .toggleClass("cls3") //toggle需点击切换，自动增加和移除cls3

#### 当前元素的索引值
> 获得匹配元素相对于所有同级元素的索引位置，index()。因此最好把所有li连续写。

#### 简单动效
.fadeIn();
.fadeOut();
.fadeToggle();
.show();
.slideDown();  //向下展开以显示

多次触发的问题解决：.stop().fadeIn();类似clearInterval(timer)

#### 动效(注意参数是否加'')
$objs.animate({'left':'+=50','width':20},1000,'swing',funcAfter(){}) //swing表示缓冲运动，为默认属性。还有linear

多次触发的问题解决：.stop().fadeIn();类似clearInterval(timer)

.offset().left  //返回第一个元素对于文档的位置关系
可视区：$(window)
页面文档$(document)

页面滚动事件：$(window).scroll(function(){})

#### 属性操作
.html('<p>sd</p>')  // 通过html添加新元素效率最高

.val()  //获取值

.prop({'src':'/img/1.jpg','alt':'altecont'})设置或获取属性（非cssstyle）

***
#### 事件
绑定多事件：
.bind('mouseover click',function(){
  $(this).unbind('mouseover'); //mouseover只在第一次触发
  })
  
  
阻止事件冒泡/阻止默认行为：函数中最后写上return false；

事件委托：利用事件冒泡，处理子元素事件（穿透子元素）（包括新添加的子元素）
.delegate('li','click',function)

常见事件
* .blur()
* .mouseover()  // 进入子元素也触发
* .mouseout()
* .hover()  //进出子元素不触发
* $(window).resize()
* .submit()

#### 节点操作
节点已存在会从原有位置删除并插入新位置。

.append('<span>子元素</span>')
.prepend()
.after('<span>后边插入同级元素</span>')

css动画
.cls1{transition:all 1s ease;}
要增加的类样式.cls2{transform:rotate（135deg) }
.cls1加上cls2会用1s完成rotate转换。

**函数节流**
减少mousewheel的高频触发,向下滚动dat=-1，向上dat=1,只触发最后一次
var timer=null;
$(window).mousewheel(function(event,dat){
  clearTimeout(timer);
  timer=setTImeout(function(){},200)
  }）



***
### ajax
> 原理：实例化xmlhttp对象，使用此对象和后台通信，且不影响后续jacascript执行。`同源策略`，只能请求需同一个域下面的资源。

使用node创建本地服务器环境
服务器的da.json内容：{"name"："zhangsan"，"age"：21}

```javascript
$.ajax({
    url: 'js/da.json',
    type:'GET',
    dataType:'json',
    data:{'sendinfo':'infoServerNeeds'},    
}
.done(function(data){
    alert(data.name);
}
.fail(function(){})
```
#### jsonp 
> 原理：通过<script>标签跨域请求数据 

服务器的da.json内容： fnback({"name"："zhangsan"，"age"：21})

```javascript
$.ajax({
    url: 'https://www.baidu.com/sugrec?',
    type:'GET',
    dataType:'jsonp',
    jsonCallback:'fnback',
    data:{'wd':'联想词'},    
}
.done(function(data){
    alert(data.name);
}
.fail(function(){})
```
### jquery UI:拖动操作

#### cookie
> jquery.cookie.js

1. cookie最大4k，在同源http请求中携带传递，可设置访问路径阻止其他路径访问。
2. localStorge为5M或更大，在所有同源窗口中共享，一直有效
3. sessionStorge为5M或更大，在同源的当前窗口关闭前有效

$.cookie('cookiename1','cookievalue',{expires:1,path:'/'})
$.cookie('cookiename1'）

localStorge.setItem("dat","lis");或localStorge.dat='lis';
localStorge.getItem("dat","lis");或localStorge.dat;

实例：只弹一次的窗口
```
$(function(){
    if($.cookie('hasread')==undefiend)){
        $.cookie('hasread',1,{expires:1,path:'/userpage/'});
        $('#block').hide();
    }
})
```

### 移动端js
事件：touchstart,touchmove,touchend,touchcancel(cancel较少用)
点击事件：先touchstart，然后touchend
> zeptojs 移动端js库
> swiper.js swiper.css 滑动效果插件。

##  bootstrap
