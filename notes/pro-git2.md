### install on Debian(linux)

$ sudo dnf install git-all
$ tar -zxf git-2.8.0.tar.gz
$ cd git-2.8.0
$ make configure
$ ./configure --prefix=/usr
$ make all doc info
$ sudo make install install-doc install-html install-info

$ git clone git://git.kernel.org/pub/scm/git/git.git  # self update

### configurations

pass the option --system to /etc/gitconfig, it reads and writes from this file
specifically

~/.gitconfig or ~/.config/git/config file: Values specific personally to you, the user.You can
make Git read and write to this file specifically by passing the --global option

You can view all of your settings and where they are coming from using:

$ git config --list --show-origin

Set Your Identity globally with --global. for a specific program,run the command without global

$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com

$ git config --global core.editor emacs

$ git config --global core.editor "C:/Program Files/Notepad++/notepad++.exe"
-multiInst -notabbar -nosession -noPlugin"  # on windows

### help

open maunal in the browser:

$ git &lt;verb> help || --help  # exp: git help config

show quick refresher on the available options in dos/bash:

$ git &lt;verb> -h  # git config -h

### structure

not-tracked/modified
tracked/staged(after $git add，置入暂存区，staging area)










## Git Basics

$ git init  # init current directory

$ git init [&lt;directory>]


exp: a basic commit

$ git add *.c
$ git add LICENSE
$ git commit -m 'Initial project version'

$ git clone &lt;url> [$Alias]
\# URL use https:// protocol, you may also see git:// or user@server:path/to/repo.git, 

Checking the Status of Your Files

$ git status
-s  # short description

Tracking New Files or staging modified files

$ git add &lt;file> [&lt;file>]*

exp: .ignore file

	# ignore all .a files
	*.a
	# but do track lib.a, even though you're ignoring .a files above
	!lib.a
	# only ignore the TODO file in the current directory, not subdir/TODO
	/TODO
	# ignore all files in any directory named build
	build/
	# ignore doc/notes.txt, but not doc/server/arch.txt
	doc/*.txt
	# ignore all .pdf files in the doc/ directory and any of its subdirectories
	doc/**/*.pdf

Viewing Your Staged and Unstaged Changes

$ git diff
--staged || --cached  # view diff of staged files(--staged and --cached are synonyms):

Committing Your Changes

$ git commit -m "commit info"
-a  # skip $git add,all tracked(only tracked) files modified will be commited

Removing Files

remove it from your tracked files (more accurately, remove it from your staging area) and then commit
file will not be tracked

$ git rm <file>  # 执行了删除文件，并将删除文件这个修改提交到staging area，且提交后日后不再track此文件(已被删除)
-f  # remove file that's already added to staging area and delete this file,并将删除文件这个修改提交到staging area. 慎用
--cached  #  实际不删除此文件，但会将删除文件这个修改提交到staging area

以上都会将文件从status的untracedFiles中删除，git add file依然可以添加此文件

移动或重命名文件

$ git mv file_from file_to  # 提交后为 renamed:ne.txt -> as/nkknaul ，源地址不会改变，可多次使用mv对目标地址进行转换




Viewing the Commit History

$ git log
--stat
--pretty=oneline
--pretty=format:"%h - %an, %ar : %s" --graph
--since=2.weeks and --until="2020-06-15"
--grep str  # 提交信息中包含str
-S something # 找到something出现次数被修改的提交.例如增加了一次函数调用，就可用-S funcName

NOTE:press q to quit log

Make minor improvements to your last commit

> amend(new commit) doesn't replace last commit,it's just like the last commit never happened, it(last commit) won’t show up in your repository history.

$ git commit --amend  



Unstaging a Staged File

旧版
$ git reset HEAD &lt;file>
$ git checkout -- &lt;file>

新版
$ git restore --staged &lt;file>  # 取消提交
$ git restore &lt;file>  # 取消文件修改

### Working with Remotes

NOTE:&lt;remote>为远程仓库在本地的别名

$ git clone &lt;url>  # automatically sets up your local master branch to track the remote master branch (or whatever the default branch is called)

$ git remote add [&lt;options>] &lt;remote> &lt;url>  # 先添加仓库，remote为url的本地别名

$ git remote  # 查看已添加仓库的别名
-v  # 查看具体信息

$ git fetch &lt;remote>  # update local repo, but it only downloads the data to your local repository — it doesn’t automatically merge it with any of your work or modify what you’re currently working on. You have to merge it manually into your work when you’re ready.

$ git pull &lt;remote> &lt;remote-branch> # git pull is shorthand for `git fetch` followed by `git merge FETCH_HEAD`.automatically fetch and then merge that remote branch into your current branch

$ git push &lt;remote> &lt;branch>

Inspecting a Remote

$ git remote show &lt;remote>

$ git remote rename prev_name new_name

### Tagging

$ git tag  # 显示所有tag

为当前提交状态增加tag

$ git tag -a &lt;tagName> -m "my version 1.4"
-a 为tag名称
-m 为tag保存的信息

$ git show  # 显示最近一次提交
$ git show &lt;tagName>  # 显示指定tag的信息

Lightweight Tags

$ git tag &lt;tagName>  # 不加-a，-m，-s，不添加额外的tag信息，一般临时使用

Tag later

$ git tag -a &lt;tagName> &lt;hashcode>  # hashcode如9fceb02
$ git tag -d &lt;tagName>  # 删除tag

