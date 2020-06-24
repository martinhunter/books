形式： `$ command: 说明`
<necessary argument> : 实际输入值,必有
[optional command] : 可选值


## base
work space:工作区
staged space:暂存区
commited space：仓库

数据提交到暂存区时会存储一系列文件快照，暂存区中存储了指针指向特定的快照
commit时，创建校验码（checksum）树
恢复到特定commit时，从树对象重新产生快照

When you create the commit by running git commit, Git checksums each subdirectory (in this case,
just the root project directory) and stores them as a tree object in the Git repository. Git then creates
a commit object that has the metadata and a pointer to the root project tree so it can re-create that
snapshot when needed.

.gitignore文件，不追踪的文件

exp: #代表注释，/表示路径，*，.等符合正则匹配

	# comment here
	doc/**/*.pdf

## commands

$ git init: 初始化

$ git add <regex-file> <regex-file2> <regex-fileN>: 向暂存区添加文件或添加已修改的文件，<regex-file>文件名符合正则式
exp: $ git add *.c

$ git commit: 提交变化
-m <'commit-info'>: 必须，对提交进行备注，<'commit-info'>为备注
-a: 跳过git add，提交所有已追踪的修改过的文件

$ git clone <url> [yourName]: 复制url的内容，并创建以<url>仓库名为名[若有yourName则以yourName为名]的新仓库
exp: $ git clone https://github.com/libgit2/libgit2

## lifecycle of the status of files:

	1.untracked      2.unmodified      3.modified      4.staged
	
	1->add-the-file------------------------------------------>4
	                 2->edit-the-file---------->3
									   3->stage-the-file----->4
	1<---------remove-the-file<-2
					 2<-------------------------------commit<-4





$ git status: 检查当前文件状态
-s: 精简显示

$ git diff: 比较工作区和暂存区的文件的不同
--staged/--cached:比较暂存区与最后一次提交的文件

$ git difftool: 可视化软件打开 

$ rm <file>： 只将<file>从工作区中移除

$ git rm <file>： 将<file>从暂存区和未追踪区中移除
exp:$ git rm \*~： 从暂存区和工作区中移除~结尾的文件
$ git rm <file> --cached： 将<file>从暂存区移除，保留在未追踪区中
$ git rm -f <file>： (暂存且有修改时）从暂存区和未追踪区中移除以保护文件意外被删

$ git mv <file> <newName>： 当作移动并重命名

$ git log: 查看历史
-p/--patch: 显示不同
-<number>: number为数字，查看历史条数，通常与-p同用
--stat:缩略信息
--pretty=<oneline/format:<"yourformat">>：以特定方式显示
	- oneline # 一行
	- format:"%h - %an, %ar : %s" # 自定义格式

--graph:显示分支情况，通常与--pretty同用
--since=<time>:设置历史时间
-S <string>:文件中含有string，且string出现的次数相比之前的commit有变化的commit（包括第一次提交）
-- <path/>:放在最后，注意空格，限定有历史变化的路径

$ git commit --amend [-m <newComment>]：将当前暂存区提交，并与之前一次合并，可修改为新备注

$ git reset HEAD <file>: 取消暂存
$ git checkout -- <file>：取消文件的修改

### 远程

$ git remote ： 显示本地已有的远程仓库的名字
-v：显示仓库url和其名称
$ git remote add <remote> <url> ：显式添加远程仓库,<remote>为远程仓库在本地的别名
exp: $ git remote add pb https://github.com/paulboone/ticgit
$ git remote remove <remote>：显式删除

$ git fetch <remote>
git fetch pb

$ git push <remote> <branch>
exp: $ git push origin master

$ git push <remote> <tagname>: 推送特定tag（特定版本），如此其他用户可获得此tag
$ git push <remote> --tags: 推送所有tags
$ git push <remote> :refs/tags/<tagname>: 删除远程tag
$ git push origin --delete <tagname>：删除远程tag

$ git remote show <remote>:显示信息

$ git remote rename <prevName> <newName>

$ git tag ： 显示所有的tag，通常是版本标记
-l <tag-string>": 筛选出符合tag-string的tag
exp: $ git tag -l "v1.8.5*": 
-a <tagName> -m "my version 1.4"：-a为当前commit添加<tagName>，且包含tag自身信息，如作者，添加tag日期
-a <tagName> <git-hash>: 用commit的hash来为这个commit添加tag
-d <tagname>：删除特定tag

“detached HEAD” state：
缺点：直接commit会不属于任何分支，只能用其hash获取。
推荐：commit到一个新分支，$ git checkout -b <branchName> <tagName>

$ git tag <tagName>：轻量级tag，只是为当前commit添加了一个tag

$ git show <tagName>: 显示特定tag的信息

$ git checkout <tagName>: 显示特定tag所在commit的文件

$ git config --global alias.<aliasName> <full-command>: 为<full-command>设置别名<aliasName>
exp:$ git config --global alias.unstage 'reset HEAD --'
result:$ git unstage fileA == $ git reset HEAD -- fileA

HEAD:一个特殊指针，指向当前所在的分支

$ git branch <branch-name>：创建指向当前commit的分支

$ git log --oneline --decorate： --decorate显示当前HEAD指针的指向

$ git checkout 
<branch-name>：切换到<branch-name>分支，此时HEAD指针切换至指向<branch-name>
-b <branch-name>: 创建分支并切换到此分支
-d <branch-name>: merge后去除<branch-name>指针

$ git merge <branch-name>：将<branch-name>合并到当前分支，当前分支后移并指向<branch-name>

Let’s go through a simple example of branching and merging with a workflow that you might use in
the real world. You’ll follow these steps:
1. Do some work on a website.
2. Create a branch for a new user story you’re working on.
3. Do some work in that branch.
At this stage, you’ll receive a call that another issue is critical and you need a hotfix. You’ll do the
following:
1. Switch to your production branch.
2. Create a branch to add the hotfix.
3. After it’s tested, merge the hotfix branch, and push to production.
4. Switch back to your original user story and continue working.
 