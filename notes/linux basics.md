一般指令形式：操作名 输入流名称。如 head /etc/fileName

对\*，?必须使用单引号包裹，避免产生正则匹配（其他字符可用可不用）。如 find /etc/dict -name f'\*'le

变量符号：`$`

`$PATH` 设置路径:`PATH = newPath2:$PATH`

使用`&`操作符将进程设置为后台运行，这样提示符会一直显示，你在进程运行过程中可以继续其他操作

chmod命令更改文件权限。例如，对文件file，要为用户组g和其他用户o加上可读权限r，运行以下命令：
chmod go+r file
chmod go-r file  # 取消权限

符号链接:
ln -s target linkname  # 没有-s，ln命令会创建一个硬链接，为文件创建一个新的名字。新文件拥有老文件的所有状态信息，和符号链接一样，打开这个新文件会直接打开文件内容


gzip:压缩单个文件
tar：压缩归档多个文件


three modes of tar(not compatible)

- -c: create
- -x: decompress
- -t: show content but don't decompress

[optional
-z: 自动调用gzip产生.tar.gz文件(必须且写在最前）
-v: show detail
-p: preserve privilages info
-f: file(必有，且写在最后）

归档文件（.tar.gz)


设置解包的路径：

tar -zxvf archive_name.tar.gz -C /tmp/extract_here/

### [Linux目录结构](http://www.pathname.com/fhs/)

/bin:binary excutable files
/dev:device
/etc:etcetera,store system config files

### sudo

在/etc/sudoers文件中加入指定的用户

	User_Alias ADMINS = user1, user2
	ADMINS ALL = NOPASSWD: ALL
	root ALL=(ALL) ALL

第一行为user1和user2指定一个ADMINS别名，第二行赋予它们权限。ALL = NOPASSWD: ALL表示
有ADMINS别名的用户可以运行sudo命令。该行中第二个ALL代表允许执行任何命令，第一个ALL表示
允许在任何主机运行命令（如果你有多个主机，你可以针对某个主机或者某一组主机设置，这个我们在
这里不详细介绍）。
root ALL=(ALL) ALL表示root用户能够在任何主机上执行任何命令。(ALL)表示root用户可以以任何
用户的身份运行命令。你可以通过以下方式将(ALL)权限赋予有ADMINS别名的用户，将(ALL)加入
到/etc/sudoers行，如➊所示：

	ADMINS ALL = (ALL)➊ NOPASSWD: ALL

### 设备文件

	$ ls -l
	brw-rw---- 1 root disk 8, 1 Sep 6 08:37 sda1
	crw-rw-rw- 1 root root 1, 3 Sep 6 08:37 null
	prw-r--r-- 1 root root 0 Mar 3 19:17 fdata
	srw-rw-rw- 1 root root 0 Dec 18 07:43 log

请注意，上面每一行的第一个字符（代表文件模式）：字符b（block）、c（character）、p（pipe）和
s（socket）代表设备文件。下面是详细介绍。

### dd命令
> 对于块设备和字符设备非常有用，它的主要功能是从输入文件和输入流读取数据然后写入输出文
件和输出流，在此过程中可能涉及到编码转换。

	$ dd if=/dev/zero of=new_file bs=1024 count=1

- if=file：代表输入文件，默认是标准输入。
- of=file：代表输出文件，默认是标准输出。
- bs=size：代表数据块大小。dd命令一次读取或者写入数据的大小。对于海量数据，你可以在数字后设置b和k来分别代表512字节和1024字节。如：bs=1k和bs=1024一样。
- ibs=size，obs=size：代表输入和输出块大小。如果输入输出块大小相同，你可以使用bs选项，如果不相同的话，可以使用ibs和obs分别指定。
- count=num：代表复制块的总数。在处理大文件或者无限数据流（/dev/zero）的时候，你可能会需要在某个地方停止dd复制，不然的话将会消耗大量硬盘空间和CPU时间。这时你可以使用count和skip选项从大文件或设备中复制一小部分数据。
- skip=num：代表跳过前面的num个块，不将它们复制到输出。