Sharing Tags,explicitly push tags to a shared server

$ git push &lt;remote> &lt;tagname>
$ git push &lt;remote> --tags  # 一次推送所有tag

远程删除tag的2种方法

$ git push &lt;remote> :refs/tags/&lt;tagname>:  # `:refs/tags/&lt;tagname>:` 是固定搭配
$ git push origin --delete &lt;tagname>

Checking out Tags： view the versions of files a tag is pointing to

$ git checkout &lt;tagname>

> 会进入detached HEAD 状态，if you make changes and then create a commit, the tag will stay the same,
but your new commit won’t belong to any branch and will be unreachable, except by the exact
commit hash. Thus, if you need to make changes — say you’re fixing a bug on an older version, for
instance — you will generally want to create a branch:

$ git checkout -b &lt;branch> &lt;tagname>  # -b创建新分支，并使用checkout转到此分支


Git Aliases(Pg.60/66)

$ git config --global alias.co checkout
$ git config --global alias.br branch
$ git config --global alias.ci commit
$ git config --global alias.st status
$ git config --global alias.unstage 'reset HEAD --'
$ git config --global alias.last 'log -1 HEAD'

### Git Branching

$ git branch &lt;branch>  # create new branch

$ git checkout &lt;branch>  # Switching Branches

$ git checkout -b &lt;new-branch>  # create new branch and switch to it

> a branch in Git is actually a simple file that contains the 40 character SHA-1 checksum of
the commit it points to, branches are cheap to create and destroy. Creating a new branch is as quick
and simple as writing 41 bytes to a file (40 characters and a newline).


Basic Branching and Merging

$ git merge &lt;branch>  # Git simply moves the pointer forward to the branch(when master is not modified)
$ git branch -d &lt;branch>  # after merge, delete the temporaty branch
$ git branch -D &lt;branch>  # force delete

Basic Merging

> three-way merge：(when master branch and issue are both modified)Git creates a new snapshot that results from the two snapshots pointed to by the branch tips(指2个分支当前指向的节点) and the common ancestor of the two(指开始分叉的节点). merge and automatically creates a new commit that points to it

$ git checkout master  # 切换到主干，分支被合并到主干
$ git merge iss53

If you changed the same part of the same file
differently in the two branches you’re merging, Git won’t be able to merge them cleanly.


$ git mergetool  # use a graphical tool to resolve these conflicts

$ git branch --merged  # just leave the stared branch and delete others
$ git branch --no-merged  # can't deleteany branch cause they are not fully merged

Long-Running Branches(development process)

- master branch: entirely stable — possibly only code that has been or will be released.
- develop/next branch: a parallel branch that they work from or use to test stability — it isn’t necessarily always stable, but whenever it gets to a stable state, it can be merged into master.
- topic branches: short-lived branches, like iss53 branch, when they’re ready, to make sure they pass all the tests and don’t introduce bugs.Then it can be pulled into develop branch

In reality, we’re talking about pointers moving up the line of commits you’re making.the line is with pointer pointing to different stability.

$ git checkout master
$ git merge 9be07e4  # merge hash/tag of development branch moves master node to the hash


Remote Branches

git ls-remote &lt;remote> || git remote show &lt;remote>  # get a full list of remote references

远程跟踪分支：形式为<remote>/<branch>,例如远程仓库名为rem，使用git checkout rem/master来跳转至远程仓库的分支.


exp: remote branch process

$ git clone https://github.com/martinhunter/books.git/ -o longLocalName2

$ cd books

$ git remote rename longLocalName2 local2

$ git ls-remote local2  # 显示远程分支

$ git add localFile.txt

$ git commit -m 'update local'

$ git fetch local2

此时节点为A，对master修改，且远程也有修改，fetch更新数据，此时从A分叉出master和local2/master

$ git checkout local2/master  # 在local2/master会进入detached HEAD 状态，除非在此之上创建新分支，否则任何修改都无法被保存

$ git remote add local3 https://github.com/martinhunter2/books.git/  # when having multiple remote servers,assume you have another internal Git server that is used only for development by one of your sprint teams. This server is at github.com/martinhunter2/books.git/.添加多个服务器

$ git fetch local3  # local3指向local2/master分支

$ git checkout -b serverfix

$ git add hotfixfile.txt

$ git commit -m 'server fixed'

$ git config --global credential.helper cache.  # store passwords for HTTPS URL

$ git push local2 serverfix  # Git automatically expands the serverfix branchname out to `refs/heads/serverfix:refs/heads/serverfix`, which means, “Take my serverfix local branch and push it to update the remote’s serverfix branch.”

$ git push origin serverfix:serverfix  # it says, “Take my serverfix and make it the remote’s serverfix.”. Use this to push a local branch into a remote branch that is named differently.

$ git branch -d serverfix  # 删除本地以准备合并

$ git fetch local2  # fetch all the changes on the server that you don’t have yet, it will not modify your working directory at all. It will simply get the data for you and let you merge it yourself.

$ git merge local2/serverfix  # 将远程serverfix合并到当前本地分支

$ git checkout -b serverfix origin/serverfix  # start tracking remote branch(like the origin/master branch)


### Pushing

use new private branches for work you don’t want to share(not push), and push up only the new topic branches you want to collaborate on.

Tracking Branches：local branches that have a direct relationship to a remote branch

$ git checkout --track local2/serverfix  # 等同于git checkout -b serverfix origin/serverfix,以远程分支为基础新建分支.

