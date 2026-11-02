---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
manual_content: true
source_repository: "https://github.com/macula-projects/macula-cloud"
source_branch: "main"
source_commit: "7d5404146483d7ccbce5e95411fe9c1e5de361a6"
source_paths: ["deploy/README.md", "macula-cloud-admin/README.md", "macula-cloud-admin/package.json"]
---

## 从开发框架开始

Macula Boot 为业务应用提供 Parent、Commons 和按需组合的 Starter。应用创建与依赖选择见[创建应用平台](/docs/latest/04_devmanual/创建应用平台/)，组件清单见[平台能力](/docs/latest/01_services/)。

## 获取 Macula Cloud 与管理端

Macula Cloud 的后端服务和 Vue 管理端在同一仓库维护，管理端目录为 `macula-cloud-admin/`。

```bash
git clone https://github.com/macula-projects/macula-cloud.git
cd macula-cloud
```

| 开发工具 | 要求 |
| --- | --- |
| 后端 | Java 17、Maven |
| 管理端 | 推荐 Node.js 24 LTS，最低支持 Node.js 22.12 |
| 本地容器环境 | Docker Compose v2 |

## 启动本地平台

本地环境支持 IDE 调试和完整容器两种方式。中间件、数据库迁移、服务启动顺序及必填配置见[部署 Macula 平台](/docs/latest/04_devmanual/部署macula平台/)。

在 IDE 模式下启动后端后，可在仓库的管理端目录运行：

```bash
cd macula-cloud-admin
npm ci
npm run dev
```

Vite 开发服务通过 `/api` 代理访问 Gateway，IAM 地址由管理端配置提供。实际页面地址以终端输出为准；认证接入及本地配置以[当前管理端 README](https://github.com/macula-projects/macula-cloud/blob/7d5404146483d7ccbce5e95411fe9c1e5de361a6/macula-cloud-admin/README.md) 为准。

## 接入业务应用

通过 [Examples](/docs/latest/04_devmanual/运行与测试/) 了解服务、网关与 Starter 的组合方式，并在 Macula Cloud 中维护业务所需的接入应用、菜单和权限。

已有应用升级请阅读[从 6.0.x 迁移到 latest](/docs/latest/05_ops/升级指南/)。
