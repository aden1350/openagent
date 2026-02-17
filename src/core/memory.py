"""
Memory System - Hierarchical Memory Management
解决上下文爆炸问题，分层管理记忆
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class MemoryLevel:
    """记忆层级"""
    
    def __init__(self, name: str, max_items: int = 10, ttl_seconds: int = 3600):
        self.name = name
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self.items: List[Dict[str, Any]] = []
    
    def add(self, content: str, metadata: Optional[Dict] = None):
        """添加记忆"""
        item = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.items.append(item)
        
        # 超过容量时清理旧记忆
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
    
    def get_context(self, max_items: int = None) -> str:
        """获取上下文（用于构建prompt）"""
        items = self.items[-max_items:] if max_items else self.items
        if not items:
            return ""
        
        context_parts = [f"[{self.name}]"]
        for item in items:
            context_parts.append(f"- {item['content']}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        """清空记忆"""
        self.items = []


class HierarchicalMemory:
    """
    分级记忆系统 (Hierarchical Memory System)
    
    L1 长期记忆: 核心目标、身份、原则 (不清理)
    L2 中期记忆: 当前任务、进度 (保留最近)
    L3 短期记忆: 临时数据、工具输出 (可频繁清理)
    """
    
    def __init__(self):
        # L1: 长期 - 核心身份和目标
        self.long_term = MemoryLevel("L1_LONG_TERM", max_items=50, ttl_seconds=86400 * 30)
        
        # L2: 中期 - 当前任务和进度
        self.mid_term = MemoryLevel("L2_MID_TERM", max_items=20, ttl_seconds=3600)
        
        # L3: 短期 - 工具输出和临时数据
        self.short_term = MemoryLevel("L3_SHORT_TERM", max_items=10, ttl_seconds=300)
    
    def add_long_term(self, content: str, metadata: Optional[Dict] = None):
        """添加长期记忆"""
        self.long_term.add(content, metadata)
    
    def add_mid_term(self, content: str, metadata: Optional[Dict] = None):
        """添加中期记忆"""
        self.mid_term.add(content, metadata)
    
    def add_short_term(self, content: str, metadata: Optional[Dict] = None):
        """添加短期记忆"""
        self.short_term.add(content, metadata)
    
    def get_full_context(self, include_short: bool = True) -> str:
        """获取完整上下文"""
        parts = []
        
        # L1 始终包含
        l1 = self.long_term.get_context()
        if l1:
            parts.append(l1)
        
        # L2 始终包含
        l2 = self.mid_term.get_context()
        if l2:
            parts.append(l2)
        
        # L3 可选
        if include_short:
            l3 = self.short_term.get_context()
            if l3:
                parts.append(l3)
        
        return "\n\n".join(parts)
    
    def get_compact_context(self) -> str:
        """获取精简上下文（用于长对话）"""
        # 只保留L1和L2
        parts = []
        
        l1 = self.long_term.get_context(max_items=5)
        if l1:
            parts.append(l1)
        
        l2 = self.mid_term.get_context(max_items=5)
        if l2:
            parts.append(l2)
        
        return "\n\n".join(parts)
    
    def clear_short_term(self):
        """清空短期记忆"""
        self.short_term.clear()
    
    def to_dict(self) -> Dict:
        """序列化（用于保存）"""
        return {
            "long_term": self.long_term.items,
            "mid_term": self.mid_term.items,
            "short_term": self.short_term.items
        }
    
    def from_dict(self, data: Dict):
        """反序列化"""
        self.long_term.items = data.get("long_term", [])
        self.mid_term.items = data.get("mid_term", [])
        self.short_term.items = data.get("short_term", [])


# 全局实例
memory = HierarchicalMemory()