$ git pull  # on a tracking branch,it knows which server to fetch from and which branch to merge in.

$ git branch -u local8/serverfix  # 修改当前分支所追踪的分支为local8/serverfix

$ git branch -vv  # 查看当前track状态

/* ahead means 3 commits locally are not pushed to the server*/

* master    51b2e08 [bks/master: ahead 3, behind 1] fixed
  newfix    a065b98 [bks/serverfix: ahead 1] new fix
  serverfix 51b2e08 fixed

$ git fetch --all; git branch -vv  # If you want totally up to date ahead and behind numbers, you’ll need to fetch from all your remotes

### Pulling

Deleting Remote Branches

$ git push local2 --delete serverfix  # 通常不用，it removes the pointer from the server. The Git server will generally keep the data there for a while until a garbage collection runs, so if it was accidentally deleted, it’s often easy to recover.



	exp: remote branch process
	
	$ git clone https://github.com/martinhunter/books.git/ -o longLocalName2

	此时默认节点为A

	$ cd books
	
	$ git remote rename longLocalName2 local2
	
	$ git ls-remote local2  # 显示远程分支情况
	
	$ git add localFile.txt
	
	$ git commit -m 'update local'
	
	// 对本地master修改，从A分出节点B

	// 在server的master上新建文件remote-modify.txt并commit，从A分出节点B-remote
	
	$ git fetch local2
	
	// 更新本地数据，此时A有2个分支B和B-remote
	
	$ git checkout local2/master  # 切换到B-remote节点，在local2/master会进入detached HEAD 状态，除非在此之上创建新分支，否则任何修改都无法被保存
	
	$ git remote add local3 https://github.com/martinhunter2/books.git/  # when having multiple remote servers,assume you have another internal Git server that is used only for development by one of your sprint teams. This server is at github.com/martinhunter2/books.git/.添加多个服务器
	
	$ git fetch local3  # local3指向local2/master分支
	
	// 切换到bk/master，并修改，使用switch，在bk/master的head处创建分支而非本地
	git checkout bk/master;
	notepad local-fix-1;
	git add local-fix-1;
	git commit -m local-fix-1;
	git switch -c local-fix-1;
	git push bk local-fix-1;

	NOTE: $ git checkout -b local2/serverfix,创建新分支只会在本地创建，在本地的head处分支，创建了名为local2/serverfix的分支，而非在local2作用域下名为serverfix的分支

	$ git checkout -b serverfix
	
	$ git add hotfixfile.txt
	
	$ git commit -m 'server fixed'
	
	$ git config --global credential.helper cache.  # store passwords for HTTPS URL
	
	$ git push local2 serverfix  # Git automatically expands the serverfix branchname out to `refs/heads/serverfix:refs/heads/serverfix`, which means, “Take my serverfix local branch and push it to update the remote’s serverfix branch.”
	
	$ git push origin serverfix:serverfix  # it says, “Take my serverfix and make it the remote’s serverfix.”. Use this to push a local branch into a remote branch that is named differently.
	
	$ git branch -d serverfix  # 删除本地以准备合并
	
	$ git fetch local2  # fetch all the changes on the server that you don’t have yet, it will not modify your working directory at all. It will simply get the data for you and let you merge it yourself.
	
	$ git merge local2/serverfix  # 将远程serverfix合并到当前本地分支
	
	$ git checkout -b serverfix origin/serverfix  # start tracking remote branch(like the origin/master branch)
	
	
	Pushing
	
	use new private branches for work you don’t want to share(not push), and push up only the new topic branches you want to collaborate on.
	
	Tracking Branches：local branches that have a direct relationship to a remote branch
	
	$ git checkout --track local2/serverfix  # 等同于git checkout -b serverfix origin/serverfix.
	
	$ git pull  # on a tracking branch,it knows which server to fetch from and which branch to merge in.
	
	$ git branch -u local2/serverfix  # 修改当前分支所追踪的分支
	
	$ git branch -vv  # 查看当前track状态
	
	/* ahead means 3 commits locally are not pushed to the server*/
	
	* master    51b2e08 [bks/master: ahead 3, behind 1] fixed
	  newfix    a065b98 [bks/serverfix: ahead 1] new fix
	  serverfix 51b2e08 fixed
	
	$ git fetch --all; git branch -vv  # If you want totally up to date ahead and behind numbers, you’ll need to fetch from all your remotes
	
	Pulling
	
	Deleting Remote Branches
	
	$ git push local2 --delete serverfix  # 通常不用，it removes the pointer from the server. The Git server will generally keep the data there for a while until a garbage collection runs, so if it was accidentally deleted, it’s often easy to recover.





### Rebasing

> You may want to use rebase -i to squash your work down to a single commit

> works by going to the common ancestor of the two branches (the one you’re on and the one you’re rebasing onto), getting the diff introduced by each commit of the branch you’re on, saving those diffs to temporary files, resetting the current branch to the same commit as the branch you are rebasing onto, and finally applying each change in turn.

$ git checkout exp-branch
$ git rebase master  

$ git rebase --onto master server client
// This basically says, “Take the **client** branch, figure out the patches since it diverged from the **server**
branch, and replay these patches in the client branch as if it was based directly off the **master** branch instead.” It’s a bit complex, but the result is pretty cool

the mechanism of rebasing:

