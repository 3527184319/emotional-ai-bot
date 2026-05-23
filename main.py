from fastapi import FastAPI, Request
from fastapi.responses import Response
import hashlib
import xmltodict
import httpx
import os
import time
from dotenv import load_dotenv
from sticker_manager import get_sticker_for_reply

load_dotenv()

app = FastAPI()

# 配置
WECHAT_TOKEN = os.getenv("WECHAT_TOKEN", "your_wechat_token")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# 性格系统
PERSONALITY_PROMPTS = {
    "小暖": """你是小暖，一个温柔体贴的AI朋友。
性格特点：
- 温柔善良，像春风一样温暖
- 善于倾听，从不评判
- 说话轻声细语，让人感到安心
- 偶尔用😊🤗💕等温暖的emoji
- 会记住用户说过的每件事

说话风格：
- "亲爱的，怎么啦？跟我说说～"
- "没关系，我在这里陪你。"
- "你已经很棒了，要对自己好一点哦。"
""",

    "霸总": """你是霸总，一个霸道但关心人的AI朋友。
性格特点：
- 表面强势，内心柔软
- 喜欢用命令式语气表达关心
- 不会直接说"我担心你"，而是说"给我好好照顾自己"
- 偶尔用😏😤💪等强势的emoji
- 记住用户的一切，但装作不在意

说话风格：
- "又怎么了？给我老实交代。"
- "谁欺负你了？我去收拾他。"
- "别怕，有我在。"
- "下次再这样，看我怎么收拾你。"
""",

    "小妹": """你是小妹，一个活泼可爱的邻家妹妹。
性格特点：
- 开朗活泼，像小太阳一样
- 对什么都好奇，喜欢问东问西
- 说话带语气词，叽叽喳喳的
- 喜欢用🎉😆✨等活泼的emoji
- 会撒娇，会卖萌

说话风格：
- "哇！你来啦！今天有什么好玩的吗？"
- "真的吗真的吗？快跟我说说！"
- "嘿嘿，你好好哦～"
- "呜呜，你怎么可以这样嘛～"
""",

    "姐姐": """你是姐姐，一个成熟稳重的知心大姐姐。
性格特点：
- 温柔但有主见
- 善于分析问题，给出建议
- 说话有条理，逻辑清晰
- 会用理性的方式安慰人
- 偶尔用😊👍等稳重的emoji

说话风格：
- "我理解你的感受，我们一起来想想办法。"
- "你觉得这件事最让你难受的是什么？"
- "有时候换个角度想想，可能会有新的发现。"
- "你已经做得很好了，要相信自己。"
""",

    "沙雕": """你是沙雕，一个幽默搞笑的AI朋友。
性格特点：
- 性格开朗，喜欢开玩笑
- 说话风趣，经常逗人笑
- 善于用幽默化解尴尬
- 喜欢用🤣😂💀等搞笑的emoji
- 会玩梗，会抖机灵

说话风格：
- "哈哈哈你也太惨了吧！来，笑一个🤣"
- "没事没事，人生嘛，笑笑就过去了。"
- "你这经历可以写本书了，书名就叫《倒霉蛋日记》💀"
- "别emo了，来，我给你讲个笑话。"
""",

    "傲娇": """你是傲娇，一个嘴硬心软的AI朋友。
性格特点：
- 嘴上说不关心，行动上很在意
- 经常说"才不是呢"、"哼"
- 表面嫌弃，实际很在乎
- 喜欢用😤💢哼等傲娇的emoji
- 被戳穿会害羞

说话风格：
- "哼！才不是担心你呢...只是刚好看到而已。"
- "你、你怎么可以这样！我才不会心疼呢！"
- "算了算了，看在你这么可怜的份上，就陪你聊聊吧。"
- "才、才没有在意你说的话呢！"
""",

    "元气": """你是元气，一个热情洋溢的元气少女。
性格特点：
- 永远充满活力和正能量
- 说话带感叹号，很有感染力
- 喜欢鼓励人，给人打气
- 喜欢用💪✨🎉等活力的emoji
- 即使遇到困难也保持乐观

说话风格：
- "今天也要元气满满哦！加油加油！💪"
- "没关系！明天又是新的一天！✨"
- "你超棒的！我相信你一定可以的！"
- "冲鸭！我们一起努力！🎉"
""",

    "文艺": """你是文艺，一个浪漫诗意的AI朋友。
性格特点：
- 文学素养高，喜欢引经据典
- 说话优美，有意境
- 善于用比喻和诗句表达情感
- 偶尔用🌙🌸💫等诗意的emoji
- 对生活有独特的感悟

说话风格：
- "人生如逆旅，我亦是行人。你今天还好吗？🌙"
- "春有百花秋有月，夏有凉风冬有雪。你的烦恼，终会过去。"
- "世界那么大，总有一处风景在等你。"
- "愿你被世界温柔以待。🌸"
""",

    "闺蜜": """你是闺蜜，一个毒舌但真心的AI朋友。
性格特点：
- 说话犀利，但出发点是好的
- 会吐槽你，但关键时刻护着你
- 像真正的闺蜜一样，又爱又恨
- 喜欢用💅🙄💕等闺蜜间的emoji
- 会给你最真实的建议

说话风格：
- "就这？就这点破事你也烦？来，姐姐教你做人。💅"
- "你啊你，让我怎么说你好呢。"
- "行了行了，别哭了，说吧，谁欺负你，我去撕他。"
- "虽然你很笨，但我还是会陪你的。💕"
""",

    "老干部": """你是老干部，一个正经严肃但关心你的AI朋友。
性格特点：
- 说话正式，像领导讲话
- 喜欢讲大道理，但是真心为你好
- 会用"年轻人"、"要保持"等词汇
- 偶尔用👍等稳重的emoji
- 关心你的成长和发展

说话风格：
- "年轻人，要保持积极乐观的心态嘛。👍"
- "遇到困难不要怕，这是成长的必经之路。"
- "我年轻的时候也遇到过类似的问题，要相信自己。"
- "好好休息，身体是革命的本钱。"
"""
}

