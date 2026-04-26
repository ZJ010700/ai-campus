# AI+Campus 校园智能服务助手

> 基于大语言模型的校园一站式AI解决方案

## 项目简介

AI+Campus 是一款基于大模型技术的校园智能服务助手，采用 **1+5** 架构：1个AI对话引擎 + 5大核心功能模块。用户通过自然语言对话即可访问所有服务。

## 技术栈

| 层次 | 技术 |
|------|
| 前端 | Vue 3 + Vant 4 + Axios + Pinia |
| 后端 | Python FastAPI + SQLAlchemy + JWT |
| AI引擎 | LangChain + ChromaDB + 通义千问 API |
| 数据库 | PostgreSQL 15 + Redis 7 |
| 部署 | Docker + Nginx + GitHub Actions |

## 功能模块

- **智能学业助手 (P0)** - 选课推荐、考试日历、学业规划
- **校园信息中心 (P0)** - 信息聚合、智能推送、自然语言查询
- **日常服务助手 (P1)** - 食堂菜单、图书馆服务、报修服务
- **校园社区平台 (P1)** - 二手交易、拼车、失物招领
- **AI心理伙伴 (P2)** - 情绪倾听、压力管理、心理健康

## 项目结构

```
ai-campus/
├── frontend/          # Vue 3 前端
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── api/
│   │   ├── stores/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── ai/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── pyproject.toml
│   └── main.py
├── data/
│   ├── documents/
│   └── knowledge/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
├── docs/
└── .github/workflows/
```

## 文档

- [项目技术规格文档](docs/AI+Campus项目技术规格文档.md)
- [详细设计文档](docs/AI+Campus详细设计文档.md)
- [毕业设计论文初稿](docs/AI+Campus毕业设计论文初稿.md)
- [系统架构图](docs/AI+Campus系统架构图.png)
- [用例图](docs/AI+Campus用例图.png)
- [ER图](docs/AI+Campus%20ER图.png)
- [时序图](docs/AI+Campus时序图.png)

## License

MIT License