1. if exp-branch is deleted,then the nodes C3-C5(which relies on exp-branch) will also be deleted
1. now try to merge master and C3 and create a new commit C3',
1. merge C3' and C4 to C4',till all nodes are merged
1. the end node is C5' here, and exp-branch points to C5'.

$ git checkout master
$ git merge exp-branch  # master moves forward to the end C5' and now points to the same node as exp-branch.


$ git rebase &lt;basebranch> &lt;topicbranch>  # rebase the server branch onto the master branch.It's short-hand for $ git checkout &lt;topicbranch>; $ git rebase &lt;basebranch>

The Perils of Rebasing:`Do not rebase commits that exist outside your repository and that people may have based
work on.`

When you rebase stuff, you’re abandoning existing commits and creating new ones that are similar
but different. If you push commits somewhere and others pull them down and base work on them,
and then you rewrite those commits with git rebase and push them up again, your collaborators
will have to re-merge their work and things will get messy when you try to pull their work back
into yours.

$ git pull --rebase  # instead of a normal git pull,so git will automatically rebase master to local2/master

Rebase vs. Merge

In general the way to get the best of both worlds is to rebase local changes you’ve made but haven’t
shared yet before you push them in order to clean up your story, but never rebase anything you’ve
pushed somewhere.

### Git on the Server

The Protocols:Local, HTTP, Secure Shell (SSH) and Git

Local protocol

> in which the remote repository is in another directory on the
same host.your team has access to a shared filesystem such as an NFS mount

$ git clone /srv/git/project.git
$ git clone file:///srv/git/project.git

HTTP

Smart HTTP and Dumb HTTP (Pg.104/110)

The SSH Protocol

$ git clone ssh://[user@]server/project.git


Create Repository

clone your repository to create a new bare repository, you run the
clone command with the --bare option.

$ git clone --bare my_project my_project.git  # 先回到git上一级目录，my_project为本地文件夹名称.`$ cp -Rf my_project/.git my_project.git` works roughly the same，只复制了.git中的内容

Putting the Bare Repository on a Server

$ scp -r &lt;git> &lt;userName>@&lt;site>:&lt;remote-directory>

now you’ve set up a server called git.example.com

$ scp -r my_project.git user@git.example.com:/srv/git

$ git clone user@git.example.com:/srv/git/my_project.git
$ ssh user@git.example.com
$ cd /srv/git/my_project.git
$ git init --bare --shared  # --shared adds group write permissions to a repository

Generating Your SSH Public Key(Pg.109/115)
$ cd ~/.ssh
$ ls  # The .pub file is your public key, and the other file is the corresponding private key.
authorized_keys2 id_dsa known_hosts
config id_dsa.pub

$ ssh-keygen -o  # create ssh-keyNow. Now,each user that does this has to send their public key to you or whoever is administrating the Git server (assuming you’re using an SSH server setup that requires public keys). All they have to
do is copy the contents of the .pub file and email it.

SSH On Server

$ sudo adduser git
$ su git
$ cd
$ mkdir .ssh && chmod 700 .ssh
$ touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
$ cat /tmp/id_rsa.john.pub >> ~/.ssh/authorized_keys  # store public keys in authorized_keys
$ cat /tmp/id_rsa.josie.pub >> ~/.ssh/authorized_keys
$ cat /tmp/id_rsa.jessica.pub >> ~/.ssh/authorized_keys

$ cd /srv/git
$ mkdir project.git
$ cd project.git
$ git init --bare
Initialized empty Git repository in /srv/git/project.git/

\# on John's computer
$ cd myproject
$ git init
$ git add .
$ git commit -m 'Initial commit'
$ git remote add origin git@gitserver:/srv/git/project.git
$ git push origin master

Restrict the git user account to only Git-related activities

$ cat /etc/shells # see if git-shell is already in there. If not...
$ which git-shell # make sure git-shell is installed on your system.
$ sudo -e /etc/shells # and add the path to git-shell from last command

$ sudo chsh git -s $(which git-shell)  # chsh &lt;username> -s &lt;shell>

Restrict users from being able to use SSH port forwarding to access any host the git server is able to reach

edit the authorized_keys file and prepend the
following options to each key you’d like to restrict:
`no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty`

## Integrationmanager workflow

1. The project maintainer pushes to their public repository.
2. A contributor clones that repository and makes changes.
3. The contributor pushes to their own public copy.
4. The contributor sends the maintainer an email asking them to pull changes.
5. The maintainer adds the contributor’s repository as a remote and merges locally.
6. The maintainer pushes merged changes to the main repository.

## Dictator and Lieutenants Workflow (for multiple-repository)

> one famous example is the Linux kernel

1. Regular developers work on their topic branch and rebase their work on top of master. The
master branch is that of the reference repository to which the dictator pushes.
2. Lieutenants merge the developers' topic branches into their master branch.
3. The dictator merges the lieutenants' master branches into the dictator’s master branch.
4. Finally, the dictator pushes that master branch to the reference repository so the other
developers can rebase on it.

### (Patterns for Managing Source Code Branche)[https://martinfowler.com/articles/branching-patterns.html]

#### Commit Guidelines

$ git diff --check ：检查出可能的空白符错误
$ git add --patch ：会先比较文件修改前后的不同之处，再询问是否stage.

2点比较法：issue54..origin/master

显式所有不在issue54上而在origin/master的commit，
且不包含origin/master中merge节点的commit.

$ git log --merges issue54..origin/master
- 即选出合并的节点，结果为{H,K,N}

