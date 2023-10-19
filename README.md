# Intelligent tree-Assistant

Selenium实现智慧树自动刷课刷题脚本。

## 功能

AotoCourse.py
- 自动判断是否观看完毕
- 自动静音
- 自动切换流畅画质
- 自动检测并关闭网课中弹题
- 自动 1.5 倍速播放
- 自动点击下一个视频，下一门课程

AutoTest.py
- 自动获取题目选项
- 自动询问文心一言回答，并获取文心一言的答案
- 自动勾选文心一言的答案
- 自动进行吓一题，下一个测试
- 自动保存，并未提交，方便查阅或修改


## 使用说明

### 安装paddlepaddle pencv-python Pillow等库

1. pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
2. pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
3. pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple

### Chrome 浏览器加载本地cookie

将C:\Users\<用户名>\AppData\Local\Google\Chrome\User Data  的User Data文件夹复制一份放在自己相放的地方，并将复制的文件夹路径填入代码的path中

### 操作步骤

刷课运行AotoCourse.py，刷课运行AutoTest.py


### 注意

用无界面的browser会使智慧树cookie失效，需要将logIn()里的输入账号密码的注释打开，并填入账号密码，而有界面的browser不会有这样的问题

