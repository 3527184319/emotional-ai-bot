"""表情包管理器 - 根据对话内容搜索匹配的表情包"""
import httpx
import random
from typing import Optional

# 免费表情包API配置
# 方案1: 使用Giphy的公开API（有限制但免费）
# 方案2: 使用本地表情包URL（更稳定）

# 情绪关键词映射（用于搜索）
EMOTION_SEARCH_KEYWORDS = {
    "happy": ["happy", "celebration", "joy", "dance", "yay"],
    "excited": ["excited", "omg", "wow", "amazing"],
    "love": ["love", "heart", "kiss", "hug", "cute"],
    "laugh": ["lol", "laugh", "funny", "haha", "meme"],
    "sad": ["sad", "cry", "tears", "comfort", "hug"],
    "angry": ["angry", "annoyed", "mad", "frustrated"],
    "tired": ["tired", "sleepy", "exhausted", "nap"],
    "stressed": ["stress", "anxiety", "worried", "calm"],
    "goodmorning": ["good morning", "wake up", "coffee", "sunshine"],
    "goodnight": ["goodnight", "sleep", "sweet dreams", "night"],
    "eating": ["eating", "food", "yummy", "hungry"],
    "studying": ["studying", "homework", "focus", "book"],
    "working": ["working", "office", "busy", "deadline"],
    "greeting": ["hi", "hello", "wave", "hey"],
    "encourage": ["fighting", "ganbare", "you can do it", "cheer up"],
    "patpat": ["headpat", "pat", "pet", "gentle"],
    "shy": ["shy", "blush", "embarrassed", "nervous"],
}

# 关键词检测（从用户消息中提取情绪）
# 注意：关键词要精确，避免误匹配
KEYWORD_DETECT = {
    "happy": ["开心", "高兴", "快乐", "太好了", "哈哈", "嘿嘿", "耶", "棒极了"],
    "excited": ["激动", "兴奋", "太棒了", "amazing", "天哪", "哇塞"],
    "love": ["爱你", "喜欢你", "心动", "甜蜜", "么么", "宝贝"],
    "laugh": ["笑死", "哈哈哈", "太搞笑了", "lol", "笑死我了"],
    "sad": ["难过", "伤心", "想哭", "不开心", "郁闷", "唉", "心烦", "心情不好"],
    "angry": ["生气", "气死", "烦死了", "讨厌", "愤怒"],
    "tired": ["累了", "困了", "疲惫", "想睡觉", "加班累"],
    "stressed": ["压力大", "焦虑", "担心", "紧张", "考试"],
    "goodmorning": ["早安", "早上好", "早呀", "起床了"],
    "goodnight": ["晚安", "要睡了", "困了要睡", "休息了"],
    "eating": ["吃饭", "饿了", "好吃", "外卖", "美食", "饿"],
    "studying": ["学习", "看书", "作业", "考试", "复习"],
    "working": ["上班", "工作", "加班", "开会", "好忙"],
    "greeting": ["你好", "嗨", "hi", "hello", "在吗"],
    "encourage": ["加油", "坚持", "努力", "撑住"],
    "patpat": ["摸摸", "抱抱", "拍拍", "安慰我"],
    "shy": ["害羞", "不好意思", "脸红", "尴尬"],
}

# 预定义的表情包URL（免费GIF资源）
# 使用Tenor的直接链接（无需API）
STICKER_URLS = {
    "happy": [
        "https://media.tenor.com/images/5e89c7f9b9b5b5b5b5b5b5b5b5b5b5b5/tenor.gif",
        "https://media.tenor.com/images/happy-dance/happy-dance.gif",
    ],
    "sad": [
        "https://media.tenor.com/images/sad-anime/sad-anime.gif",
        "https://media.tenor.com/images/comfort-hug/comfort-hug.gif",
    ],
    "laugh": [
        "https://media.tenor.com/images/lol-funny/lol-funny.gif",
        "https://media.tenor.com/images/laughing/laughing.gif",
    ],
    "love": [
        "https://media.tenor.com/images/love-heart/love-heart.gif",
        "https://media.tenor.com/images/kiss/kiss.gif",
    ],
    "goodnight": [
        "https://media.tenor.com/images/goodnight-sleep/goodnight-sleep.gif",
        "https://media.tenor.com/images/sweet-dreams/sweet-dreams.gif",
    ],
    "goodmorning": [
        "https://media.tenor.com/images/good-morning/good-morning.gif",
        "https://media.tenor.com/images/wake-up/wake-up.gif",
    ],
    "encourage": [
        "https://media.tenor.com/images/fighting/fighting.gif",
        "https://media.tenor.com/images/you-can-do-it/you-can-do-it.gif",
    ],
    "patpat": [
        "https://media.tenor.com/images/headpat/headpat.gif",
        "https://media.tenor.com/images/pat-pat/pat-pat.gif",
    ],
}