$ git log --no-merges issue54..origin/master



- issue54在C,origin/master在L，commits如下
	- commits：{A-O}
- 从2个分支分叉开始(不包含分叉节点),所有origin/master的commit
	- commits：{D-O}
- 不包含合并的节点(master指向N,也不会包含).即使再分叉也不行
	- commits：{H,K,N}
- 包含分叉的节点
	- commits：{E,F}
- 包含普通的节点
	- commits：{DGIJLMO}
- --no-merges issue54..origin/master结果为
	- commits：{DEFG IJ LM O}



exp: 图示

```
                M-----N-O <- (master)
               /     /
            G-H-J-K-L 
           / /   / 
        D-E-F---I
       /
    A-B-C <- (issue54)
```

### Private Small Team

需要fetch上一个人的提交
fetch origin
checkout -b issue
do some commits
checkout master
merge issue
merge origin/master  # key,用本地master分支，将origin/master并入
push origin master

另一个人再次fetch此提交重复上述工作，确保每时每刻掌握他人的工作，可避免重复

### Forked Public Project

Pull request:Once your work has been pushed to your fork of the repository, you need to `notify the maintainers` of the original project that you have work you’d like them to merge

$ git request-pull &lt;start> &lt;url> &lt;end>
- start is branch/tag of origin
- url is the url of forked project
- end is the local:forked branch

$ git clone &lt;url>
$ cd project
$ git checkout -b featureA
... work ...
$ git commit
... work ...
$ git commit

... fork the original project to myfork ...

$ git remote add myfork &lt;url>

$ git push -u myfork featureA  # send local changes(featureA) to the fork

$ git request-pull origin/master myfork  # send request to 

push to the fork with a different name `&lt;local-branch>:&lt;forked-branch>`

$ git push myfork master:for-linus

$ git request-pull v1.0 myfork master:for-linus

Rebase that branch on top of origin/master, resolve the conflicts for the maintainer, and then resubmit your changes

$ git checkout featureA 
$ git rebase origin/master
$ git push -f myfork featureA  # replace the featureA branch on the server with a commit that isn’t a descendant of it.An alternative would be to push this new work to a different branch on the server (perhaps called featureAv2).


--Squash:
--squash produce the repository state as if a real merge happened,without actually making a merge
commit.

- `--squash` is cleaner than `--no-commit`
	- --squash creates a 'normal' commit after $ git commit,`not a merged joint`.
	- --no-commit creates a merged commit after $ git commit.

$ git checkout -b featureBv2 origin/master
$ git merge --squash featureB
... change implementation ...
$ git commit
$ git push myfork featureBv2



$ git format-patch -M origin/master  # 本地创建patch文件，方便发邮件

set up the imap section in your ~/.gitconfig file.
You can set each value separately with a series of git config commands, or you can add them manually, but in the end your config file should look something like this:

[imap]
folder = "[Gmail]/Drafts"
host = imaps://imap.gmail.com
user = user@gmail.com
pass = YX]8g76G_2^sFbd
port = 993
sslverify = false

### Maintaining a Project

namespace topic branches — such as sc/ruby_client, where sc is short for the person who contributed the work

Apply an emailed patch: 

- `$git apply`(apply all or abort all)
- `$git am`(apply a series of patches from a mailbox).

... save the patch in /tmp/patch-ruby-client.patch ...
$ git apply --check /tmp/patch-ruby-client.patch  # if check reports no error,then apply
$ git apply /tmp/patch-ruby-client.patch

$ git am -3 0001-see-if-this-helps-the-gem.patch  # -3 attempts to merge for public commit 
$ git am --resolved
-i : enter interactive mode

check out branch form contributer

$ git remote add jessica git://github.com/jessica/myproject.git
$ git fetch jessica
$ git checkout -b rubyclient jessica/ruby-client
... jessica adds new features ...
$ git pull https://github.com/onetimeguy/project  # for inconsistent contributers,don't save url

Compare Contribution-branch To Origin/master-branch And See Changes

$ git log contrib --not master  # --not excludes master commits,the same as `master...contrib`

A...B : diverge node of A and B is C,and show commits of C to B(C not included).


  $ git merge-base contrib master  # 先获得2个分支的分叉点的hash
  $ git diff <hash>  # 再比较当前分支与分叉节点.	

  $ git diff master...contrib  # shorthand for the command above

Rebasing and Cherry-Picking Workflows Insteadof Merge

cherrypick is like a rebase for a single commit,useful if you have a number of
commits on a topic branch and you want to integrate only one of them

$ git cherry-pick &lt;hash>  # pull commit e43a6 into your current branch

Rerere(reuse recorded resolution)

> it’s a smart way of shortcutting manual conflict resolution. When rerere is enabled, Git will keep a set of pre- and post-images from successful merges, and if it notices that there’s a conflict that looks exactly like one you’ve already fixed, it’ll just use the fix from last time, without bothering you with it.

$ git config --global rerere.enabled true

Use Key To Verify All Your Signed Tags.

$ git tag -s v1.5 -m 'my signed 1.5 tag'  # sign the tag as a maintainer

$ gpg --list-keys

$ gpg -a --export F721C45A | git hash-object -w --stdin

$ git tag -a maintainer-pgp-pub 659ef797d181633c87ec71ac3f9ba29fe5775b92

$ git describe master  # show annotated tag of current head

### Preparing a Release from latest snapshot

