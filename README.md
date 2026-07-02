# PM汪需求分析工具

一款面向产品经理的 C 端消费者需求分析工具，基于六部分方法论（Who → Scene → Job → Pain → Insight → Opportunity）进行结构化分析，最终输出完整的需求文档。

## 功能特性

- 📊 **结构化分析**：按照 Who → Scene → Job → Pain → Insight → Opportunity 六部分方法论进行分析
- 🤖 **AI 辅助调研**：集成 AI 能力，辅助生成用户画像、场景、动机等内容
- 📝 **Markdown 导出**：一键导出完整的需求分析文档
- 📈 **完成度追踪**：实时查看各模块的完成状态
- 🎨 **现代 UI**：简洁优雅的界面设计，类似 Linear / Vercel 风格

## 技术栈

- **后端**：FastAPI + SQLAlchemy + SQLite
- **前端**：Jinja2 模板 + HTMX（无构建步骤）
- **AI**：兼容 OpenAI 格式的 API 接口

## 快速开始

```bash
# 安装依赖
pip install -e ".[dev]"

# 配置环境变量（复制 .env.example 为 .env 并填入你的配置）
cp .env.example .env

# 启动服务
uvicorn app.main:app --reload

# 访问 http://localhost:8000
```

## 环境变量配置

在项目根目录创建 `.env` 文件：

```bash
# AI API 配置（用于 AI 辅助调研功能）
AI_API_KEY=你的API密钥
AI_API_URL=https://your-api-endpoint.com/v1/chat/completions
AI_MODEL=你的模型名称
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `AI_API_KEY` | API 密钥 | 空（不配置则 AI 功能不可用） |
| `AI_API_URL` | API 地址 | `https://token-plan-cn.xiaomimimo.com/v1/chat/completions` |
| `AI_MODEL` | 模型名称 | `mimo-v2.5` |

> 💡 AI 辅助调研功能需要配置兼容 OpenAI 格式的 API。如果不配置，其他功能仍可正常使用。

## 项目结构

```
app/
├── main.py              # FastAPI 入口
├── config.py            # 配置
├── database.py          # 数据库
├── models/              # ORM 模型
├── routers/             # 路由
├── services/            # 业务逻辑
│   ├── validation.py    # 完成度校验
│   └── export.py        # Markdown 导出
├── templates/           # Jinja2 模板
└── static/              # 静态资源
```

## 分析方法论

| 模块 | 说明 |
|------|------|
| Who（用户） | 目标用户画像与分层 |
| Scene（场景） | 核心使用场景与行为路径 |
| Job（动机） | JTBD 用户任务与目标 |
| Pain（痛点） | 用户痛点、竞品分析、未满足需求 |
| Insight（洞察） | 从痛点提炼的关键判断 |
| Opportunity（机会） | 产品机会点、能力建议、MVP |

## License

MIT