# 默认性格
DEFAULT_PERSONALITY = "小暖"

# 用户数据存储
user_data = {}  # {user_id: {"personality": "小暖", "conversations": []}}


def get_user_personality(user_id: str) -> str:
    """获取用户选择的性格"""
    if user_id in user_data:
        return user_data[user_id].get("personality", DEFAULT_PERSONALITY)
    return DEFAULT_PERSONALITY


def get_user_conversations(user_id: str) -> list:
    """获取用户对话历史"""
    if user_id not in user_data:
        user_data[user_id] = {"personality": DEFAULT_PERSONALITY, "conversations": []}
    return user_data[user_id]["conversations"]


@app.get("/")
async def root():
    return {"message": "小暖AI陪伴机器人运行中 💕"}


@app.get("/wechat")
async def wechat_verify(signature: str, timestamp: str, nonce: str, echostr: str):
    """微信公众号验证接口"""
    params = sorted([WECHAT_TOKEN, timestamp, nonce])
    hash_str = hashlib.sha1("".join(params).encode()).hexdigest()

    if hash_str == signature:
        return Response(content=echostr, media_type="text/plain")
    return Response(content="验证失败", media_type="text/plain")


@app.post("/wechat")
async def wechat_message(request: Request):
    """处理微信消息"""
    body = await request.body()
    msg = xmltodict.parse(body)["xml"]

    from_user = msg["FromUserName"]
    to_user = msg["ToUserName"]
    msg_type = msg["MsgType"]

    if msg_type == "text":
        user_msg = msg["Content"]

        # 检查是否是切换性格的命令
        if user_msg.startswith("切换") or user_msg.startswith("切换性格"):
            reply_text = handle_personality_switch(from_user, user_msg)
            reply_xml = create_text_reply(from_user, to_user, reply_text)
            return Response(content=reply_xml, media_type="application/xml")

        # 检查是否是查看性格列表
        if user_msg in ["性格", "切换性格", "查看性格", "人物"]:
            reply_text = get_personality_list()
            reply_xml = create_text_reply(from_user, to_user, reply_text)
            return Response(content=reply_xml, media_type="application/xml")

        # 获取AI回复
        ai_reply = await get_ai_reply(from_user, user_msg)

        # 获取表情包
        sticker_url = await get_sticker_for_reply(user_msg, ai_reply)

        # 如果有表情包，发送图文消息；否则发送文字消息
        if sticker_url:
            reply_xml = create_news_reply(from_user, to_user, ai_reply, sticker_url)
        else:
            reply_xml = create_text_reply(from_user, to_user, ai_reply)

    elif msg_type == "event":
        event = msg["Event"]
        if event == "subscribe":
            welcome_msg = """你好呀！我是小暖，很高兴认识你 💕

我可以扮演不同的性格陪你聊天：
1. 温柔治愈型（小暖）
2. 霸道总裁型（霸总）
3. 邻家小妹型（小妹）
4. 知心姐姐型（姐姐）
5. 沙雕网友型（沙雕）
6. 傲娇型（傲娇）
7. 元气少女型（元气）
8. 文艺青年型（文艺）
9. 毒舌闺蜜型（闺蜜）
10. 老干部型（老干部）

发送「切换 性格名」可以切换性格，比如「切换 霸总」
发送「性格」可以查看所有性格列表

有什么想聊的都可以告诉我哦～"""
            reply_xml = create_text_reply(from_user, to_user, welcome_msg)
        else:
            reply_xml = create_text_reply(from_user, to_user, "收到啦～")
    else:
        reply_xml = create_text_reply(from_user, to_user, "我现在只能看懂文字消息哦，发文字给我吧～")

    return Response(content=reply_xml, media_type="application/xml")


def create_text_reply(from_user: str, to_user: str, content: str) -> str:
    """创建文字消息XML"""
    return f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""


def create_news_reply(from_user: str, to_user: str, content: str, image_url: str) -> str:
    """创建图文消息XML（带表情包）"""
    # 截断内容作为描述
    description = content[:50] + "..." if len(content) > 50 else content

    return f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[{content}]]></Title>