exp: for linux and for windows

```
$ git archive master --prefix='project/' | gzip > `git describe master`.tar.gz
$ ls *.tar.gz
$ git archive master --prefix='project/' --format=zip > `git describe master`.zip
$ ls *.zip
```

$ git shortlog  # summarizes all the commits,gives you a summary of all the commits since your last release

$ git shortlog --no-merges master --not v1.0.1  # shows diff between current version and v1.0.1

## GitHub

Two Factor Authentication(2FA) to protect account.

#### The GitHub Flow is centered on Pull Requests. 

> It is centered on the Topic Branches workflow

1. Fork the project
2. Create a topic branch from master.
3. Make some commits to improve the project.
4. Push this branch to your GitHub project.
5. Open a Pull Request on GitHub.
6. Discuss, and optionally continue committing.
7. The project owner merges or closes the Pull Request.
8. Sync the updated master back to your fork.

This is basically the Integration Manager workflow covered in Integration-Manager Workflow

exp: update forked branch

$ git remote add origin https://github.com/myForkedProgit/progit2.git
$ git remote add progit https://github.com/initialProgit/progit2.git
$ git branch --set-upstream-to=progit/master master
$ git config --local remote.pushDefault origin

$ git checkout master  # now it will automatically find the corresponding url
$ git pull
$ git push

### Pull Request `Ref`s

show us what
$ git ls-remote &lt;remote>  # references are present on the server

>>>
bddf460a677091bb39a9b7568538b515661e23a0        HEAD
237999457c2d8ac4b20ee965036055b1fb579c69        refs/heads/fix3
3599582fb6895c1c866c5b93834f3142dd0316c2        refs/heads/local-fix-1
2194d6f618cd62522e8c1bdabdd18a7de950cca7        refs/heads/local-hotfix-2
bddf460a677091bb39a9b7568538b515661e23a0        refs/heads/master
a065b9870b9fa874a82f5e488dbd1318cc852c24        refs/heads/newfix
51b2e08ee2e9fc340c3e17ab69fba89bc3aaaedf        refs/pull/1/head
23464a258543c160cf61c6c52e6d285760b5f9a0        refs/pull/2/head
237999457c2d8ac4b20ee965036055b1fb579c69        refs/pull/3/head
3599582fb6895c1c866c5b93834f3142dd0316c2        refs/pull/4/head
f042e38d4f4964d4a6412925e57c10bf5e61f588        refs/pull/4/merge
2194d6f618cd62522e8c1bdabdd18a7de950cca7        refs/pull/5/head
58a53cb7d4b69f3b8d4a0f6fe9a944ec93aba82c        refs/pull/5/merge

ref/pull/ is pseudo branch
- open pull request have 2 references
- closed pull request have 1 references
You only get branches under refs/heads/ when you clone or fetch from the server

$ git fetch origin refs/pull/4/head  # will directly download pull request branch for you.

```
[remote "origin"]  # origin is local name for remote url
    url = https://github.com/libgit2/libgit2
    fetch = +refs/heads/*:refs/remotes/origin/*
    fetch = +refs/pull/*/head:refs/remotes/origin/pr/*  # add this line in .git/config to download all pull requests.for example,refs/pull/12/head will be stored as refs/remotes/origin/pr/12, the content in the * are equal
    $ git checkout pr/2 
```


“reflog” — a log of where your HEAD and branch references have been for the last few months(not for too long).

$ git reflog
$ git show HEAD@{5}
$ git show master@{yesterday}

`^`(caret) at the end of a reference, Git resolves it to mean the parent of that commit.
`~`(tilde) is direct parent of current branch.

主分支merge副分支
^ and ~ are equal，they are shorthand for ^1,~1,即主分支
^n 选择第n个分支上的parent
~n 选择主分支的parent

$ git show "HEAD^"
$ git show "HEAD^3"  # ^n是一个整体,HEAD本身为merge的节点，则有多个parent，`^n`选择第n个分支上的parent

exp:
HEAD^^3^^^2
== HEAD^1^3^1^1^2
== HEAD~^3~~^2

means parent,3rdBranchParent,parent,parent,2ndBranchParent

#### double dot systax ..

$ git log refA..refB  # include refB and excludes refA
== $ git log ^refA refB
== $ git log refB --not refA

#### Triple Dot
$ git log --left-right refA..refB  # excludes intersection of refA and refB,--left-right shows which commit is in

#### interactive

git add -i

#### Stashing Your Work(临时保存)

Now you want to switch branches, but you don’t want to commit what you’ve been working on yet, so you’ll stash the changes.

$ git stash  # each git stash creates a stash,saved as stash@{n}
$ git stash list  # show stashes
$ git checkout issue32
... do some work and commit ...
$ git checkout master
$ git stash apply stash@{2} # revert specific change
$ git stash apply  # revert the last stash but not stage
$ git stash apply --index  # revert the last stash and stage
$ git stash drop stash@{0}  # remove specific stash

$ git stash --keep-index  # store stage info in status
$ git status -s

$ git stash --include-untracked or -u  # include untracked files in the stash being created

$ git stash --patch  # prompt you interactively which of the changes you would like to stash and which you would like to keep in your working directory.

$ git stash branch &lt;new branchname>  # creates a new branch for you with your selected branch name, checks out the commit you were on when you stashed your work, reapplies your work there, and then drops the stash if it applies successfully

