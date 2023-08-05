#pipini
###用法:
>pipini -c                   创建默认的pip.ini文件
pipini -l                   查看pip.ini文件的内容
pipini --index-url=xxx      设置index-url的值
pipini --timeout=xxx        设置timeout的值
pipini --trusted-host=xxx   设置trusted-host的值
###默认的pip.ini如下：
>[global]
index-url = https://pypi.douban.com/simple
trusted-host = https://pypi.douban.com
timeout = 60