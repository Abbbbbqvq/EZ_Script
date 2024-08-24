# EZ_Script

配合绿盟ez漏扫的打点脚本，自动化扫描页面中的接口，并探测可能存在的未授权接口、log4j、sql注入、rce等，可联动burp做进一步被扫。

## 声明

仅用于授权安全渗透测试，请勿用于非法攻击。

## 目录展示

![image-20240823200948585](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823200948585.png)

targets.txt存放的是url

sub_domains.txt存放的是domain，防止爬取到非本资产的其他url，所以需要做一个筛选

直接在在线网站中提取domain，然后分开放到对应文件即可

Config.yaml没配置过反连的往下滑，配置反连平台

## 工具下载

[Qianlitp/crawlergo: A powerful browser crawler for web vulnerability scanners (github.com)](https://github.com/Qianlitp/crawlergo)

[m-sec-org/EZ: EZ是一款集信息收集、端口扫描、服务暴破、URL爬虫、指纹识别、被动扫描为一体的跨平台漏洞扫描器。 (github.com)](https://github.com/m-sec-org/EZ)

https://github.com/winezer0/passive-scan-client-plus

[Abbbbbqvq/Enscan_Script: 快速筛选Enscan输出结果中的domain，让你在红蓝攻防中快人一步 (github.com)](https://github.com/Abbbbbqvq/Enscan_Script)

## 如何使用

如果没搭建好ez扫描器直接往下滑，环境搭建

首先运行服务端和客户端

```
./ez_linux_amd64 reverse  #服务端
./ez webscan  #客户端
```

Ez启动后默认监听2222端口，如果改过监听端口，需要到脚本里设置对应端口

![image-20240823195843756](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823195843756.png)

接着开启靶机[Vulfocus log4j2-rce靶机 | NSSCTF](https://www.nssctf.cn/problem/1125)

![image-20240823200007790](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823200007790.png)

将url复制到target.txt文件中，将domain提取出来放到sub_domains.txt中，保存

![image-20240823200140413](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823200140413.png)

然后运行脚本即可，稍待片刻，就能扫出漏洞了，当然理想情况是这样的，此脚本还有完善的空间，现只是一个demo版，可以的话大家可以多提供提供思路

![image-20240823202228294](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823202228294.png)

## burp联动ez

脚本默认代理端口为2222端口

![image-20240824114741851](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240824114741851.png)

可将端口修改为8080，转发到Burp上，然后burp通过插件passive-scan-client转发到ez上(原版或者是plus版都可以，只要能用)

![image-20240824115017696](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240824115017696.png)

![image-20240824115129857](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240824115129857.png)



## 环境搭建

该工具扫描log4j等漏洞需要使用到服务器，没有的话就只能扫描一些单一的漏洞了。

首先到EZ项目下下载对应的扫描器

[m-sec-org/EZ: EZ是一款集信息收集、端口扫描、服务暴破、URL爬虫、指纹识别、被动扫描为一体的跨平台漏洞扫描器。 (github.com)](https://github.com/m-sec-org/EZ)

然后到[M-SEC社区 (nsfocus.com)](https://msec.nsfocus.com/)去注册申请一个使用许可证书文件

![image-20240823191920769](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823191920769.png)

将证书文件和ez扫描器拷贝到当前目录下之后

![image-20240823192137597](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823192137597.png)

输入命令，如果当前目录没有config.yaml文件，会自动生成config.yaml文件，然后开启本地2222端口监听，到这一步，ez扫描器就能正常使用了。

```
./ez webscan
```

![image-20240823192435078](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823192435078.png)

接下载是反连平台搭建[反连平台搭建（外网篇） | EZ (ezreal.cool)](https://docs.ezreal.cool/docs/EZUSE/ez-reverse)

首先在ez项目下下载你服务器能使用的版本到你服务器上

然后操作也差不多，输入命令，然后目录下生成config.yaml文件

```
./ez_linux_amd64 webscan
```

接下来，就是配置服务器端的ez的config.yaml，ip必须为0.0.0.0，端口随意，token自己最好是设置的复杂一些，长一些，disable要设置为false

![image-20240823193625197](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823193625197.png)

设置好这些之后，回到客户端，也就是你自己的电脑，设置你本地的config.yaml，也跟服务器端的差不多，就是ip得设置为你服务器的ip，然后disable得设置为false，token要跟服务器端的一样

![image-20240823193907620](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823193907620.png)

设置好这些之后，服务器端运行命令，客户端运行命令

```
./ez_linux_amd64 reverse  #服务器端运行
./ez --check-reverse webscan  #客户端运行
```

客户端回显，配置的rmi和ldap正常执行

![image-20240823194529579](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823194529579.png)

服务端回显payload

![image-20240823195040550](https://github.com/Abbbbbqvq/EZ_Script/blob/main/images/image-20240823195040550.png)

至此，ez扫描器搭建完成，更多的配置可以参考ez使用文档

最后就是下载爬虫工具，用于爬取url

[Qianlitp/crawlergo: A powerful browser crawler for web vulnerability scanners (github.com)](https://github.com/Qianlitp/crawlergo)

## 更新日志
1、 2024.8.23 创建EZ_Script项目

2、 2024.8.24 修复存在的一些问题

## 待更新内容
1、 目前的Burp联动ez只爬取get请求，后续增加post请求

2、增加爬取url缓存去重，防止不同网页爬取的url相同而导致重复发包

