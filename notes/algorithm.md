## pre-requests

6.042 math for computer science
6.001 discrete mathematics and probability


## course

1.analysis of algorithms

importance of performance(like money/currency,is a standard to measure/quality which is more acceptable),better performace pays for other things(user-friendliness,security)


2.design of algorithms

## sorting

- max time(upperbound)
- expected time(need assumption of statistical distribution)
- min time(no algorithm needed)


n:实际要处理的元素数量
T(n)：排序n个元素实际所需时间/读取变量次数/进行基本计算的次数。

## 渐近符号

Θ(n³)：只保留最高阶项n³，忽略剩余项

O()：限定上界,`=`表达的含义为`<=`
Ω()：限定下界,`=`表达的含义为`>=`


f(n)=O(g(n))：g(n)为f(n)的上界，`=`表达的含义为`<=`，f(n)是O(g(n))的子集

此时，当n0>0,c>0时，对所有n>=n0，0<=f(n)<=c*g(n)

例:2n² = O(n³)

## solve recursion

### 1.substitution method

T(n)= c*T(prev-n) + n

guess T(n)=O(g(n)) and substitue T(prev-n) with g(prev-n),T(n) = O(g(n)) - const, const>0

NOTE：有时g(n)需带有低阶项才能贴近上界

### 2.recursion-tree method

将多项变为树状结构

Ex: T(n) = T(n/4) + T(n/2) + n²
			
					  phase1
					     n²
			 	  T(n/4)  T(n/2)

					  phase2
						 n²
			 (n/4)²			    (n/2)²
		(n/16)²  (n/8)²      (n/8)²   (n/4)²

					  phaseN
						 n²
			 (n/4)²			    (n/2)²
		T(n/16)  T(n/8)     T(n/8)  T(n/4)
						... 
    T(1)  T(1) 		...  	... 	 T(1)  T(1) 

	每行相加，最终变为T(n) = n² + ... + (5/16)**k*n² <=2n²

### 3.master method

只能计算符合以下形式的递归式：

	T(n) = aT(n/b) + f(n) = a*(aT(n/b/b) + f(n/b))+f(n) = a**2T(n/b/b)+ a*f(n/b)+f(n)

a个相同的子问题，a>=1
每个子问题的规模是n/b（递归的代价）,b>1
f(n)是非递归的代价,f(n)渐近趋正，指对足够大的n，f(n)>0

compare f(n) with n**(log(b)a)

Case 1. 
when f(n) = O(n\*\*(log(b)a - ε)) for ε>0.
T(n) = Θ(n\*\*(log(b)a))

Case 2.
when f(n) = Θ(n\*\*(log(b)a)\*lg(k)n) for some k>=0, 其中lg(k)n 等同于 (log(2)n)\*\*k
T(n) = Θ(n\*\*(log(b)a)\*lg(k+1)n)

Case 3.
when f(n) = Ω(n\*\*(log(b)a + ε)) for some ε>=0 & a\*f(n/b) <= (1- ε')\*f(n) for some ε'> 0 (确保每层越来越小)
T(n) = Θ(f(n))

格式：(n,j=2)∑(j)

	n
	∑ j  = n*(n+1)/2 -1
	j=2

	n
	∑ (j-1)  = n*(n-1)/2
	j=2

insertion-sort(A) | 代价(常数项) | 次数
-|-|-|
for j=2 to A.length | c_1 | n |
key = A[j] | c_2 | n-1 |
i = j - 1 | c_3 | n-1 |
while i>0 and A[i]>key | c_4 | (n,j=2)∑(t_j) |

c_3:某个常数`c`，为分别不同常数项增加后缀`_3`

t_j:while行在j不同时，进行循环的次数不同（花费的时间），因此次数为t_j而非一个定值

whole