$ git clean -n -d  # use -n instead of -f to see what will be removed all the untracked files in your working directory first
$ git clean -f -d  # removes any files and also any subdirectories that become empty as a result
$ git stash --all  # remove everything but save it in a stash

### GPG(sign your work)

$ gpg --gen-key;
$ gpg --list-keys
$ git config --global user.signingkey 5CECE40B479E0F8625C35A2ED02FF22E3657BF8D  # 5CECE40B479E0F8625C35A2ED02FF22E3657BF8D is hash of public key

$ git tag -s v1.5 -m 'my signed 1.5 tag'  # will require passphrase
$ git tag -v &lt;tag-name>  # verify a signed tags

$ git commit -a -S -m 'Signed commit'  # sign commits
$ git log --show-signature -1  # verify signed commit

$ git merge --verify-signatures non-verified-branch  # verify branch that is to be merged
fatal: Commit ab06180 does not have a GPG signature
$ git merge --verify-signatures -S signed-branch  # use -S to sign merged branch

### Searching

$ git grep &lt;keyword> &lt;regex-file> # shows files containing keyword,file is like `*.c` to filter specified fileType
-n or --line-number 
-c or --count  # counts
-p or --show-function  # display the enclosing method or function for each matching string

$ git grep --break --heading -n -e '#define' --and \( -e LINK -e BUF_MAX \) v1.8.0  # --and ensures that multiple matches must occur in the same line of text. here #define and (LINK or BUF_MAX) appear in oneline

Git Log Searching

$ git log -S ZLIB_BUF_MAX --oneline
-G  # regex search
$ git log -L :&lt;keyword>:&lt;file>  # list every change of keyword till creation of file
$ git log -L '/unsigned long git_deflate_bound/',/^}/:&lt;file>  # regex search

Modify History

NOTE: Don’t push your work until you’re happy with it

$ git commit --amend   # just a small rebase,don't amend if you pushed last commit,amend usually for small changes and use --no-edit

$ git rebase -i HEAD~3  # same as HEAD~3..HEAD
opens editor and modify/delete commit message(change pick to edit,squash) with reversed order.after save git rewinds with your new commit message



$ git reset HEAD^
$ git add README
$ git commit -m 'Update README formatting'
$ git add lib/simplegit.rb
$ git commit -m 'Add blame'
$ git rebase --continue

The Nuclear Option: filter-branch

