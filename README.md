# FocusGPT DEMO

这是基于DataFocus开放的API和前端组件，搭建的一个DEMO。

需要node.js环境编译前端，和python后端环境

运行脚本

```bash
start.bat
```

![sample](./sample.jpg)

### 配置

可以指定环境变量DF_URL和DF_APP_TOKEN来配置DataFocus环境和APP_TOKEN信息，或是在server/config.py中直接指定

```python
# server/config.py
# Datafocus环境配置
DF_URL = os.getenv("DF_URL", "https://cloud001.datafocus.ai")
DF_APP_TOKEN = os.getenv("DF_APP_TOKEN", "NWIzZjg1OT********************************************************************lhMzMwNGE=")

```



