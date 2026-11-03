---
title: "平台概述"
linkTitle: "平台概述"
weight: 1
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["README.md", "pom.xml", "macula-boot-parent/pom.xml"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["README.md"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["README.md"]}]
---

Macula 是面向 Java 业务应用的模块化微服务开发平台。它将通用技术组件、统一身份与权限等平台服务，以及业务应用的参考工程组合起来，帮助团队统一基础能力，把主要开发工作放在业务上。

## 平台组成

| 组成 | 职责 | 使用方式 |
| --- | --- | --- |
| **Macula Boot** | 统一依赖、自动配置及 Web、安全、数据访问、消息等组件 | 在应用中按需引入 Parent 和 Starter |
| **Macula Cloud** | 提供 IAM、应用、用户、角色、菜单及 ID、调度等平台服务 | 按需部署，通过协议或客户端组件接入 |
| **Macula Samples** | 展示业务应用的模块组织、配置及完整调用链 | 作为业务开发参考，或使用 Archetype 创建自己的项目 |

Cloud 的管理端位于同仓的 `macula-cloud-admin`，用于管理平台身份、应用和权限。业务应用可以拥有自己的管理前端和 BFF，通过 Cloud 复用公共平台能力。

Boot 支持按需组合组件；只使用部分技术 Starter 时，不要求部署完整 Cloud。需要统一登录、菜单和平台权限等能力时，再接入相应平台服务。

## 业务开发边界

Macula 提供技术基础和平台公共服务。业务团队仍需定义领域模型、业务规则、接口契约、数据范围与页面，并负责测试和部署验证。

业务应用通常由前端、应用 Gateway、BFF 和业务服务协作完成请求。模块职责与 Cloud 的连接关系见[应用架构](/docs/latest/00_introduce/应用架构/)；代码和对象如何分层见[应用分层](/docs/latest/00_introduce/值对象与分层/)。

## 核心能力

| 分类 | Starter | 能力 |
| --- | --- | --- |
| 基础 | `commons`、`async`、`mapstruct` | 通用模型与异常、异步上下文传递、对象转换 |
| Web 与安全 | `web`、`security`、`feign`、`springdoc`、`crypto` | Web 自动配置、认证鉴权、服务调用、OpenAPI、加解密 |
| 数据访问 | `mybatis-plus`、`jpa`、`redis`、`cache` | 关系型数据库访问、Redis 与多级缓存 |
| 分布式能力 | `lock4j`、`idempotent`、`leaderelection`、`seata`、`springretry` | 分布式锁、幂等、Leader 选举、事务与重试 |
| 消息与任务 | `rocketmq`、`kafka`、`sender`、`task` | 消息队列、可靠消息、任务调度 |
| 云原生 | `cloud-gateway`、`cloud-alibaba`、`cloud-tencent` | 网关、Nacos/Sentinel、Polaris 等服务治理能力 |
| 可观测性 | `observability`、`auditlog`、`operationlog` | 统一 OTLP 指标、链路与日志，以及业务审计和操作日志 |
| 业务集成 | `oss`、`tinyid`、`binlog4j`、`websocket`、`wechat` | 对象存储、ID、Binlog、WebSocket、微信生态 |

完整模块位于 [`macula-boot-starters`](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-starters)，每个主要 Starter 的目录中均提供独立 README 和配置示例。
统一可观测性接入见 [`macula-boot-starter-observability`](/docs/latest/01_services/生产准备/observability/)，
从 5.x 迁移请参考[从 5.x 迁移到 latest 的升级指南](/docs/latest/05_ops/升级指南/)。

## 适用场景

适合需要复用身份与权限管理、统一 Java 技术栈，同时允许各业务按需组合组件的团队。已有 Spring 应用可以选择独立 Starter；新业务可从 Samples 或 Archetype 建立工程。

对于单一、简单的服务，应先评估实际边界和运维成本，不必为了套用模板而拆出全部微服务模块。应用架构是可组合的参考，不要求每个项目采用相同部署规模。

## 依赖基线

latest 跟随 Macula Boot main，当前版本为 **6.1.0-SNAPSHOT**，基于 Java 17、Spring Boot 4.0 和 Spring Cloud 2025.1。latest 是开发快照；正式版本以[变更历史](/docs/latest/11_about/更新日志/)及 GitHub Releases 为准，6.0 系列不建议使用。

业务项目优先继承 Macula Boot Parent，再按需选择 Starter，由 Parent 管理版本与构建约定。已有其他 Parent 的项目需要显式管理 Macula 制品及第三方依赖，不能只填一个版本号。具体 POM 示例见[快速开始 → 依赖接入](/docs/latest/00_introduce/快速开始/#依赖接入)。

## 技术架构

平台组成与请求链路的主图统一放在[应用架构](/docs/latest/00_introduce/应用架构/)；身份与权限的原理图见[安全架构](/docs/latest/00_introduce/安全架构/)。先通过[快速开始](/docs/latest/00_introduce/快速开始/)跑通示例，再按需要阅读这两部分原理。

实际创建、接入和修改业务应用，按[开发指引](/docs/latest/04_devmanual/)操作；框架源码构建、测试与贡献要求见[贡献规范](/docs/latest/11_about/贡献规范/)。

## License

Macula Boot 基于 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/LICENSE) 开源。
