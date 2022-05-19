# feishu-notifier-bot

飞书/Lark 通知用机器人

## 开发初衷

人在国内，想要有一个免费的方式收取程序运行的信息。而国内的聊天软件同时满足开放、有一定装机量、跨平台的不多，所以选择使用飞书/Lark。

从实现方式来说，最简单应该是创建一个群，然后添加自定义机器人，使用 webhook url 发送（不过我没有实验过），但是这种模式需要先拉一个群，对于个人版飞书，操作起来不自然。

## 实现方式

使用飞书的机器人，应用程序发送信息给机器人的代理服务，服务调用机器人将信息发到个人飞书。这是考虑到在应用程序中嵌入机器人发信息的代码通用性较差，且发消息的代码也不是十分轻量，所以将机器人发信息做成一个服务，应用程序通过 http 请求调用。相当于做一个套机器人，本项目就是这个代理服务（也可以理解成机器人）。注意这个服务只能支持定向发送到一个人。

## 使用方法

### 准备工作

- 安装飞书并创建一个个人帐号
- 创建机器人
  - 按照[飞书开放平台](https://open.feishu.cn/app?lang=zh-CN)的指引创建应用，并且启用机器人
  - 在“权限管理”面板中开通“获取与发送单聊、群组消息”
  - 发布机器人
  - 记录应用凭证的 app id 和 app secret
- 一台可以访问公网的机器，安装了docker或有python3.10以上环境
- 找到自己的飞书帐号的open id

### 部署

#### docker

```bash
$ docker run -d -e YOUR_APP_ID=${YOUR_APP_ID} \
  -e APP_SECRET=${YOUR_APP_SECRET} \
  -e OPEN_ID=${OPEN_ID_OF_YOUR_RECEIVE_ACCOUNT} \
  -p 8000:80 dxsooo/feishu-notifier-bot
```

API 服务将部署到 <http://localhost:8000>

#### 源码部署

```bash
# clone项目后
$ cd feishu-notifier-bot

# 安装依赖
$ pip install -r requirements.txt

# 创建环境变量文件
$ cat > .env << EOF
APP_ID=${YOUR_APP_ID}
APP_SECRET=${YOUR_APP_SECRET}
OPEN_ID=${OPEN_ID_OF_YOUR_RECEIVE_ACCOUNT}
EOF

# 启动
$ uvicorn app.main:app
```

API 服务将部署到 <http://localhost:8000>

### 使用示例

```bash
curl -X POST http://localhost:8000/notifications -H 'Content-Type: application/json' -d '{"content":"对不起，我是警察"}'
```

## 开发

服务基于 [FastAPI](https://github.com/tiangolo/fastapi) 开发，包管理工具使用 Poetry

```bash
# 初始化项目
$ poetry install

# 启动
$ uvicorn app.main:app --reload
```

主要逻辑代码位于 [app/](./app/) 下，参考[飞书官方的示例](https://github.com/larksuite/lark-samples/tree/main/robot_quick_start/python)改写。
