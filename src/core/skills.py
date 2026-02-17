"""
技能管理系统
动态加载和管理Agent技能
"""
import os
import importlib
import inspect
from typing import Dict, List, Callable, Any
from pathlib import Path


class Skill:
    """技能类"""
    
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
        self.usage_count = 0
    
    def execute(self, *args, **kwargs) -> Any:
        """执行技能"""
        self.usage_count += 1
        return self.func(*args, **kwargs)


class SkillManager:
    """
    技能管理器
    
    支持:
    - 动态加载技能
    - 技能分类
    - 使用统计
    """
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.categories: Dict[str, List[str]] = {}
        
        # 内置技能
        self._register_builtin_skills()
    
    def _register_builtin_skills(self):
        """注册内置技能"""
        # 搜索技能
        self.register("web_search", "网络搜索", self._web_search)
        
        # 读取文件
        self.register("read_file", "读取文件", self._read_file)
        
        # 写文件
        self.register("write_file", "写文件", self._write_file)
        
        # 执行命令
        self.register("execute_command", "执行Shell命令", self._execute_command)
    
    def register(self, name: str, description: str, func: Callable, category: str = "general"):
        """注册技能"""
        skill = Skill(name, description, func)
        self.skills[name] = skill
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
    
    def get_skill(self, name: str) -> Skill:
        """获取技能"""
        return self.skills.get(name)
    
    def list_skills(self, category: str = None) -> List[Skill]:
        """列出技能"""
        if category:
            skill_names = self.categories.get(category, [])
            return [self.skills[name] for name in skill_names]
        return list(self.skills.values())
    
    def find_skill(self, query: str) -> List[Skill]:
        """查找相关技能"""
        query = query.lower()
        results = []
        for skill in self.skills.values():
            if query in skill.name.lower() or query in skill.description.lower():
                results.append(skill)
        return results
    
    def execute(self, skill_name: str, *args, **kwargs) -> Any:
        """执行技能"""
        skill = self.get_skill(skill_name)
        if not skill:
            raise ValueError(f"Skill '{skill_name}' not found")
        return skill.execute(*args, **kwargs)
    
    # 内置技能实现
    def _web_search(self, query: str) -> str:
        """网络搜索（待实现）"""
        return f"搜索: {query} - 需要配置搜索API"
    
    def _read_file(self, path: str) -> str:
        """读取文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {path}: {e}"
    
    def _write_file(self, path: str, content: str) -> str:
        """写文件"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Written to {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"
    
    def _execute_command(self, cmd: str) -> str:
        """执行命令"""
        import subprocess
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout or result.stderr
        except Exception as e:
            return f"Error: {e}"


# 全局实例
skill_manager = SkillManager()
