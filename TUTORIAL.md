# OpenAgent 教程

> 本框架由 OpenClaw + MiniMax M2.5 驱动，持续自我迭代

---

## 第一课：Hello World

### 创建你的第一个 Agent

```python
from src.core.agent import Agent

# 创建 Agent 实例
my_agent = Agent("我的助手")

# 设置身份
my_agent.add_system_prompt("你是一个专业的投资顾问")

# 开始对话
response = my_agent.chat("今天A股怎么样？")
print(response)
```

---

## 第二课：记忆系统

### 分层记忆

OpenAgent 有三层记忆：

```python
# L1: 长期记忆 - 核心身份和目标
my_agent.add_system_prompt("你是投资专家，擅长分析A股和港股")

# L2: 中期记忆 - 当前任务
my_agent.set_task("帮用户分析今日股市")

# L3: 短期记忆 - 临时信息
my_agent.memory.add_short_term("用户持有10000元A股")
```

### 查看记忆

```python
# 获取精简上下文
context = my_agent.memory.get_compact_context()
print(context)
```

---

## 第三课：技能系统

### 使用内置技能

```python
# 读取文件
content = my_agent.execute_skill("read_file", "/path/to/file.txt")

# 执行命令
result = my_agent.execute_skill("execute_command", "ls -la")

# 写文件
my_agent.execute_skill("write_file", "/path/to/notes.txt", "内容...")
```

### 注册新技能

```python
from src.core.skills import SkillManager

skills = SkillManager()

# 定义技能
def my_custom_skill(arg1, arg2):
    return f"处理: {arg1} + {arg2}"

# 注册
skills.register(
    name="我的技能",
    description="处理两个参数",
    func=my_custom_skill,
    category="tools"
)

# 使用
result = skills.execute("我的技能", "参数1", "参数2")
```

---

## 第四课：股市分析

### 获取 A股 数据

```python
# 运行分析脚本
import subprocess
result = subprocess.run(
    ["python", "stock_full_analysis.py", "morning"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### 获取港股 数据

```python
result = subprocess.run(
    ["python", "hk_us_stock_analysis.py"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

---

## 第五课：构建你的投资助手

### 完整示例

```python
from src.core.agent import Agent

class 投资助手(Agent):
    def __init__(self):
        super().__init__("投资助手")
        self.add_system_prompt("""
            你是一个专业的投资助手。
            专长：A股分析、基金推荐、风险控制
            风格：稳健、保守、注重风险
        """)
    
    def 分析今日股市(self):
        """分析今日市场"""
        import subprocess
        result = subprocess.run(
            ["python", "stock_full_analysis.py", "morning"],
            capture_output=True,
            text=True,
            cwd="/root/.openclaw/workspace"
        )
        return result.stdout
    
    def 推荐基金(self, 本金=10000):
        """推荐基金"""
        return f"基于{本金}元本金，建议配置：\n- 指数ETF: 40%\n- 行业ETF: 30%\n- 现金: 30%"

# 使用
助手 = 投资助手()
print(助手.推荐基金(10000))
```

---

## 练习题

1. 创建一个天气查询 Agent
2. 添加一个计算技能
3. 制作你的专属投资助手

---

## 下一步

- 添加更多技能
- 连接真实 AI API
- 实现自动化交易

有问题随时问我！
