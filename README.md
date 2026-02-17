# openagent

> 🤖 一个可迭代的 Agent 框架，专注高效上下文管理和安全密钥处理

## 核心特性

- 🧠 **分级记忆系统** - 长期/中期/短期分层管理，避免上下文爆炸
- 🔐 **密钥安全管理** - 环境变量分离，不提交密钥到仓库
- 🛠️ **模块化工具** - 易于扩展的工具集
- 🔄 **可迭代架构** - 支持持续升级和能力增强

## 快速开始

```bash
# 克隆项目
git clone https://github.com/aden1350/openagent.git
cd openagent

# 复制环境配置模板
cp .env.example .env.local

# 编辑你的密钥
vim .env.local

# 安装依赖
pip install -r requirements.txt

# 运行
python -m src.main
```

## 架构

```
openagent/
├── src/
│   ├── core/           # 核心引擎
│   │   ├── agent.py    # Agent主逻辑
│   │   ├── memory.py   # 分级记忆系统
│   │   └── skills.py   # 技能管理
│   ├── tools/          # 工具集
│   └── config/         # 配置管理
├── .env.example        # 环境变量模板 (公开)
├── .gitignore          # 忽略密钥文件
└── requirements.txt     # 依赖
```

## 密钥管理

| 文件 | 作用 | 是否上传到Git |
|------|------|--------------|
| `.env.example` | 配置模板 | ✅ |
| `.env.local` | 你的密钥 | ❌ |

## License

MIT