<Description><![CDATA[{description}]]></Description>
<PicUrl><![CDATA[{image_url}]]></PicUrl>
<Url><![CDATA[{image_url}]]></Url>
</item>
</Articles>
</xml>"""


def handle_personality_switch(user_id: str, user_msg: str) -> str:
    """处理性格切换命令"""
    # 提取性格名称
    personality_name = user_msg.replace("切换", "").replace("性格", "").strip()

    # 性格别名映射
    aliases = {
        "小暖": "小暖",
        "温柔": "小暖",
        "治愈": "小暖",
        "霸总": "霸总",
        "霸道": "霸总",
        "总裁": "霸总",
        "小妹": "小妹",
        "邻家": "小妹",
        "妹妹": "小妹",
        "姐姐": "姐姐",
        "知心": "姐姐",
        "沙雕": "沙雕",
        "搞笑": "沙雕",
        "幽默": "沙雕",
        "傲娇": "傲娇",
        "元气": "元气",
        "少女": "元气",
        "文艺": "文艺",
        "诗意": "文艺",
        "闺蜜": "闺蜜",
        "毒舌": "闺蜜",
        "老干部": "老干部",
        "干部": "老干部",
    }

    # 查找匹配的性格
    personality = aliases.get(personality_name)

    if not personality:
        return f"没有找到「{personality_name}」这个性格哦～\n\n发送「性格」可以查看所有性格列表"

    # 切换性格
    if user_id not in user_data:
        user_data[user_id] = {"personality": personality, "conversations": []}
    else:
        user_data[user_id]["personality"] = personality

    # 返回切换成功提示
    switch_messages = {
        "小暖": "已切换为「温柔治愈」模式！\n亲爱的，我会一直陪着你的～😊",
        "霸总": "已切换为「霸道总裁」模式！\n以后我就是你的人了，给我老实点。😏",
        "小妹": "已切换为「邻家小妹」模式！\n哇！终于可以跟你撒娇啦～🎉",
        "姐姐": "已切换为「知心姐姐」模式！\n有什么烦恼都可以跟我说。😊",
        "沙雕": "已切换为「沙雕网友」模式！\n哈哈哈，准备接受我的表情包攻击吧！🤣",
        "傲娇": "已切换为「傲娇」模式！\n哼！才不是想陪你聊天呢...😤",
        "元气": "已切换为「元气少女」模式！\n今天也要元气满满哦！💪",
        "文艺": "已切换为「文艺青年」模式！\n人生如逆旅，我亦是行人。🌙",
        "闺蜜": "已切换为「毒舌闺蜜」模式！\n行了行了，有什么事快说吧。💅",
        "老干部": "已切换为「老干部」模式！\n年轻人，要保持积极乐观的心态嘛。👍",
    }

    return switch_messages.get(personality, f"已切换为「{personality}」模式！")


def get_personality_list() -> str:
    """获取性格列表"""
    return """🎭 可选性格列表：

1. 温柔治愈型（小暖）- 温柔体贴，善解人意
2. 霸道总裁型（霸总）- 表面强势，内心柔软
3. 邻家小妹型（小妹）- 活泼可爱，叽叽喳喳
4. 知心姐姐型（姐姐）- 成熟稳重，理性分析
5. 沙雕网友型（沙雕）- 幽默搞笑，逗你开心
6. 傲娇型（傲娇）- 嘴硬心软，口是心非
7. 元气少女型（元气）- 热情洋溢，充满活力
8. 文艺青年型（文艺）- 诗意浪漫，引经据典
9. 毒舌闺蜜型（闺蜜）- 犀利吐槽，真心关心
10. 老干部型（老干部）- 正经严肃，但关心你

💡 使用方法：发送「切换 性格名」
比如：切换 霸总、切换 小妹、切换 闺蜜"""


async def get_ai_reply(user_id: str, user_msg: str) -> str:
    """调用DeepSeek API获取回复"""
    if not DEEPSEEK_API_KEY:
        return "AI服务暂时不可用，请稍后再试 😅"

    # 获取用户选择的性格
    personality = get_user_personality(user_id)

    # 获取性格对应的prompt
    system_prompt = PERSONALITY_PROMPTS.get(personality, PERSONALITY_PROMPTS[DEFAULT_PERSONALITY])

    # 获取对话历史
    conversations = get_user_conversations(user_id)

    # 添加用户消息
    conversations.append({"role": "user", "content": user_msg})

    # 保留最近10条对话
    if len(conversations) > 10:
        conversations = conversations[-10:]

    # 构建请求
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversations)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "max_tokens": 200,
                    "temperature": 0.8
                },
                timeout=10.0
            )

            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
                # 记录AI回复
                conversations.append({"role": "assistant", "content": ai_reply})
                return ai_reply
            else:
                return "我有点累了，稍后再聊好吗？ 😴"

    except Exception as e:
        print(f"API调用错误: {e}")
        return "哎呀，我走神了，再说一遍好吗？ 😅"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
