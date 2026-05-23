"""本地测试脚本 - 模拟微信消息"""
import asyncio
from main import get_ai_reply

async def test_chat():
    print("=== 小暖AI本地测试 ===\n")

    # 模拟用户ID
    user_id = "test_user_001"

    while True:
        user_msg = input("你: ")
        if user_msg.lower() in ['退出', 'quit', 'exit']:
            print("\n再见！💕")
            break

        reply = await get_ai_reply(user_id, user_msg)
        print(f"小暖: {reply}\n")

if __name__ == "__main__":
    asyncio.run(test_chat())
