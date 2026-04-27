# AI+Campus 校园智能服务助手

<p align="center">
  <strong>AI+Campus</strong> - 基于大语言模型的校园智能服务助手
</p>

---

## 项目简介

AI+Campus 是一款面向高校校园场景的智能服务助手，基于大语言模型（LLM）和 RAG（检索增强生成）技术，为师生提供全方位的校园服务。系统采用 **1+5 架构**：1个AI对话引擎 + 5大核心功能模块，用户通过自然语言对话即可访问所有服务。

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.11+)
- **数据库**: PostgreSQL 15 (异步 SQLAlchemy)
- **缓存**: Redis 7
- **AI 引擎**: LangChain + 通义千问 (DashScope)
- **向量数据库**: ChromaDB
- **认证**: JWT (python-jose + passlib)
- **数据库迁移**: Alembic

### 前端
- **框架**: Vue 3 + Composition API
- **UI 组件库**: Vant 4 (移动端)
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite 5
- **HTTP 客户端**: Axios

### 部署
- **容器化**: Docker + Docker Compose
- **Web 服务器**: Nginx
- **CI/CD**: GitHub Actions

## 项目结构

```
ai-campus/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── ai/                 # AI 引擎（LangChain、RAG、Agent）
│   │   │   ├── engine.py       # AI引擎核心（通义千问 LLM 封装）
│   │   │   ├── prompts.py      # Agent系统提示词（主路由 + 5子Agent）
│   │   │   ├── agents.py       # 多Agent调度器（意图识别 + 路由）
│   │   │   ├── rag.py          # ChromaDB 向量检索
│   │   │   └── tools.py        # Agent工具函数
│   │   ├── api/v1/             # API 路由（11个模块）
│   │   │   ├── auth.py         # 认证接口
│   │   │   ├── chat.py         # AI对话接口（核心）
│   │   │   ├── academic.py     # 学业助手
│   │   │   ├── campus_info.py  # 校园信息
│   │   │   ├── daily_service.py# 日常服务
│   │   │   ├── community.py    # 社区互动
│   │   │   └── mental_health.py# 心理健康
│   │   ├── core/               # 核心配置（数据库、Redis、安全）
│   │   ├── models/             # SQLAlchemy 数据模型（7张表）
│   │   ├── schemas/            # Pydantic 请求/响应模型
│   │   ├── services/           # 业务逻辑层（10个服务）
│   │   └── utils/              # 工具函数
│   ├── alembic/                # 数据库迁移
│   ├── main.py                 # 应用入口
│   ├── requirements.txt        # Python 依赖
│   └── pyproject.toml          # 项目配置
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/                # API 请求封装（8个模块）
│   │   ├── components/         # Vue 组件（8个）
│   │   ├── router/             # 路由配置（14条路由）
│   │   ├── stores/             # Pinia 状态管理
│   │   ├── styles/             # 全局样式（CSS变量主题）
│   │   ├── utils/              # 工具函数
│   │   └── views/              # 页面视图（13个页面）
│   ├── package.json
│   └── vite.config.js
├── docker/                     # Docker 配置
│   ├── Dockerfile.backend      # 后端镜像
│   ├── Dockerfile.frontend     # 前端镜像（多阶段构建）
│   ├── docker-compose.yml      # 编排配置（4个服务）
│   └── nginx.conf              # Nginx 反向代理
├── data/                       # 数据目录
│   ├── documents/              # 文档数据
│   └── knowledge/              # 知识库数据
├── tests/                      # 测试文件
├── docs/                       # 项目文档
├── .github/workflows/          # CI/CD 配置
├── .gitignore
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (可选，用于容器化部署)

### 本地开发

#### 1. 克隆项目

```bash
git clone https://github.com/ZJ010700/ai-campus.git
cd ai-campus
```

#### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库、Redis、API Key 等配置

# 数据库迁移
alembic upgrade head

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后可访问：
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

#### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后可访问: http://localhost:5173

### Docker 部署

#### 1. 配置环境变量

```bash
# 复制后端环境变量配置
cp backend/.env.example backend/.env

# 编辑 backend/.env，配置以下关键变量：
# - DATABASE_URL（Docker 环境下使用默认值即可）
# - REDIS_URL（Docker 环境下使用默认值即可）
# - DASHSCOPE_API_KEY（通义千问 API Key，必填）
# - JWT_SECRET_KEY（生产环境请使用强密钥）
```

#### 2. 启动服务

```bash
# 在项目根目录执行
cd docker
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f backend
docker compose logs -f frontend
```

#### 3. 数据库迁移（首次部署）

```bash
docker compose exec backend alembic upgrade head
```

#### 4. 停止服务

```bash
docker compose down

