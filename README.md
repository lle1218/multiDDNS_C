#multiDDNS_C

使用方法：

1. 配置ddns/update.py文件user config中的对应服务商的用户名、密码、申请的动态域名，
并将其enable值设置为True，启动ddns.py脚本就可进行更新。

2. 可以同时配置多个域名更新

3. 更新情况记录在与update.py同目录的update.log文件中，可以在system config中修改
logpath变量的值来指定更新日志文件存储路径

4. 默认域名更新间隔是60秒，出口ip地址探测时间间隔为3秒，可以在system config中修改
interval listen_timeout的值改变对应的时间间隔




