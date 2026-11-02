---
title: "部署 Macula Cloud"
linkTitle: "部署 Macula Cloud"
weight: 2
manual_content: true
source_repository: "https://github.com/macula-projects/macula-cloud"
source_branch: "main"
source_commit: "7d5404146483d7ccbce5e95411fe9c1e5de361a6"
source_paths: ["deploy/README.md", "macula-cloud-admin/README.md"]
---

## 代码与运行方式

Macula Cloud 后端和管理端共用一个仓库，管理端位于 `macula-cloud-admin/`。本页根据当前仓库的本地部署说明整理；完整配置、端口与排错步骤见[部署 README](https://github.com/macula-projects/macula-cloud/blob/7d5404146483d7ccbce5e95411fe9c1e5de361a6/deploy/README.md)。

```bash
git clone https://github.com/macula-projects/macula-cloud.git
cd macula-cloud
cp deploy/.env.example deploy/.env
```

按本机环境修改 `deploy/.env`。开发编排用于本地开发与集成验证；共享或生产环境需要另行配置凭据、证书、备份和高可用。

## 方式一：IDE 调试

先启动中间件和初始化任务：

```bash
./deploy/scripts/compose.sh config
./deploy/scripts/compose.sh up
./deploy/scripts/compose.sh status
```

后端需要 Java 17 与 Maven。按部署 README 完成数据库迁移和 IDE 启动配置，再启动 IAM、Gateway、System 等所需服务。

管理端使用推荐的 Node.js 24 LTS，在同一仓库内运行：

```bash
cd macula-cloud-admin
npm ci
npm run dev
```

## 方式二：完整容器

使用 Docker Compose v2，并在 `deploy/.env` 中提供当前部署说明要求的配置，再启用 `apps` profile：

```bash
./deploy/scripts/compose.sh config-apps
./deploy/scripts/compose.sh up-apps
./deploy/scripts/compose.sh status
```

该模式包含后端应用与 Admin。默认管理端地址为 `http://127.0.0.1:5900/`，可通过环境配置调整端口。

## 配置与更新

后端使用 `application.yml` 和环境 profile；共享环境的配置按当前 Data ID 规则放入 Nacos。数据库使用 Flyway 管理，启动顺序、服务地址和持久化卷处理以部署 README 为准。

管理端通过 `/api` 访问 Gateway。IAM 可直连，也可按部署方式配置代理；直连时需要为对应 OAuth Client 配置精确的管理端 Origin。配置说明见[管理端 README](https://github.com/macula-projects/macula-cloud/blob/7d5404146483d7ccbce5e95411fe9c1e5de361a6/macula-cloud-admin/README.md)。
