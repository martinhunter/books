全部资源链接： [github](https://github.com/DeathKing/Learning-SICP)

中文字幕视频： [计算机程序的构造和解释-视频（SICP）【中英字幕】【FoOTOo&HITPT&Learning-SICP】](https://www.bilibili.com/video/av8515129?t=1477)

原版：[Structure and Interpretation of Computer Programs](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-001-structure-and-interpretation-of-computer-programs-spring-2005/)

SICP书： [网页版本](https://mitpress.mit.edu/sicp/)

SICP书： [HTML5版本](https://sarabander.github.io/sicp/)

答案： http://community.schemewiki.org/?SICP-Solutions

Chez Scheme作为练习环境： [Chez Scheme](https://cisco.github.io/ChezScheme/)

其他资源：
> [伯克利的CS61A Python版](http://composingprograms.com/)
> [CS61AS Racket版](http://berkeley-cs61as.github.io/index.html)
> [新加坡大学的JavaScript版](https://www.comp.nus.edu.sg/~cs1101s/sicp/)

```
当前md文档中转到相应字段markdown rule：
1. `# `,`## `等皆替换为`#`
2. 删除其后所有符号\,*,+,.,。,(,`等
3. 所有空格替换为`-`

Example:

original: ## \* of it. \**

checked: #-of-it-

false:
1. #\*-of-it-\**
2. #-of-it-*
3. #\*-of-it-\*
```

***
***
***

## Index

lec1a: 什么是computer science(engineering)

* 目的： 构建实现的过程
* 介绍达到（简单或复杂的）目的所需要的基本结构
* 递归：逐渐逼近目标值

lec1b: 计算过程

* 使用代换模型计算
* 时间复杂度（运行步骤），空间复杂度（存储的内存大小，树的最深深度）与多进行一次递归之间的关系

lec2a: 过程作为对象

* 将公共模式作为对象传递，并且可在内部传递

lec2b: 复合数据，一种新的数据表示方法，可跟基本数据一样被使用

* 创建cons结构来将分子与分母绑定，并使用car,cdr取值
* 创建构造函数与取值函数来构成一层抽象（隔开基本数据和使用），如此外部只要传递合适的对象即可处理

lec3a: 创建一种图像语言escher

* map: 一个抽象出来的公共模式，并以过程和数据作为参数
* 构建多层语言，具有高度灵活性，且每层语言谈论的对象由上一层建立


lec4b: 通用运算符

* 使某一层语言可有多种实现，且使上层语言可调用所需的那个底层（即带类型的数据
* date-oriented-objected,对象自身携带着该如何处理它的的信息
* 每层对目标数据增加自身的类型
* 通用运算符自身便可递归调用，如此形成庞大系统如((x²+2x+3)*(x+5))+4x，'+用新的通用运算符ADD替换

lec5a: 赋值与副作用

* 约束变量，自由变量（设置了作用域/环境，替换模型的基础）
* 有独立状态的独立对象构成系统（面向对象）

lec5b: 计算对象

* 非预期的共享，对象间的非预期交互导致bug
* **赋值使变量从指明一个值变为指明一个地址**

特殊文本标记
- (#)表示重要概念
- (?)表示不清楚的问题
- (-?)表示暂不深入讨论

Key Points
- [Core](#A2-three-techniques-for-controlling-complexity)
- [Importance of procedure](#Chris Strachey将过程或是函数视为程序设计语言中的第一级元素)
- [The goal](#与其说设计程序不如说是设计语言)
- [赋值的真正作用](#赋值是使过去和未来产生差别的事物)

# Contents

***

# A.0 the essense of computer science.
> computer it's not about computer or science,science/engineering is process.

The essense of computer science is how to formalize intuitions about process,how to do things.Starting to develop a way to talk precisely about how-to knowledge as opposed to geometry that talks about what is true.
计算机科学的本质：如何对计算过程进行形式化表述,如何解决问题，创造一套可以精确表述问题处理过程的方法。

## A.1 imperative knowledge 指令型知识（实际运行过程）
#### `procedures(过程/程序)` are going to be the way of talking about imperative knowledge.
a procedure will end up being another procedure，a general strategy that talks about a general strategy.
一种生成过程的过程,利用此递归性可讨论自身或所有新产生的过程.
通过procedure来讨论指令型知识

## A.2 three techniques for controlling complexity
### 1. black-box abstraction
* primitive objects （基本对象）
  1. primitive procedure ( exp: + - * / < = )
  2. primitive data ( exp: 22 23.4 )
* means of combinition （构造大东西，构造函数）
  1. procedure composition ( exp: [] composition, COND, IF )
  2. construction of compound data from primitive data
* means of abstraction ( from compound/combinition things ) （从大东西中取元素，选择函数）
  1. procedure definition ( exp: DEFINE )
  2. simple data abstraction( a technique for dealing with compound data )
* capturing common patterns
  1. high-order procedures ( 高阶过程，它的输入、输出、本身都是过程 ）
  2. **data as procedures** （ 最终:达成模糊数据与过程的区别 ）

### 2. conventional interfaces ( 约定接口，可将符合接口标准的不同部分连接起来，并由此构建系统。）
> 例如对各种数据皆使用的`+`,`-`等基本符号，引入新程序,新类型，新元素而不破坏原来程序

* generic operations
* large-scale structure and modularity
* metaphor 1:object-oriented programming
* metaphor 2:operations on aggregates ( 聚焦的操作，称作“流” ，用于数据的计算，如count，min，sum等)

### 3. metalinguistic abstraction 元语言抽象(make new languages)
>the purpose of the new designed languages will be to highlight different aspects of the system
设计意图：强调系统的某一方面,隐藏部分细节，强调其他细节。

* interpretion apply-eval
* example- logic programming
* register machines

##### `最终获得一种无关输入输出的过程，而仅关注元素（过程也是元素）间关系的语言`

##### The process of how lisp interprete itself? `eval and apply` constantly reduce expression to each other.(`eval and apply`不间断地交替进行）
> a magical symbol λ(lambda，用于表示无限)


1. (define (pr x) (someprocess))
2. (define pr (λ (x) (someprocess))
3. (define pr ((define (anonymous x) (somefunc)) anonymous))
1,2,3作用相同，2是3地简写，定义一个匿名符号，并将其返回, 用pr这个符号代表这匿名符号。

pr equals to (λ (x) (someprocess)


# B.0 substitution model( 替换模型，适用于前几节课 )
> 
```
To evaluate an application
  Evaluate the operator to get procedure
  Evaluate the operands to get arguments
  Apply the procedure to the arguments
  Copy the body of the procedure,substituting the arguments applied
   for the formal parameters of the procedure.
  Evaluate the resulting new body.
```

****
# \* if you have the name of a spirit, you have the power of it. \*
****

## B.1 基本知识
#### O(),O is order: 表示复杂程度(时间，空间)的符号
```
(define (+ x y)
	(if (= x 0)
		y
		(+ (-1+ x) (1+ y))))
```

对于上边的过程
time = O(x)
space = O(1)

#### 迭代：iteration
每一层都与上一层无关,上几层的数据丢失也不影响获得最终结果。
#### 递归：recursion
每一层获得的值都需要传递回上一层。
> 1. linear recursion每次只调用自身1次
> 2. tail recursion
> 3. binary recursion每次调用自身2次-如斐波那契数列
>   * time = O(fib(n))
>   * space = O(n)

## `Chris Strachey`将过程或是函数视为程序设计语言中的第一级元素
### The rights and priviliges of first-class citizens(一级元素的权利)
* To be named by variables
* To be passed as argements to procedures
* To be returned as values of procedures
* To be incorporated into data structures

# C.0 Layered System ( Compound data(复合数据))，每层皆可替换。

### data abstraction(数据抽象)是一种通过假定的constructors(构造函数)和selectors(选择函数)将use(数据对象)与它的presentation(表示法)分隔开来的编程方法学。

使用wishful thinking strategy(愿望思维)，即假定复合结构中的某些部分(通常是较底层的功能)已被实现并可直接使用。

通过抽象层边界(abstrction layer，由constructors和selectors组成)分离对象的使用方法成use和presentarion

### *closure*(闭包),每层闭包本身及其复合式都具有相同结构
> the means of combinition in system,put things together and then put together with the same means of combinition.

> 构建的基本数据可组合后形成新的数据，且此新数据可立刻与其他数据再次组合。这种封闭操作可迅速增加复杂度。

## C.1 一种构建cons(序对)的过程
```
(define (cons x y)
	(λ (pick)
		(cond ((= pick 1) x)
			  ((= pick 2) y))))
(define (car p) (p 1))
(define cdr (λ (p) (p 2)))
```

* (cons 1 (cons 2 (cons 3 4)))
* (cons (cons 1 2) (cons 3 4))

LIST:
> 使用cons组合对象时可有不同的组合方式(不同的tree)，选择一种约定的方式来处理，
and it represents a sequence of things as a chain of pairs and ends with a special marker/symbol called nil，
并将这种sequence(序列)称为list。

()中的内容未被调用时就相当于一个list:

1. (define (proc var) (+ var 3)) 存储在??
2. (+ 2 3)存储在一个包含'+','2','3'的list,(car list)为'+'
3. (list '+ arg1 arg2)返回一个过程而非结果，如此后续可调出arg1或进行其他处理。

## C.2 a woodcut by Escher called "Square limit"(方形极限)
> turned into a language by *Peter Hendersion* for discribing fractal figures.

```
(define (for-each proc list)
  (cond ((null? list) "done")
	(else (proc (car list))
	      (for-each proc
			(cdr list)))))
;; constructor a point: make-rect
;; selectors of vertex: horiz vert origin
;; vect is for vector
;; turn a square into arectangle and map points to coordinate position

(define (make-rect origin x y) (cons origin (cons x y)))
(define (coord-map rect)
  (lambda (point)
    (+vect
     (+vect (scale (xcor point)
		   (horiz rect))
	    (scale (ycor pint)
		   (vert rect)))
     (origin rect))))

(define (make-picture seglist)
  ;; 此过程将一系列点，如(0.1,0.3),(0.2,0.5)等连接为一条线并映射到实际的矩形上
  (lambda (rect)
    (for-each
     (lambda (s)
       ;; here s is (car seglist)
       (drawline
		((coord-map rect) (seg-start s))
		((coord-map rect) (seg-end s))))
	 seglist)))

(define r (make-rect (2 2) 7 5))
(define g (make-picture somelist2))
(g r)

(define (beside p1 p2 a)
  (lambda (rect)
    (p1 (make-rect
	 (origin rect)
	 (scale a (horiz rect))
	 (vert rect)))
    (p2 (make-rect
	 (+vect (origin rect)
		(scale a (horiz rect)))
	 (scale (- 1 a) (horiz rext))
	 (vert-rect)))))
```

一种实现特定基本法的新语言内嵌于lisp，并可使用lisp的强大特性
"递归地重复某种组合方法"的一般性思想，重新组合多个过程为新过程

## 与其说设计程序不如说是设计语言
### 1. 对于于系统的结构(工程设计过程)，一种更普遍的观点是将其视作创造一种语言.
> * 创建多层次的语言层,
> * 每层都是一种语言，
> * 每一层都建立当前层的基本(抽象)语言，
> * 每层讨论的对象都由前一层建立)。

### 2. 工程设计过程的一种比较错误的是方法学(methodology)，或者叫神话学(mythology),姑且叫做软件工程。
> 1. 它声称要先精确计算出你的任务，
> 2. 清楚后再分成3个子任务，
> 3. 再细分为几个子任务直到最底层，
> 4. 解决完后回到上一级解决第二个子任务，
> 5. 到达第二个子任务的最底层，
> 6. 解决后回到上一级解决第三个子任务，如此循环。
> * 形成树状结构，每个子节点旨在完成特定任务

**树状结构与层状结构的区别**：分解(decomposition)是按层次还是严格继承分解(levels or sreict hierarchy)

树状:解决特定的问题，不通用，不完备，会伸出许多未知复杂度的分支，同级分支间相互独立，某一分支改变会对此分支下的子分支全部改变，而无法改变其他分支。

层状:解决特定的一类问题，每层都为表达一类事物创建了完备的词汇(a robust system)，确定了每一层遵循的规则以讨论不同层次上的设计,对小的变化不敏感，小改变只导致解决方案的小改动，系统整体依然是连续的。

# D.0 符号化求导,使用从左到右的归约规则(reduction rules)(*)
> d(u+v)/dx = du/dx + dv/dx
> duv/dx = u*dv/dx + dv/dx*v
> 使用reduction rules,先将大问题分解为小问题，小问题解决后，使用递归组合返回唯一结果。
> 如果从右往左则可能匹配多个规则，无法返回唯一结果，例如无法被约分

(tips:)使用'？'对谓词(predicate)结尾

### quatation(引用)，符号为',并非`求表达式值`而是`指代表达式本身`
> example: (eq exp '+)
> 为解决语言歧义问题而加入此符号
> * Q:say your name. A:sam.
> * Q:say your name. A:your name.

### quatation是非常复杂的概念，将其加入一门语言会造成许多麻烦(-?)
> substitution(替换模型)使用quotation in opaque context(不透明上下文)可能会由于语言歧义产生问题,**quatation自身也是不透明上下文的原型**。
> * 'lisa' has four letters.
> * lisa is a good girl.
> * 'a good girl' has four letters.

### 部分求导规则：
* dc/dx = 0
* dx/dx = 1
* dcu/dx = c*du/dx
* d(u+v)/dx = du/dx + dv/dx
* duv/dx = u*dv/dx + dv/dx*v

```
;;rules
(define (deriv exp var)
  (cond ((constant? exp var) 0)
		((same-var? exp var) 1)
		((sum? exp)
		  (make-sum (deriv (A1 exp) var)
					(deriv (A2 exp) var)))
		((product? exp)
		  (make-sum
			(make-product (M1 exp) (deriv (M2 exp) var))
			(make-product (deriv (M1 exp) var) (M2 exp))))
		((more-conds) (correspond-exps))))
;;presentation
(define (constant? exp var)
  (and (atom? exp)
	   (not (eq? exp var))))
(define (same-var? exp var)
  (and (atom? exp)
	   (eq? exp var)))
(define (sum? exp)
  (and (not (atom? exp))
	   (eq (car exp) '+)))
(define (make-sum a1 a2)
  (list '+ a1 a2))
(define A1 cadr)
(define A2 caddr)
(define (product? exp)
  (and (not (atom? exp))
	   (eq (car exp) '*)))
(define (make-product m1 m2)
  (list '* m1 m2))
(define M1 cadr)
(define M2 caddr)

(define foo
  '(+ (* a (+ x x)
	  (+ (+ b x) c)))

>>>(deriv foo 'x)
>>>(+ (+ (* A (+ (* X 1) (* 1 X)))
		(+ 0 (+ X X)))
	 (* (* (* B 1) (* 0 X)) 0))
;;多出许多1，0是由于make-sum，make-product没有对不同情况化简，需增加检测
(define (make-sum a1 a2)
  (cond ((and (number? a1)
			  (number? a2))
		 (+ a1 a2))
		((and (number? a1) (= a1 0)
		 a2)
		((and (number? a2) (= a2 0)
		 a1)
		(else (list '+ a1 a2))))
>>>(deriv foo 'x)
>>>(+ (*A (+ X X)) B)

>>>(deriv foo 'a)
>>>(* X X)
```


## D.1 基于规则代换的模式匹配语言
### pattern-matching(模式匹配,比符号化求导更加通用)，structure of rules
## matching,instantiation,the control structure。将这些自身从规则中分离并封装
* ### pattern:is something that matches the original expression
* ### skeleton:is something you substitute into in order to get a new expression
* ### 骨架:将匹配成功的值替换到骨架中，通过实例化以得到一个新表达式

### 运行过程:
expression(表达式)对象通过matcher(匹配器,已传入匹配规则列表)传递dictionary of matches(包含被匹配到的变量及相应的subexpression(子表达式))并进行相应部分的instantiation(实例化器，已传入相应的骨架列表),产生new expression(新的表达式)。

### matcher:输入pattern,expression,instanced-dictionary,输出dictionary(of instanced-dictionary and new matched parts)

```
(define (match pat exp dict)
  (cond ((eq? dict 'failed) 'failed)
		((atom? pat) ...)
		((atom? exp) 'failed)
		((other-conds) (extend-dict pat exp dict)
		(else
		  (match (cdr pat)
				 (cdr exp)
				 (match (car pat)
						(car exp)
						dict)))))
(define (extend-dict pat dat dict)
  (let ((name (variable-name pat)))
	(let ((v (assq name dict)))
	  (cond ((null? v)
			 (cons (list name dat) dict))
			((eq? (cadr v) dat) dict)
			(else 'failed)))))
```
需要check expression tree and pattern tree simoutaneously

以确保表达式树与模式树的子表达式也能相匹配。

将car写在cdr中的原因:
如果(match (car )),返回'failed,则将'failed传入(match (cdr ))直接返回'failed
如果(match (car )),返回dict+carmatch,再判断(match (cdr )),若成功则返回dict+carmatch+cdrmatch，否则返回'failed。
获得的carmatch(?x y)要传入(match (cdr )中并与(match (cdr ))的cdrmatch不矛盾,如果cdrmatch为(?x 3)则会产生矛盾。

### instantiation:输入dictionary,skeleton,输出expression
```
(define (instantiate skeleton dict)
  (define (loop s)
	(cond ((atom? s) s)
		  ((skeleton-evaluation? s)
		   (evaluate (eval-exp s) dict))
		  (else (cons (loop (car s))
					  (loop (cdr s))))))
  (loop skeleton))
```

### control structure:控制规则如何应用在表达式上
> 检查待化简表达式的每个子表达式(已在matcher的car,cdr树形递归实现)

> 检查每个子节点，在该层次上把规则所对应的骨架实例化，最后使用(garbage in garbage out) simplifier化简,
> 转换为基本对象(如变量)，对复合对象(coumpound objects)细分。

```
(define derive-rules
  '(
	;; 一个匹配常量的模式(?c)的变量c,匹配任意表达式模式(?)的变量v,结果与0这个骨架匹配
	( (dd (?c c) (? v)) 0 )
	;;一个匹配变量的模式(?v)的变量v,对同一个模式变量v求导，v/v=1
	( (dd (?v v) (? v)) 1 )
	( (dd (?v u) (? v)) 0 )
	;;(+ (? x1) (? x2))要匹配(? v)
	( (dd (+ (? x1) (? x2)) (? v))
	  ;; ?表示模式变量，':'表示要代换的对象，即被实例化为x1，x2的值，下2行为骨架
	  (+ (dd (: x1) (: v))
		 (dd (: x2) (: v))) )
	(more-rules )
  )
)

(define dsimp
  (simplifier derive-rules))

>>>(dsimp '(dd (+ x y) x))
>>>用simplifier根据derive-rules匹配'(dd (+ x y) x)，并最终分解为(+ x/x y/x)
>>>(+ 1 0)

;;修改derive-rules以匹配其他规则
```

## D.2 generic operator(通用运算符)，对不同类型的对象皆适用
### D.2.1 方法一：dispatch on type(基于类型的分派)
> 某一层的实现可能有不同方法，对上一层的目标对象加上类型标签，调用下一层中相应的过程。
> 但是将下一次中的过程也都加上相应的标签，例如procedure改成procedure-rectproc，以避免方法冲突。
> 解决方法：适用命名空间

### D.2.2 方法二：data-directed programming(数据导向编程)
> 沿用方法一，并构建存储类型，运算符的表格,使对象加标签的工作自动化

> ```
(define (operate op obj)
  (let ((proc (get (type obj) op)))
    (if (not (null? obj))
        (proc (contents obj))
        (error "undefined op"))))
;;define the selectors using operate(功能是attatch-type)
(define (real-part obj)
  (operate 'real-part obj))
> ```

;;set a default form that stores op,type,op-type.
;;use put to store new type and new op-type
;;use get to get op-type
(put 'rectangular 'real-part 'real-part-rectangular)
(put 'rectangular 'magnitude 'magnitude-rectangular)
(put 'polar 'real-part 'real-part-polar)

(get 'rectangular 'real-part)

### D.2.2 方法三：message passing(消息传递)
不使用类型，而是直接将这些运算符本身与目标对象绑定，而不将运算符存在表格中。

## D.3 generic arithmetic system(通用算术系统)
> 内含多个计算不同种类数的算术程序包，并实现顶层的add,multiply,sub等通用运算
> 每向上一层(且有垂直屏障，即此层有多个方法)都要在对象前加一层类型。

```
;;install complex number
(define (operate-2 op arg1 arg2)
  (if
	;;judge type first
	(eq? (type arg1) (type arg2))
	(let

;;install ordinary number
(define (make-number n)
  (operate/attach-type 'number n))
(define (+number x y)
  (make-number (+ x y))
```

## D.4 计算多项式
对D2中的方法进行组合，以确保高层与底层系统都能在自身需求范围内有效运行

# E.0 
## E.1 赋值，对象不再关联值而是关联储存值的地方(可能随时间变化)
> ### 目的:构造模块化的系统

> 此时substitution model(代换模型)将会失效

procedure! 使用'!'表示赋值操作。
## 赋值是使过去和未来产生差别的事物(#)

## E.2 enviroment model(环境模型,可适用赋值操作)
> 作用似乎是保存公共变量和局部变量（即全局环境与局部环境）

bound(bound variables):a variable,V,is **bound** to an expression,E.use an unused variable,W,to replace V.the meanig of E is unchanged.
约束(约束变量，指形式参数(formal parameter))：一个表达式中的变量用其他变量替换，且表达式语义不变。

自由变量：非约束变量

lambda:约束变量的唯一工具(可用适当的方法避免适用define)，lambda中的形参变量符合约束

scope(作用域):变量的可用范围

### enviroment is a way of doing substitutions virtually
enviroment is a function,or a (structured sort of)table or such thing like that
环境执行虚拟的代换，它代表了一个地方，储存未完成的代换。即变量名可在环境中找到相应的值。由多个过程自身的约束变量形成的框架（表）互相连接而成，各个表保存了自身上下文中的变量。


对于2个对象，enviroment中的变量部分通用，部分不通用，是各自的局部变量（同名变量亦不出错）。

### actions and identity
确认对象是否改变



## E.3 计算对象
### E.3.1 电气系统,各个对象有明显的连接（线）
> #### 适用赋值模拟电路，与或非门，

;;每条线命名目的：可随时存取，供前后其他电路调用。
(define input1 (makewire))
(define input2 (makewire))
(define output (makewire))
(and-gate input1 input2 output)
将输入、输出线路皆作为参数传入。并通过and-gate修改线路的信号值。

## E.3.2 赋值与不赋值创建cons。
### 逻辑学家 `Alonzo Church`

```
;;Alonzo Church created the traditional cons using only lambda
(define (cons x y)
  (lambda (m) (m x y)))
(define (car x)
  (x (lambda (a d) a)))
(define (cdr x)
  (x (lambda (a d) d)))
;;(lambda (v) (+ 2 v)) is the definition of a function
;;((lambda (v) (+ 2 v))) is to eval the function
>>>((lambda (m) (m x y)) (lambda (a d) a))
;;after evaling (lambda (m) (m x y))
>>>((lambda (a d) a) x y)
;;after eval(substitute arguments)
>>>x

;;new way to cons with pointer setter
(define (cons x y)
  (lambda (m)
    (m x
	   y
       (lambda (n) (set! x n))
       (lambda (n) (set! y n)))))
(define (car x)
  (x (lambda (a d as ds) a)))
(define (cdr x)
  (x (lambda (a d as ds) d)))

(define (set-car! x y)
  ;;y is the new pair
  (x (lambda (a d as ds) (as y))))
(define (set-cdr! x y)
  (x (lambda (a d as ds) (ad y))))
```

# F.0 stream processing(流处理)
### 引入赋值造成了什么？造成了需要考虑以下问题。
assignment>
state>
change>
time>
identity object>
sharing>
错误的表达式顺序和别名会产生bug

### F.1 stream使程序更加统一，减少赋值引起的问题
### stream原理：层层筛选得出所需要的值，而非按时间顺序遍历树（轮廓）结构的每个节点

```
;; 流结构类似表但有所不同
(define (cons-stream x y)
  (cons x (delay y)))
(define (head s) (car s))
(define (tail s) (force (cdr s)))
(define (delay x))

;;对一个流结构中的每个值传入某一过程
(define (map-stream proc s)
  (if (empty-stream? s)
	  the-empty-stream
	  (cons-stream
		(proc (head s))
		(map-stream proc (tail s)))))
;;一个流筛选器。
(define (filter pred s)
  ;;pred for predicate，filter matched ones.
  (cond
	((empty-stream? s) the-empty-stream)
	((pred (head s)
	  (cons-stream (head s)
				   (filter pred (tail s))))
	(else (filter pred (tail s)))))
```

### F.1.1 stream的结构,（如同电流一般，边输入边输出，并非等一级得出所有结果再传递给下一级）
(head (tail (filter prime? (E-1 10000 1000000))))
(cons 10000 (delay (E-1 10001 1000000))) 
;; 使用(delay y),对表达式y,产生1个promise，有需要时promise才会计算表达式y。
;; 使用(force (delay y))来调用promise


#### F.1.2 delay:stream的实现核心
> 将事件发生的逻辑顺序与机器中时间发生的顺序解耦(de-couple).
> 放弃程序运行所反映的明确的事件概念，以此自由安排计算顺序

##### 调用类似列表结构如(tail (tail stream))时，是**从内往外**调用(#)

```
;; v1.将exp形成闭包，需要的参数在此时被传入
(define (delay exp)
  (lambda()(exp)))

;; v2.由于失去了时间性，取下一个tail时会重新计算整个tail
;; 因此需将内部的(tail stream)保存，即
;; (tail (tail stream))不需要再计算(tail stream)
;; (tail (tail (tail stream)))不需要再计算(tail (tail stream))
(define (memo-proc no-param-proc)
  ;;memo-proc只在第一次运行时创建一个new-proc，并存储
  (let ((already-run? nil) (result nil))
    (lambda ()
      (if (not already-run?)
	  (sequence
	   (set! result (no-param-proc))
	   (set! already-run? (not nil))
	   result)
	result))))

(define (delay exp)
  (memo-proc (lambda()(exp))))		

;; 直接调用exp
(define (force exp)
  (exp))


;; 实际应用
;; create 1 1 1 1
(define ones (cons-stream 1 ones))
;; create 1 2 3 4
(define integer
  (cons-stream 1 (add-stream integer ones)))
;; create accumulator for a stream 's'
(define (integer-stream s initial-value dt)
  (define int
    (cons-stream initial-value
		 (add-stream (scale-stream dt s)
			     int)))
  int)
(define (add-stream s1 s2)
  (cond ((empty-stream? s1) s2)
	((empty-stream? s2) s1)
	(else
	 (cons-stream
	  (+ (head s1) (head s2))
	  (add-stream (tail s1) (tail s2))))))
(define (scale-stream c s)
  (map-stream (lambda (x) (*x c)) s))
;; 处理斐波那契数列
(define fibs
  (cons-stream
   0
   (cons-stream 1
		(add-stream fibs (tail fibs)))))
```

### F.2.1.normal-order evaluation(正则序求值)
> ### 使所有东西都自带delay，如此定义2个互相调用的对象也不会出错
> ### 直接将参数代换入过程，而不先对参数求值,只代换了计算参数的promise
```
(define y
  (intergal-stream (delay dy) 1 0.01))
(define dy
  (map-square y))
```

### F.2.2.applicative-order evaluation(应用序求值)
> 使用代换模型，先求值所有的参数，再代换调用

```
;;以下调用会出错
(define y
  (intergal-stream dy 1 0.01))
(define dy
  (map-square y))
```

# G.0 元循环
## G.1 eval is a "universal machine"(通用机器)


### infinite loop
```
Y = 
(lambda (f)
  ((lambda (x) (f (x x)))
   (lambda (x) (f (x x)))))

(Y anything)
```


# H.0 逻辑式程序

> 3句箴言
> 1. express what is true
> 2. check if something if true
> 3. find out what is true

不定义明确的计算方向，而是关注关系。

定义（声明）与实际计算过程变得相同。如SQL（查询语言）

	(son-of ada juda)
	(son-of ada gowen)
	(son-of juda sif)
	(son-of juda murl)
	
在逻辑式程序中可得出：

- 描述（新增）gown的son是lily
- 判断sif的grandfa是gowen这个描述是否正确
- sif的grandfa是谁(根据条件查找）
- murl与ada的关系是什么(根据条件查找）
- 等等

	(rule
		;; declare this relashion below is true
		(rela2 ?x ?y ?z)
		;; only when the condition below is true
		(and (rela3 ?x ?y)
			 (rala4 > ?y ?z)))

primitives: new query
means of combinition: add,or,not,lisp-value
means of abstraction: rule

### not的问题

(and (not a) (not b))

and按正则顺序筛选（计算）时，not的位置不同会导致结果的不同

对x直接使用not，则x之外的所有东西形成一个集合，这集合对于x并不可知。
要先列出所有的`是与不是`的关系rule，才能进行正确的推导，但由于物数量过多，想要对物建立所有的`是与不是`的关系是不可能的。


## 寄存器

- factorial machine:有寄存器n,val。
- continue controller machine：记住有穷状态控制器的位置（状态）,有寄存器continue
- 栈：保存和还原n，continue

```

--definition--
(define (fact n)
  (if (=1 n)
      n
    (* n (fact (-1 n)))))

--definition-end--
--machine-language--
;; (fetch n),n is stored in register
;; (save n),(restore n),n is stored in stack
;; (goto (fetch continue)),run proc stored in register continue
(
 (assign continue done)

 loop
 (branch (=1 (fetch n)) BASE)
 ;; save state
 (save continue)
 (save n)
 (assign n (-1 (fetch n)))
 (assign continue AFT)
 (goto loop)

 AFT
 ;; restore state
 (restore n)
 (restore continue)
 (assign val (* (fetch n) (fetch val)))
 (goto (fetch continue))

 BASE
 (assign val (fetch n))
 (goto (fetch continue))

 (fact 4)

 DONE
)
--machine-language-end--

--stack-after-loop--
done
4
aft
(= n 4)
(= continue proc-aft)
3
aft
2
;; n is assigned to 1
--stack-end--

--restore-part--

;; now in register
;; (= n 1)
;; (= continue aft)

(Base)
(assign val 1)
(goto AFT)
(assign n 2) ;;(restore n)
(assign continue aft) ;; (restore continue)
(assgin val (* 2 1))
(goto AFT)
...
(assign n 4) ;;(restore n)
(assign continue done) ;; (restore continue)
;; stack is empty now
(assign val (* 4 6))
(goto done)
(DONE)
--restore-end--

```

organization of register machine

data-paths <--> finite-state controller(完成特定事件，跳转到特定状态)
data-paths <--> stack(实现递归,并维持无穷的假象)