#!/usr/bin/env python3
"""
OpenAgent 主入口
快速启动你的 AI Agent
"""
from src.core.agent import Agent


def main():
    """主函数"""
    print("=" * 50)
    print("🤖 OpenAgent - 可迭代的 Agent 框架")
    print("=" * 50)
    print()
    
    # 创建 Agent
    agent = Agent(name="OpenAgent")
    
    # 设置身份
    agent.add_system_prompt("你是一个有帮助的AI助手，专注于帮你完成各种任务。")
    
    # 设置当前任务
    agent.set_task("与用户对话")
    
    print("Agent 已启动！")
    print("输入 'quit' 或 'exit' 退出")
    print()
    
    # 对话循环
    while True:
        try:
            user_input = input("你> ").strip()
            
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("再见！👋")
                break
            
            if not user_input:
                continue
            
            # 获取回复
            response = agent.chat(user_input)
            print(f"Agent> {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n再见！👋")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()
