# 小暖AI陪伴机器人

一个温柔的AI陪伴聊天机器人，支持微信公众号部署。

## 功能特点

- 温柔体贴的AI人设
- 记住用户对话历史
- 微信公众号消息自动回复
- 完全免费部署

## 部署步骤

### 1. 获取DeepSeek API Key

1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
2. 注册账号（新用户送500万token）
3. 创建API Key

### 2. 注册微信公众号

1. 访问 [mp.weixin.qq.com](https://mp.weixin.qq.com)
2. 注册订阅号（免费）
3. 记录AppID和AppSecret

### 3. 部署到Vercel（免费）

1. Fork本项目到你的GitHub
2. 在Vercel中导入项目
3. 添加环境变量：
   - `WECHAT_TOKEN`: 你在公众号后台设置的Token
   - `DEEPSEEK_API_KEY`: 你的DeepSeek API Key

### 4. 配置公众号

1. 登录公众号后台
2. 进入「开发」→「基本配置」
3. 服务器URL填写：`https://你的项目名.vercel.app/wechat`
4. Token填写：与环境变量中的WECHAT_TOKEN一致
5. 点击「提交」验证

### 5. 测试

关注你的公众号，发送消息测试！

## 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env
# 编辑.env填入你的配置

# 运行
python main.py
```

## 文件说明

- `main.py`: 主程序，处理微信消息和AI回复
- `requirements.txt`: Python依赖
- `.env.example`: 环境变量模板
- `config.py`: 配置文件（本地测试用）

## 注意事项

- 免费方案有一些限制（冷启动、API额度等）
- 对话历史存储在内存中，重启会丢失
- 生产环境建议使用数据库存储

## 后续优化

- [ ] 添加数据库存储对话历史
- [ ] 实现用户会员系统
- [ ] 添加每日消息次数限制
- [ ] 接入微信支付
- [ ] 开发小程序版本
