## js：事件驱动

> w3c is outdated, ask MDN(mozilla developer network) for help.

事件处理器（处理settimeout等）在线程空闲之前不会运行

CORE：js是单线程的,实现非阻塞式I/O

运行过程：

1. 调用settimeout
1. 将一个延时事件排入队列
1. settimeout代码块后的代码运行直到完成所有
1. 
1. 队列中有适合触发的事件
1. 虚拟机调用此事件的处理器，现在再去尝试获取变量值


### 异步的计时函数

setInterval和setTimeout事件

浏览器触发频率：约200次/秒

增加频率
- Node.js中：使用process.nextTick
- 垫片(shim)技术：推荐浏览器使用requestAnimationFrame而非setTimeout

### 什么是异步函数

- 一个函数为异步函数：则它会导致将来再运行另一个函数，后者取自于事件队列。
- 若另一个函数作为参数传递给次异步函数，则称其为回调函数。

#### 间或异步函数

如$(function(){});
- 应当在其他脚本运行后再运行
- 但若有缓存，则会先运行

#### 缓存型异步函数
> 是间或异步函数的变种

网页worker对象，结果已缓存，函数同步，否则异步

#### 异步递归，回调存储

不要使用异步递归：通过延时而重复相同的函数调用
使用回调存储：更加高效，库应当提供回调机制

#### 返值

可被同步调用，也可被异步调用

#### 错误处理

只能再回调内部处理远不回调的异步错误

throw：想让应用停止工作时。
不使用throw：进行错误处理{onsuccess ..., onfail ...}

避免2层以上的函数嵌套。方式：激活异步调用之函数的外部存储异步结果

## 分布式事件

> 一个小动作，整个应用到处都引发了反应。可在运行时对其增减任务

### PubSub模式

> publish to subscribers

> 用于多次触发的对象。为一个对象的事件添加多个处理器

作用：PubSub简化了事件命名，分发和堆积

addEventListener和bind都是pubsub模式，node中的eventemitter也是,js里为`$.Callbacks`

exp:创建一个PubSub模式

	PubSub = {handlers: {}}
	PubSub.on = function(eventType, handler) {
		if (!(eventType in this.handlers)) {
			this.handlers[eventType] = [];
		}
		this.handlers[eventType].push(handler);
		return this;
	}

	PubSub.emit = function(eventType) {
		// 将具有length属性的arguments转换为数组
		// 第一个参数为eventType，apply中并不需要
		var handlerArgs = Array.prototype.slice.call(arguments, 1);
		for (var i = 0; i < this.handlers[eventType].length; i++) {
			this.handlers[eventType][i].apply(this, handlerArgs);
		}
		return this;
	}

	/* 释义：var handlerArgs = Array.prototype.slice.call(arguments, 1);
	call:对(arguments,1)调用Array.prototype.slice方法
	Array.prototype将arguments转换为Array对象
	arr.slice(1)获得arr[1:]
	handelerArgs = arguments[1:] */

问题：事件处理器无法知道自身是从事件队列还是应用代码中运行的。

solve:先存储异步事件的队列，其他代码处理完后再触发它们，如此每次只触发一个处理器，以免阻塞线程

	var task = [];
	setInterval(function() {
		var next;
		if (next = task.shift()) {
			next();
		};
	},0)

### 事件化模型

> 既保存数据，又能声明自己发生变化

只要对象带有PubSub接口，就可称之为事件化对象
存储数据的对象因内容变化而发布事件，这些对象称作模型。
模型变化，然后触发事件而导致DOM更新

### 模型事件的传播

事件化模型使用set/get方法来触发

	style.set({font:'Palatino'});  // 触发器警报
	style.get('font');	// 'Palatino'
	style.font;  // 如此获取为'Palatino'
	style.font = 'Comic Sans';  // 不触发
	style.font;  // 如此获取为'Comic Sans'
	style.get('font');  // 仍为'Palatino'

**事件循环与嵌套**

双向绑定：2个模型的取值会彼此关联

为避免无限循环（互相触发）的3种不同方法：

- 模型的一个变化导致同一个模型再次变化，第二次变化嵌套在第一次变化内，不再触发变化。
- 显式声明双向绑定，一个值发生变化时，另一个值通过延时事件异步更新
- 添加{silent:true}选项，先修改所有值，然后触发change事件

### **promise对象**（如ajax）和deferred对象

> 用于仅触发一次的事件，执行/拒绝一次后即失效
> deferred时promise的超集，且可直接触发。而promise则需其他东西触发

## 工作流控制

