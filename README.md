## SchoolNet-AutoLogin

### 使用说明

1. clone 本仓库

2. 在`config.py`中填写`ACCOUNT`（账号）和`PASSWORD`（密码）
3. 在仓库根目录打开一个终端按照以下操作进行

````bash
>> # 安装依赖
>> # Install requirements
>> pip install -r requirements.txt

>> # 执行登录操作
>> # python login.py login -u <用户代理> -i <网卡:此网卡的第n个IP>
>> # 用户代理可以用来规避校园网的PC/移动设备检测，最多可以允许两个不同平台的设备在线(必需参数)
>> # 获取网卡和网卡的第n(一般为1)个IP可以用来向校园网后端提交本机IP，以便后端为本机IP开放网络(必需参数)
>> python login.py login -u <User-Agent> -i <Network Interface:n-st IP of this interface>

# eg.(示例)
>> python login.py login -u GooglePixel6 -i wlan0:1
# 示例注释: 如果你想要使用安卓移动设备用户代理，那么你在登录时-u参数应该填写GooglePixel6
# 示例注释: 如果你选择wlan0网卡的第一个IP，那么你在登录时-i参数应该填写wlan0:1


>> # 下面是获取必需参数的方法
>> # 获取可选的用户代理
>> # Get available User-Agent
>> python login.py list -u
# eg. output (示例输出)
# GooglePixel6
# iPhone13ProMax
# Windows10Edge
# MacOSXSafari
# LinuxFirefox

>> # 获取可用的网卡以及它的IP地址
>> # Get available Network Interface and IP(s) of this interface
>> python login.py list -i
# eg. output (示例输出)
# Interface:	 lo
# IP(s):		 127.0.0.1
#
# Interface:	 eno1
# IP(s):		 None
#
# Interface:	 wlan0
# IP(s):		 172.16.112.17
````
