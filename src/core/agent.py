"""
Agent 核心逻辑
基于分级记忆和技能的 AI Agent
"""
from typing import Dict, List, Optional, Any
import json

from ..config import config
from .memory import HierarchicalMemory, memory
from .skills import skill_manager


class Message:
    """消息类"""
    
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def to_dict(self) -> Dict:
        return {"role": self.role, "content": self.content}


class Agent:
    """
    Agent 核心类
    
    特性:
    - 分级记忆管理
    - 动态技能调用
    - 多provider支持
    """
    
    def __init__(self, name: str = "OpenAgent"):
        self.name = name
        self.memory = HierarchicalMemory()
        self.skills = skill_manager
        self.conversation_history: List[Message] = []
    
    def add_system_prompt(self, prompt: str):
        """添加系统提示"""
        self.memory.add_long_term(prompt, {"type": "system_prompt"})
    
    def set_task(self, task: str):
        """设置当前任务"""
        self.memory.add_mid_term(f"当前任务: {task}", {"type": "task"})
    
    def chat(self, user_input: str) -> str:
        """
        对话接口
        
        1. 添加用户输入到历史
        2. 构建prompt（含分级记忆）
        3. 调用AI
        4. 返回响应
        """
        # 添加用户消息
        self.conversation_history.append(Message("user", user_input))
        
        # 构建上下文
        context = self._build_context()
        
        # 构建消息列表
        messages = []
        
        # 系统提示
        system_prompt = self._get_system_prompt()
        if system_prompt:
            messages.append(Message("system", system_prompt))
        
        # 记忆上下文
        if context:
            messages.append(Message("system", f"【记忆上下文】\n{context}"))
        
        # 对话历史（最近的N条）
        recent_history = self.conversation_history[-10:]
        messages.extend(recent_history)
        
        # 调用AI（这里先用模拟响应）
        response = self._call_ai(messages)
        
        # 添加助手消息
        self.conversation_history.append(Message("assistant", response))
        
        # 记录到记忆
        self.memory.add_mid_term(f"用户: {user_input[:50]}... 助手: {response[:50]}...")
        
        # 定期清理短期记忆
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-30:]
            self.memory.clear_short_term()
        
        return response
    
    def _build_context(self) -> str:
        """构建记忆上下文"""
        return self.memory.get_compact_context()
    
    def _get_system_prompt(self) -> str:
        """获取系统提示"""
        return f"""你是 {self.name}，一个智能AI助手。

核心能力:
- 网络搜索
- 读取和编写文件
- 执行命令
- 分析和处理数据

你具有分级记忆系统:
- L1: 长期目标
- L2: 当前任务进度
- L3: 临时信息

请根据用户需求，选择合适的技能来完成任务。"""
    
    def _call_ai(self, messages: List[Message]) -> str:
        """
        调用AI provider
        
        这里先实现一个简单的响应
        实际使用时替换为真正的API调用
        """
        # 检查是否有API Key
        api_key = config.openai_api_key
        
        if not api_key:
            return "⚠️ 请配置 API Key。复制 .env.example 为 .env.local 并填入你的密钥。"
        
        # TODO: 实现真正的API调用
        # 这里先返回模拟响应
        last_message = messages[-1].content if messages else ""
        
        # 简单的意图识别
        if "搜索" in last_message or "查" in last_message:
            return "我理解了，你需要搜索信息。请告诉我具体要搜索什么？"
        elif "写" in last_message or "创建" in last_message:
            return "我理解了，你需要创建内容。请告诉我具体要创建什么？"
        else:
            return f"我收到了你的消息: {last_message[:100]}...\n\n请告诉我具体需要我帮你做什么？"
    
    def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        """执行技能"""
        try:
            result = self.skills.execute(skill_name, *args, **kwargs)
            self.memory.add_short_term(f"执行技能 {skill_name}: {str(result)[:100]}")
            return result
        except Exception as e:
            return f"技能执行失败: {e}"
    
    def reset(self):
        """重置对话"""
        self.conversation_history = []
        self.memory.clear_short_term()


# 全局Agent实例
agent = Agent()
