# scfproxy

利用云函数多出口的特点，使用mitm配合云函数实现动态代理

使用方法：

腾讯云创建云函数，创建方式选择自定义创建，函数类型选择web函数，名称地域自定
提交方法选择本地自拍包，触发器选择新建api服务，将scf.zip上传并部署
部署成功后复制 触发管理 里面的访问路径，填写在mitm.py中
客户端安装mitmproxy
运行mitmdump -s mitm.py --ssl-insecure --listen-port 8082


不适合大量扫描，因为每月免费额度只有100万次

