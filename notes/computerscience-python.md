## Order



### debug

scientific method to solve the bug:

- study available data
	- include all test results that worked and didn't work
	- include program text
- form hypothesis(guess) with *all* the data
- design a repeatable experiment

key to a valid scientific experiment:

- posssible to refute the experiment
- get useful intermediate results(not just a answer in the end)
- must know expected result

how to design experiment:

- find simplist input that will invoke the bug(so the program does't need to run a long time)
- use binary search(to find the part that is most likely to fall)

实例：

	loop:代码总行数=n
	在n/2处打印期望值及实际值（通常是一些变量）
	依据结果是否符合期望，判断错误在上半段还是下半段。
	branch：若在上半段
	goto loop:在n/4处打印期望值及实际值（通常是一些变量），并判断
	branc：若在下半段
	goto loop:在n*3/4处打印期望值及实际值（通常是一些变量），并判断
	done:直至错误准确所在
	
	可能假设错误需做出新的假设，并重新loop

most common little bugs

- reversed order of arguments
- spelling
- initialization(initialized in and out of loop,forget to reinitialize in loop)
- object vs value equality(when using `==)
- alising(deep and shallow copy)

tips

- keep record of what you tried
- reconsider assumptions(output might not be produced by the expected part of code)
- debug code,don't believe comments(written by others)
- get help,explain what I'm trying to do
- walk away

solve bug
- will the solution solve all problems,is it an independant problem
- what's the result of the change,will it break other things
- tiny up(clean up) code a bit first,rather than adding new code
- make sure you can revert,save old versions.

## algorithm

greedy algorithm：优先达成部分的优化可能导致剩余部分无法达成
例：dogslet，贪婪算法获得doges，会导致lt无法成词。不贪婪可获得单词dogs和let

enumerate

dynamic programming
