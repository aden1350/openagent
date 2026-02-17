"""
自我迭代模块
让 Agent 能够持续学习和优化自己
"""
from typing import Dict, List, Any
from datetime import datetime


class SelfImprover:
    """
    自我迭代器
    
    功能：
    - 记录学习心得
    - 分析不足并改进
    - 生成优化建议
    """
    
    def __init__(self):
        self.learnings: List[Dict] = []
        self.improvements: List[Dict] = []
    
    def add_learning(self, topic: str, content: str, source: str = "research"):
        """记录学习"""
        self.learnings.append({
            "topic": topic,
            "content": content,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_improvement(self) -> str:
        """生成改进建议"""
        if not self.learnings:
            return "暂无学习记录"
        
        recent = self.learnings[-5:]
        suggestions = []
        
        for learning in recent:
            topic = learning["topic"]
            suggestions.append(f"- {topic}: {learning['content'][:100]}")
        
        return "\n".join([
            "📚 最近学习:",
            *suggestions,
            "",
            "💡 改进建议:",
            "1. 将学到的知识应用到代码中",
            "2. 优化现有模块",
            "3. 添加新功能"
        ])
    
    def reflect_and_improve(self, task_result: str, feedback: str = None) -> Dict:
        """反思并改进"""
        improvement = {
            "task": task_result,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "action": None
        }
        
        # 简单分析
        if "error" in task_result.lower() or "失败" in task_result:
            improvement["action"] = "需要调试修复"
        elif "success" in task_result.lower() or "成功" in task_result:
            improvement["action"] = "可复制到其他场景"
        
        self.improvements.append(improvement)
        return improvement
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "total_learnings": len(self.learnings),
            "total_improvements": len(self.improvements),
            "recent_topics": [l["topic"] for l in self.learnings[-5:]]
        }


# 全局实例
self_improver = SelfImprover()


# 使用示例
if __name__ == "__main__":
    # 记录学习
    self_improver.add_learning(
        "分级记忆",
        "使用L1/L2/L3分层管理上下文",
        "research"
    )
    
    # 反思改进
    result = self_improver.reflect_and_improve("成功分析A股数据")
    
    # 获取状态
    print(self_improver.get_status())
    print(self_improver.generate_improvement())
