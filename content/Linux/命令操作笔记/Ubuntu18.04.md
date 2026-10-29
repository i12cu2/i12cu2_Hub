## 一、基础与目录操作

| 命令                 | 作用                      |
| -------------------- | ------------------------- |
| `pwd`                | 查看当前路径              |
| `cd Desktop`         | 切换到桌面                |
| `cd ./A`             | 进入当前路径下的 A 文件夹 |
| `cd ..`              | 返回上一级                |
| `cd ../..`           | 返回上两级                |
| `cd -`               | 回到上一次操作路径        |
| `cd` 或 `cd ~`       | 进入当前用户家目录        |
| `clear`              | 清屏                      |
| `touch 1.txt`        | 创建空文件                |
| `mkdir 1`            | 创建文件夹                |
| `mkdir -p A/B/C/D/E` | 递归创建多级目录          |
| `tree`               | 显示目录树                |
| `history`            | 查看历史命令              |
| `!2074`              | 执行历史命令中第 2074 条  |
| `Tab`                | 自动补全文件名/命令       |
| `Ctrl + C`           | 清除当前命令              |

## 二、查看文件与帮助

- `ls`：列出目录内容  
- `ls -a`：显示全部文件，包括隐藏文件  
- `ls -l`：显示文件详细信息  
- `ls -lh`：显示详细信息，并以易读单位显示大小  
- `ls -alh`：等价于 `ls -a -l -h`，可合并选项  
- `ll`：相当于 `ls -la`  
- `command --help`：查看命令帮助  
- `man ls`：查看手册  
  - 退出：`q`  
  - 翻屏：文档记 `f` 翻屏、`d` 上翻屏  
- man 手册章节：  
  1. 标准命令  
  2. 系统调用  
  3. 库函数  
  4. 设备文件  
  5. 文件格式  
  6. 游戏娱乐  
  7. 杂项  
  8. 管理员命令  

## 三、文件查看、编辑、重定向与管道

- `cat 1.txt`：查看文件内容  
- `gedit 1.txt`：图形化编辑文件  
- `vim`：终端编辑器，文档中作者选择使用 vim  
- `more 1.txt`：分页查看  
  - 文档记：`f` 翻页，`d` 上翻，`q` 退出  
- `>`：重定向，覆盖写入  
  - 例：`ls -alh > 1.txt`  
- `>>`：追加重定向  
  - 例：`ls -alh >> 1.txt`  
- `|`：管道  
  - 例：`ls -alh /bin | more`  
- `;`：多个命令依次执行  
  - 例：`ls; ls -alh`

## 四、文件与目录管理

- `rm 1.txt`：删除文件  
- `rm *.txt`：删除所有 txt 文件  
- `rm -r B`：删除文件夹 B  
- `rm -rf`：强制递归删除，危险命令，慎用  
- `*`：通配符，匹配任意字符  
  - 例：`ls 2*`  
- `?`：匹配单个字符  
- `[23]`：匹配指定字符之一  
  - 例：`ls 1[23]4.txt` 可匹配 `124.txt`、`134.txt`  
- `mv 1-softlink.txg 1-softlink.txt`：重命名  
- `mv 111.txt laowang/`：移动文件到目录  
- `mv laowang/ gebilaowang`：文件夹重命名  
- `cp 2.txt A`：复制文件到 A 文件夹  
- `cp -r A gebilaowang/`：递归复制文件夹  
- `cp` 常用选项：  
  - `-a`：保留链接、属性，递归复制  
  - `-f`：已存在目标文件时不提示  
  - `-i`：覆盖前提示确认  
  - `-r`：递归复制目录  
  - `-v`：显示拷贝进度  
- `ln -s 1.txt 1-softlink.txt`：创建软链接  
- `ln 1.txt 1-softlink.txt`：创建硬链接，相当于别名  
- `grep "ntfs" xxx.txt`：搜索文件内容  
  - `-v`：显示不包含匹配文本的行  
  - `-n`：显示匹配行及行号  
  - `-i`：忽略大小写  

## 五、查找文件

- 查找当前目录下名为 `test.sh` 的文件：  
  `find . -name "test.sh"`
- 查找当前目录下所有 `.sh` 文件：  
  `find . -name "*.sh"`
- 查找当前目录下所有以大写字母开头的文件：  
  `find . -name "[A-Z]*"`
- 查找 `/tmp` 下等于 2M 的文件：  
  `find /tmp -size 2M`
- 查找 `/tmp` 下大于 2M 的文件：  
  `find /tmp -size +2M`
- 查找 `/tmp` 下小于 2M 的文件：  
  `find /tmp -size -2M`
- 查找当前目录下大于 4k、小于 5M 的文件：  
  `find . -size +4k -size -5M`
- 查找当前目录下权限为 777 的文件或目录：  
  `find . -perm 777`
- 若在系统目录查找，可能需要 `sudo`，如：  
  `sudo find / -name "*name*"`

## 六、打包与压缩

- `tar -cvf test.tar *.py`：打包 py 文件  
- `tar -xvf test.tar`：解包  
- `tar -zcvf xxx.tar.gz *.py`：打包并 gzip 压缩  
- `tar -zxvf xxx.tar.gz`：解压 gzip 包  
- `tar -jcvf yyy.tar.bz2 *.py`：打包并 bzip2 压缩  
- `tar -jxvf yyy.tar.bz2`：解压 bzip2 包  
- `tar -zxvf text.tar.gz -C dongge/`：解压到指定目录，`-C` 指定路径  
- `zip zzz.zip *.py`：zip 压缩  
- `unzip zzz.zip`：解压 zip  
- `unzip -d ./text myzip.zip`：解压到指定目录，`-d` 指定路径  

