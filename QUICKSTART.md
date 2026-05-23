# 🚀 快速开始（5分钟搞定）

## 第一步：获取免费API Key（2分钟）

### DeepSeek API（推荐）
1. 打开 https://platform.deepseek.com
2. 点击「注册」，用手机号注册
3. 登录后，点击「API Keys」
4. 点击「创建API Key」，复制保存

**免费额度：新用户送500万token，够用很久！**

## 第二步：本地测试（1分钟）

```bash
# 进入项目目录
cd emotional-ai-bot

# 安装依赖
pip install -r requirements.txt

# 创建配置文件
cp .env.example .env

# 编辑.env，填入你的API Key
# WECHAT_TOKEN=随便填一个
# DEEPSEEK_API_KEY=你的API Key

# 运行测试
python test_local.py
```

看到「小暖: 你好呀！」说明成功了！

## 第三步：部署到Vercel（2分钟）

### 3.1 准备GitHub仓库

1. 在GitHub上创建新仓库（名字随意，比如 `emotional-ai-bot`）
2. 把项目文件上传到仓库

### 3.2 部署到Vercel

1. 打开 https://vercel.com
2. 用GitHub账号登录
3. 点击「New Project」
4. 选择你刚才创建的仓库
5. 点击「Deploy」

### 3.3 配置环境变量

1. 在Vercel项目设置中，找到「Environment Variables」
2. 添加两个变量：
   - `WECHAT_TOKEN`: 随便填一个字符串（比如 `mytoken123`）
   - `DEEPSEEK_API_KEY`: 你的DeepSeek API Key
3. 重新部署项目

## 第四步：配置微信公众号（5分钟）

### 4.1 注册公众号

1. 打开 https://mp.weixin.qq.com
2. 点击「立即注册」
3. 选择「订阅号」
4. 按提示完成注册

### 4.2 配置服务器

1. 登录公众号后台
2. 左侧菜单「开发」→「基本配置」
3. 找到「服务器配置」
4. 填写：
   - URL: `https://你的项目名.vercel.app/wechat`
   - Token: 和你填的 `WECHAT_TOKEN` 一样
   - EncodingAESKey: 点击「随机生成」
   - 消息加解密方式: 选择「明文模式」
5. 点击「提交」
6. 点击「启用」

### 4.3 测试

1. 用手机微信扫描公众号二维码关注
2. 发送任意消息
3. 等待几秒，应该收到AI回复！

## 🎉 完成！

现在你的AI陪伴机器人已经上线了！

## ⚠️ 常见问题

### Q: 收不到回复？
A: 检查以下几点：
- Vercel部署是否成功
- 环境变量是否正确填写
- 公众号服务器配置是否正确

### Q: 回复很慢？
A: 免费服务器有冷启动延迟，首次回复可能需要几秒，这是正常的。

### Q: API额度用完了？
A: DeepSeek的免费额度用完后，可以：
- 等下个月额度刷新
- 注册新账号
- 充值（很便宜）

### Q: 对话没有记忆？
A: 当前版本用内存存储，重启会丢失。后续可以加数据库。

## 📱 下一步优化

有了收入后，可以考虑：
1. 添加数据库（永久保存对话）
2. 实现会员系统（限制免费次数）
3. 接入微信支付
4. 开发小程序版本

---

有问题随时问我！💕
