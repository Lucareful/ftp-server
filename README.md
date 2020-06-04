# 基于python的ftp服务器

## 文件结构

```cmd
├─ftp_client
│      ftp_clients.py  客户端主程序
│      test.jpg			测试文件
│      __init__.py
│      
├─ftp_server
│  │  __init__.py
│  │  
│  ├─bin
│  │      servers.py	服务端主程序
│  │      __init__.py
│  │      
│  ├─conf
│  │  │  settings.py	配置文件
│  │  │  UserDataBase.cfg	用户数据文件
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          settings.cpython-36.pyc
│  │          __init__.cpython-36.pyc
│  │          
│  ├─core	核心代码
│  │  │  main.py	
│  │  │  server.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          main.cpython-36.pyc
│  │          server.cpython-36.pyc
│  │          __init__.cpython-36.pyc
│  │          
│  └─home	存放数据文件
│      └─luenci
│          ├─data
│          └─images
│                  test.jpg
│                  
└─logger	日志功能 待开发
        __init__.py
```

## 用户文件配置

```cmd
[DEFAULT]

[root]
password = admin

[luenci]
password = 123

```

## 项目启动

先启动服务器端：

```cmd
python servers.py start
```

![](https://raw.githubusercontent.com/Lucareful/ImgRepo/master/img/hexo_img/image-20200604171502074.png)

然后启动客户端：

```cmd
python ftp_clients.py  -s 127.0.0.1 -P 8001
```

![](https://raw.githubusercontent.com/Lucareful/ImgRepo/master/img/hexo_img/image-20200604171428770.png)

## 目前支持的命令

### 上传文件

- put 命令

```cmd
put filename images   # 上传文件  images
```

> 所以上传的文件默认路径都在 home目录下

### 展示目录

- ls命令

```cmd
ls # 默认打印home user 文件下的内容
```

### 切换目录

- cd 命令

```cmd
cd  XXX   # 默认路径在user路径下
```

### 创建目录

- mkdir

```cmd
mkdir XXX
mkdir XXX\XXX			# 支持多级创建   
```

>上文中所有的命令操作默认的路径是  用户路径下