tar 常用选项：  
- `-c`：创建打包文件  
- `-x`：解开档案文件  
- `-v`：显示详细过程  
- `-f`：指定档案文件名，必须放在选项最后  
- `-t`：列出档案中包含的文件  
- `-z`：gzip 压缩/解压  
- `-j`：bzip2 压缩/解压  

## 七、时间、日历与系统信息

- `cal`：显示日历  
- `cal -y 2008`：显示 2008 年日历  
- `date`：显示当前时间  
- `date > test.txt`：把时间写入文件  
- `date "+%Y === %m === %d"`：格式化显示年月日  
- 日期格式：  
  - `%Y`、`%y`：年  
  - `%m`：月  
  - `%d`：日  
  - `%H`：时  
  - `%M`：分  
  - `%S`：秒  
- 设置时间需要管理员权限：  
  `date [MMDDhhmm[[CC]YY][.ss]]`  
  例：`date 010203042016.55`
- `du -h`：显示每个路径文件夹占用大小  
- `which ls`：查看命令所在路径  
- `which ps`：查看 ps 命令路径  

## 八、进程管理

- `ps`：查看进程  
- `ps -aux`：查看全部进程详细信息  
- `ps` 常用选项：  
  - `-a`：显示终端上所有进程，包括其他用户  
  - `-u`：显示进程详细状态  
  - `-x`：显示没有控制终端的进程  
  - `-w`：显示加宽，显示更多信息  
  - `-r`：只显示正在运行的进程  
- `top`：按资源使用大小查看进程，`q` 退出  
- `htop`：更详细查看电脑运行情况  
- `kill PID`：结束指定进程，后面的数字是进程号  

## 九、网络相关

- `ifconfig`：查看当前电脑网络信息  
  - 常见网卡名：`ens33`、`ens38`、`lo`  
- `sudo ifconfig ens33 172.16.7.139`：修改 IP  
- `ping 172.16.7.1`：测试网络延迟  
- `ifconfig | grep 172`：查找 IP  
- `ssh python@172.16.7.139`：远程登录  
- 终端切换：`Alt + 1`、`Alt + 2` 切换不同终端  

## 十、用户与组管理

### 用户
- `useradd -m shuaige`：创建用户并创建家目录  
- `useradd shuaig`：只创建用户  
- `cat /etc/passwd`：查看用户信息，末尾可确认是否创建成功  
- `ls /home/`：查看是否存在用户家目录  
- `su shuaige`：切换到用户 shuaige  
- `sudo passwd shuaige`：设置密码  
- `whoami`：查看当前账户  
- `exit`：退出用户或终端  
- `who`：查看登录用户位置  
- `userdel shuaige`：删除账户，但家目录仍存在  
- `sudo userdel -r gebilaowang`：删除账户并删除家目录  
- `su - xxxx`：切换用户并加载其环境  
- `sudo -s`：切换到超级管理员 root，之后可不再加 `sudo`  
- `rm -rf /`：删库危险命令，绝对不要执行  

### 用户组
- `cat /etc/group`：查看所有用户的组  
- `groupadd YYY`：创建组  
- `groupdel YYY`：删除组  
- `groupmod`：修改组，按两次 Tab 可显示组名  
- `cat /etc/group | grep sudo`：查找 sudo 组信息  
- 给普通用户添加 sudo 权限：  
  - `sudo usermod -a -G adm 用户名`  
  - `sudo usermod -a -G sudo 用户名`  
- `usermod -g` 与 `-G` 区别：  
  - `-g`：指定用户默认用户组  
  - `-G`：向其他组添加，通常配合 `-a` 使用  

## 十一、权限管理

`ls -l` 输出示例含义：

```text
-rw-rw-r-- 1 python python 0 3月 30 14:37 1.py
```

- 开头 `-`：普通文件  
- 开头 `d`：文件夹  
- 权限三组：  
  - `u`：文件拥有者  
  - `g`：同组用户  
  - `o`：其他人  
- 权限字母：  
  - `r`：读，数字 4  
  - `w`：写，数字 2  
  - `x`：可执行，数字 1  

修改权限：

- 符号法：  
  - `chmod u=rwx 2.py`  
  - `chmod u=,g=,o= 2.py`  
  - 可用逗号分隔多项  
- 数字法：  
  - `chmod 137 2.py`  
  - 表示：`u=1` 即 `--x`，`g=3` 即 `-wx`，`o=7` 即 `rwx`  

修改所属组和所有者：

- `chgrp YYY 1.py`：修改文件所属组  
- `chown xxxx 1.py`：修改文件所有者  

## 十二、总结提醒

这份文档主要覆盖了 Ubuntu 18.04 的：

1. 基础命令与目录操作  
2. 文件查看、编辑、重定向、管道  
3. 文件复制、移动、删除、链接  
4. 查找、搜索、打包压缩  
5. 时间、进程、网络  
6. 用户、用户组、权限管理  

学习时重点记住：  
- `ls -alh`、`cd`、`pwd`、`mkdir -p`、`rm -rf`、`cp -r`、`mv`  
- `find`、`grep`、`tar`、`chmod`、`chown`、`chgrp`  
- `ps -aux`、`top`、`kill`  
- `useradd`、`userdel`、`usermod`、`passwd`、`su`、`sudo`  
- 权限数字法：`r=4、w=2、x=1`，`777` 为最高权限  