# 停止并清除数据卷（谨慎使用）
docker compose down -v
```

部署成功后可访问：
- 前端页面: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `APP_NAME` | 应用名称 | `AI+Campus` | 否 |
| `APP_ENV` | 运行环境 | `development` | 否 |
| `DEBUG` | 调试模式 | `true` | 否 |
| `DATABASE_URL` | PostgreSQL 连接串 | `postgresql+asyncpg://postgres:postgres@localhost:5432/ai_campus` | 是 |
| `REDIS_URL` | Redis 连接串 | `redis://localhost:6379/0` | 是 |
| `JWT_SECRET_KEY` | JWT 签名密钥 | - | 是 |
| `JWT_ALGORITHM` | JWT 算法 | `HS256` | 否 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token 过期时间（分钟） | `30` | 否 |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh Token 过期时间（天） | `7` | 否 |
| `DASHSCOPE_API_KEY` | 通义千问 API Key | - | 是 |
| `DASHSCOPE_MODEL` | 使用的模型 | `qwen-plus` | 否 |
| `CORS_ORIGINS` | 允许的跨域来源 | `http://localhost:3000,http://localhost:5173` | 否 |
| `LOG_LEVEL` | 日志级别 | `DEBUG` | 否 |
| `UPLOAD_DIR` | 文件上传目录 | `./uploads` | 否 |
| `MAX_UPLOAD_SIZE` | 最大上传大小（字节） | `10485760` (10MB) | 否 |

## API 文档

后端启动后，可访问以下文档地址：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API 模块

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| 认证 | `/api/v1/auth` | 注册、登录、刷新令牌、登出 |
| 用户管理 | `/api/v1/users` | 个人信息、更新信息、修改密码 |
| AI 对话 | `/api/v1/chat` | 发送消息、对话历史、流式响应 |
| 学业助手 | `/api/v1/academic` | 课程查询、选课推荐、课程表、考试安排、成绩查询 |
| 校园信息 | `/api/v1/campus` | 公告、活动、通知、搜索、日历 |
| 日常服务 | `/api/v1/daily` | 食堂菜单、图书馆座位、图书搜索、报修、天气、校车 |
| 社区 | `/api/v1/community` | 发布帖子、帖子列表、二手交易、拼车、失物招领 |
| 心理健康 | `/api/v1/mental-health` | 心理对话、心理评估、心理资源、每日贴士 |
| 反馈 | `/api/v1/feedback` | 提交反馈、反馈列表、反馈统计 |

## 功能模块说明

### 1. AI 对话引擎（1+5 多Agent架构）
- 基于 LangChain + 通义千问的智能对话
- 主路由 Agent：意图识别，自动分发到子 Agent
- 5 个功能子 Agent：学业助手、校园信息、日常服务、社区、心理健康
- RAG 检索增强生成，结合校园知识库（ChromaDB）
- 流式响应（SSE），打字机效果

### 2. 智能学业助手 (P0)
- 课程信息查询与智能推荐
- 课程表管理与考试安排
- 成绩查询与分析
- 学习计划与学业规划建议

### 3. 校园信息中心 (P0)
- 校园公告与通知推送
- 校园活动日历
- 信息搜索与聚合
- 自然语言查询

### 4. 日常服务助手 (P1)
- 食堂菜单查询
- 图书馆座位预约与图书检索
- 校园报修服务
- 天气查询与校车时刻表

### 5. 校园社区平台 (P1)
- 帖子发布与浏览
- 二手交易
- 拼车信息
- 失物招领

### 6. AI 心理伙伴 (P2)
- AI 心理对话与情绪倾听
- 心理评估问卷
- 心理资源推荐
- 每日心理贴士

## 文档

- [系统架构图](docs/AI+Campus系统架构图.png)
- [用例图](docs/AI+Campus用例图.png)
- [ER图](docs/AI+Campus%20ER图.png)
- [时序图](docs/AI+Campus时序图.png)
- [Agent系统提示词集](docs/AI+Campus_Agent系统提示词集.docx)
- [项目方案](docs/AI+Campus校园智能服务助手项目方案.docx)

## License

MIT License