# 备用表情包（当API失败时使用）
FALLBACK_STICKERS = {
    "happy": "https://media.tenor.com/images/5e89c7f9b9b5b5b5b5b5b5b5b5b5b5b5/tenor.gif",
    "sad": "https://media.tenor.com/images/sad-anime/sad-anime.gif",
    "laugh": "https://media.tenor.com/images/lol-funny/lol-funny.gif",
    "love": "https://media.tenor.com/images/love-heart/love-heart.gif",
    "goodnight": "https://media.tenor.com/images/goodnight-sleep/goodnight-sleep.gif",
    "goodmorning": "https://media.tenor.com/images/good-morning/good-morning.gif",
    "encourage": "https://media.tenor.com/images/fighting/fighting.gif",
    "patpat": "https://media.tenor.com/images/headpat/headpat.gif",
    "greeting": "https://media.tenor.com/images/hello-wave/hello-wave.gif",
    "tired": "https://media.tenor.com/images/tired-sleepy/tired-sleepy.gif",
    "angry": "https://media.tenor.com/images/angry-annoyed/angry-annoyed.gif",
    "excited": "https://media.tenor.com/images/excited-wow/excited-wow.gif",
    "stressed": "https://media.tenor.com/images/stress-anxiety/stress-anxiety.gif",
    "eating": "https://media.tenor.com/images/eating-food/eating-food.gif",
    "studying": "https://media.tenor.com/images/studying-book/studying-book.gif",
    "working": "https://media.tenor.com/images/working-office/working-office.gif",
    "shy": "https://media.tenor.com/images/shy-blush/shy-blush.gif",
}


async def detect_emotion(text: str) -> str:
    """从用户消息中检测情绪"""
    text_lower = text.lower()

    # 统计每个情绪的匹配分数
    scores = {}
    for emotion, keywords in KEYWORD_DETECT.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[emotion] = score

    if scores:
        # 返回得分最高的情绪
        return max(scores, key=scores.get)

    # 默认返回问候
    return "greeting"


async def search_sticker_from_api(emotion: str) -> Optional[str]:
    """从API搜索表情包（可选功能）"""
    # 这里可以接入Giphy、Tenor等API
    # 目前返回None，使用本地预定义的表情包
    return None


async def search_sticker(emotion: str, limit: int = 5) -> Optional[str]:
    """根据情绪搜索表情包，返回URL"""

    # 首先尝试从API搜索（如果配置了API key）
    api_result = await search_sticker_from_api(emotion)
    if api_result:
        return api_result

    # 使用预定义的表情包
    stickers = STICKER_URLS.get(emotion, [])

    if stickers:
        return random.choice(stickers)

    # 使用备用表情包
    fallback = FALLBACK_STICKERS.get(emotion)
    if fallback:
        return fallback

    # 最后的备用方案：返回一个通用的表情包
    return "https://media.tenor.com/images/hello-wave/hello-wave.gif"


async def get_sticker_for_reply(user_msg: str, ai_reply: str) -> Optional[str]:
    """根据对话内容获取合适的表情包"""

    # 首先从用户消息检测情绪
    emotion = await detect_emotion(user_msg)

    # 搜索表情包
    sticker_url = await search_sticker(emotion)

    return sticker_url


# 测试用
if __name__ == "__main__":
    import asyncio

    async def test():
        test_cases = [
            "今天好开心啊！",
            "心情不好，想哭",
            "晚安，我要睡了",
            "早上好呀",
            "哈哈哈笑死我了",
            "考试加油！",
        ]

        for msg in test_cases:
            emotion = await detect_emotion(msg)
            sticker = await search_sticker(emotion)
            print(f"消息: {msg}")
            print(f"情绪: {emotion}")
            print(f"表情包: {sticker}")
            print("-" * 50)

    asyncio.run(test())