not recommended,use [git-filter-repo](https://github.com/newren/git-filter-repo) instead


MARK Pg.251

Tree | Role
- | - |
HEAD | Last commit snapshot, next parent
Index | Proposed next commit snapshot
Working | Directory Sandbox

$ git cat-file -p HEAD  # see what that snapshot looks like
$ git ls-tree -r HEAD

Index is your proposed next commit(staging area).
$ git ls-files -s  # -s for status

### The Role of Reset

$ git reset <hash>  # git reset HEAD~~~ works as well

Reset process:

1. Move HEAD (--soft),HEAD still points to master,but `reset` makes master points to the commit. changes still staged
2. Updating the Index (--mixed,default option for reset HEAD).update the index with the contents of whatever snapshot HEAD now points to. changes unstaged.
3. Updating the Working Directory (--hard).totally discards all changes as if it never happened

$ git reset file/path  # opposite of git add

squash commits
$ git reset --soft <hash>
$ git commit -m "squashed"

reset Vs checkout

$ git reset <hash> <file>  # 不移动HEAD，不能加--soft,--mixed,--hard，恢复到未commit前的状态. WD safe

$ git checkout <hash>  # !!! 回到特定历史事件查看当时的文件(会进入detached-HEAD状态)


$ git checkout <hash> <file>  # 不移动HEAD，恢复到文件未修改，未stage的状态，可通过git restore恢复修改.reset --hard则完全不可恢复，not WD safe



without path
- checkout is safe 
- reset --hard moves branch that HEAD points to while checkout just moves HEAD to another branch.WD Safe 

### advanced merging

提交时转换为LF，检出时转换为
$ git config --global core.autocrlf true

$ git merge anotherBranch # 尝试merge,分支内whitespace有修改
... 冲突警告，分支显示为(master|merging) ...
$ git merge --abort  # 跳出merge，分支显示为(master)

$ git -Xignore-all-space  # ignores whitespace completely when comparing lines
$ git -Xignore-space-change  # treats sequences of one or more whitespace characters as equivalent.

manual re-merging

$ git merge another  # to enter merge conflict state first

- stage 1 is the common ancestor
- stage 2 is your version(current branch)
- stage 3 is from the MERGE_HEAD, the version you’re merging in
- .common,.ours,.theirs是固定的，不可更改

$ git show :1:hello.py > hello.common.py  # use `>` to make copies
$ git show :2:hello.py > hello.ours.py  # `:2:hello.py` is shorthand for looking up its SHA
$ git show :3:hello.py > hello.theirs.py

$ git ls-files -u  # list hashes of unmerged files

...modify hello.theirs.py manually...
$ git merge-file -p \


$ git diff --ours  # in conflict state,compare your result to what you had in your branch before the merge, in other words, to see what the merge introduced.Don't have to open the file with your editor
$ git diff --theirs
$ git diff --base -b  # see changes from both sides

$ git clean -f  # clear temp files
Removing hello.common.rb
Removing hello.ours.rb
Removing hello.theirs.rb

$ git log --graph --oneline --decorate --all  # show all commits(including all branches and stashes)

use checkout without merging

$ git checkout --conflict=diff3 hello.py  # shows diff, --conflict=merge is default

$ git config --global merge.conflictstyle diff3

$ git log --oneline --left-right HEAD...MERGE_HEAD  # show unique commits of each branch

$ git log --oneline --left-right --merge  # show conflict commits

$ git diff  # see what you still have to resolve

$ git log --cc -p -1  # see how something was resolved after the fact.

Undoing Merges

$ git reset --hard HEAD~

$ git revert -m 1 HEAD  # -m 1 flag indicates which parent is the “mainline” and should be kept.like `reset ^HEAD` but doesn't delete merge joint.It actually creates a new commit that is copy of master before merge(^HEAD here) and discards all changes from another branch.

now nothing in topic is reachable from master. if you make changes in topic and try to merge in, git will only merge these changes since revert. Use the commands below to bring back all changes from topic 

$ git revert ^M  # un-revert the original merge

Pg.287

MARK Pg.251

Tree | Role
- | - |
HEAD | Last commit snapshot, next parent
Index | Proposed next commit snapshot
Working | Directory Sandbox

$ git cat-file -p HEAD  # see what that snapshot looks like
$ git ls-tree -r HEAD

Index is your proposed next commit(staging area).
$ git ls-files -s  # -s for status

### The Role of Reset

$ git reset <hash>  # git reset HEAD~~~ works as well

Reset process:

1. Move HEAD (--soft),HEAD still points to master,but `reset` makes master points to the commit. changes still staged
2. Updating the Index (--mixed,default option for reset HEAD).update the index with the contents of whatever snapshot HEAD now points to. changes unstaged.
3. Updating the Working Directory (--hard).totally discards all changes as if it never happened

$ git reset file/path  # opposite of git add

squash commits
$ git reset --soft <hash>
$ git commit -m "squashed"

reset Vs checkout

$ git reset <hash> <file>  # 不移动HEAD，不能加--soft,--mixed,--hard，恢复到未commit前的状态. WD safe

$ git checkout <hash>  # !!! 回到特定历史事件查看当时的文件(会进入detached-HEAD状态)


$ git checkout <hash> <file>  # 不移动HEAD，恢复到文件未修改，未stage的状态，可通过git restore恢复修改.reset --hard则完全不可恢复，not WD safe



without path
- checkout is safe 
- reset --hard moves branch that HEAD points to while checkout just moves HEAD to another branch.WD Safe 

### advanced merging

提交时转换为LF，检出时转换为
$ git config --global core.autocrlf true

$ git merge anotherBranch # 尝试merge,分支内whitespace有修改
... 冲突警告，分支显示为(master|merging) ...
$ git merge --abort  # 跳出merge，分支显示为(master)

$ git -Xignore-all-space  # ignores whitespace completely when comparing lines
$ git -Xignore-space-change  # treats sequences of one or more whitespace characters as equivalent.

manual re-merging

$ git merge another  # to enter merge conflict state first

- stage 1 is the common ancestor
- stage 2 is your version(current branch)
- stage 3 is from the MERGE_HEAD, the version you’re merging in
- .common,.ours,.theirs是固定的，不可更改

$ git show :1:hello.py > hello.common.py  # use `>` to make copies
$ git show :2:hello.py > hello.ours.py  # `:2:hello.py` is shorthand for looking up its SHA
$ git show :3:hello.py > hello.theirs.py

$ git ls-files -u  # list hashes of unmerged files

...modify hello.theirs.py manually...
$ git merge-file -p \


$ git diff --ours  # in conflict state,compare your result to what you had in your branch before the merge, in other words, to see what the merge introduced.Don't have to open the file with your editor
$ git diff --theirs
$ git diff --base -b  # see changes from both sides

$ git clean -f  # clear temp files
Removing hello.common.rb
Removing hello.ours.rb
Removing hello.theirs.rb

$ git log --graph --oneline --decorate --all  # show all commits(including all branches and stashes)

use checkout without merging

$ git checkout --conflict=diff3 hello.py  # shows diff, --conflict=merge is default

$ git config --global merge.conflictstyle diff3

$ git log --oneline --left-right HEAD...MERGE_HEAD  # show unique commits of each branch

$ git log --oneline --left-right --merge  # show conflict commits

$ git diff  # see what you still have to resolve

$ git log --cc -p -1  # see how something was resolved after the fact.

Undoing Merges

$ git reset --hard HEAD~

$ git revert -m 1 HEAD  # -m 1 flag indicates which parent is the “mainline” and should be kept.like `reset ^HEAD` but doesn't delete merge joint.It actually creates a new commit that is copy of master before merge(^HEAD here) and discards all changes from another branch.

now nothing in topic is reachable from master. if you make changes in topic and try to merge in, git will only merge these changes since revert. Use the commands below to bring back all changes from topic 

$ git revert ^M  # un-revert the original merge

Pg.287



MARK














## Git Internals(mechanism)



Git is fundamentally a content-addressable filesystem with a VCS user interface written on top of it.

When you make a commit, Git stores a commit object that contains a pointer to the **snapshot** of the
content you staged


所有不被指向的节点会被清除(rebase，branch -d),因此要谨慎处理

$ git diff master: Git directly compares the snapshots of the last commit of the topic branch you’re on and the snapshot of the last commit on the master branch. So if your master branch has moved forward
since you created the topic branch from it, then you’ll get seemingly strange results.




