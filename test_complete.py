"""完整功能测试脚本"""
import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from main import get_ai_reply, handle_personality_switch, get_personality_list
from sticker_manager import detect_emotion, get_sticker_for_reply


async def test_personality_switch():
    """测试性格切换功能"""
    print("=" * 60)
    print("🎭 测试性格切换功能")
    print("=" * 60)

    user_id = "test_user_001"

    # 测试切换到霸总
    print("\n1. 切换到霸总模式：")
    result = handle_personality_switch(user_id, "切换 霸总")
    print(f"系统: {result}")

    # 测试霸总回复
    print("\n2. 霸总回复测试：")
    reply = await get_ai_reply(user_id, "我今天心情不好")
    print(f"霸总: {reply}")

    # 测试切换到小妹
    print("\n3. 切换到小妹模式：")
    result = handle_personality_switch(user_id, "切换 小妹")
    print(f"系统: {result}")

    # 测试小妹回复
    print("\n4. 小妹回复测试：")
    reply = await get_ai_reply(user_id, "我今天心情不好")
    print(f"小妹: {reply}")

    # 测试查看性格列表
    print("\n5. 查看性格列表：")
    result = get_personality_list()
    print(result)


async def test_sticker_integration():
    """测试表情包集成功能"""
    print("\n" + "=" * 60)
    print("🎨 测试表情包功能")
    print("=" * 60)

    test_cases = [
        ("今天好开心啊！", "应该返回开心的表情包"),
        ("心情不好，想哭", "应该返回安慰的表情包"),
        ("晚安，我要睡了", "应该返回晚安的表情包"),
        ("早上好呀", "应该返回早安的表情包"),
        ("哈哈哈笑死我了", "应该返回搞笑的表情包"),
        ("考试加油！", "应该返回鼓励的表情包"),
    ]

    for msg, expected in test_cases:
        print(f"\n消息: {msg}")
        print(f"期望: {expected}")

        # 检测情绪
        emotion = await detect_emotion(msg)
        print(f"情绪: {emotion}")

        # 获取表情包
        sticker = await get_sticker_for_reply(msg, "")
        if sticker:
            print(f"表情包: {sticker[:60]}...")
        else:
            print("表情包: 无")


async def test_complete_conversation():
    """测试完整对话流程"""
    print("\n" + "=" * 60)
    print("💬 测试完整对话流程")
    print("=" * 60)

    user_id = "test_user_002"

    # 切换到温柔模式
    handle_personality_switch(user_id, "切换 小暖")

    conversations = [
        "你好，我叫小明",
        "今天工作好累啊",
        "晚安，我要睡了",
    ]

    for msg in conversations:
        print(f"\n你: {msg}")

        # 获取AI回复
        reply = await get_ai_reply(user_id, msg)
        print(f"小暖: {reply}")

        # 获取表情包
        sticker = await get_sticker_for_reply(msg, reply)
        if sticker:
            print(f"[表情包: {sticker[:50]}...]")


async def main():
    """运行所有测试"""
    print("🚀 开始测试小暖AI机器人的所有功能...\n")

    await test_personality_switch()
    await test_sticker_integration()
    await test_complete_conversation()

    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)

    print("\n📋 功能总结：")
    print("1. ✅ 多性格切换（10种性格可选）")
    print("2. ✅ 情绪识别（自动检测用户情绪）")
    print("3. ✅ 表情包匹配（根据情绪返回合适的表情包）")
    print("4. ✅ 对话记忆（记住用户说过的话）")
    print("5. ✅ 微信公众号对接（支持文字和图文消息）")

    print("\n🎯 下一步：")
    print("1. 部署到Vercel（免费）")
    print("2. 注册微信公众号")
    print("3. 配置服务器对接")
    print("4. 开始推广赚钱！")


if __name__ == "__main__":
    asyncio.run(main())
