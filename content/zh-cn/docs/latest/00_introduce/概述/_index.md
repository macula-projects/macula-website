---
title: "概述"
linkTitle: "概述"
weight: 1
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["README.md", "pom.xml", "macula-boot-parent/pom.xml"]}]
---

<h2 align="center">Macula Boot</h2>

<p align="center">
  <strong>基于 Spring Boot 与 Spring Cloud 的模块化微服务开发框架</strong>
</p>

<p align="center">
  <a href="https://github.com/macula-projects/macula-boot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/macula-projects/macula-boot.svg" alt="License">
  </a>
  <a href="https://github.com/macula-projects/macula-boot/actions/workflows/verification.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/macula-projects/macula-boot/verification.yml?branch=main&label=verification&logo=github" alt="Verification">
  </a>
  <a href="https://central.sonatype.com/search?q=g%3Adev.macula.boot">
    <img src="https://img.shields.io/maven-central/v/dev.macula.boot/macula-boot-parent" alt="Maven Central">
  </a>
  <img src="https://img.shields.io/badge/JDK-17+-green.svg" alt="JDK 17+">
  <img src="https://img.shields.io/badge/Spring%20Boot-4.0-green.svg" alt="Spring Boot 4.0">
  <img src="https://img.shields.io/badge/Spring%20Cloud-2025.1-green.svg" alt="Spring Cloud 2025.1">
</p>

Macula Boot 面向 Java 微服务应用提供统一的依赖管理、自动配置和基础能力 Starter。项目同时支持 Spring Cloud Alibaba、Spring Cloud Tencent 等技术体系，业务项目可以按需引入模块，不必绑定完整平台。

> Macula Boot 是 Macula 微服务平台的开发框架部分。通用技术服务参见 [Macula Cloud](https://github.com/macula-projects/macula-cloud)，管理端参见 [Macula Cloud Admin](https://github.com/macula-projects/macula-cloud/tree/main/macula-cloud-admin)。

网关入口认证、内部 JWT 与方法 / 数据授权的分层关系，见[安全架构](/docs/latest/00_introduce/安全架构/)。

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

## 平台边界

Macula Boot 提供可组合的开发组件；Macula Cloud 提供 IAM、用户、角色、菜单与平台管理服务，管理端位于同仓的 `macula-cloud-admin`；Macula Samples 是基于二者的业务应用示例。业务前端通过应用 Gateway 访问 BFF，BFF 编排业务服务。

## 依赖基线

latest 跟随 main，当前框架版本为 **6.1.0-SNAPSHOT**（开发快照），基于 Java 17、Spring Boot 4.0 和 Spring Cloud 2025.1。正式发行版本以[变更历史](/docs/latest/11_about/更新日志/)及 GitHub Releases 为准，6.0 系列不建议使用。

业务项目先继承 Parent，再选择 Starter，Parent 已管理组件版本：

```xml
<parent>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-parent</artifactId>
    <version>6.1.0-SNAPSHOT</version>
    <relativePath/>
</parent>
```

快照尚未发布或远程无法解析时，先在 **Macula Boot 源码根目录**安装完整框架及模板，然后构建业务项目：

```bash
mvn clean install -DskipTests=true -Dgpg.skip=true -Pdeploy
```

该命令跳过测试，只用于本地制品准备，不代表框架验证通过。只安装 `macula-boot-archetype` 不会同时安装所有 Starter。

已有其他 Parent 的项目，可在自己的 POM 中定义版本，并为所选 Macula 依赖显式填写 `<version>${macula.version}</version>`：

```xml
<properties>
    <macula.version>6.1.0-SNAPSHOT</macula.version>
</properties>
```

这只是 Macula 制品版本声明；还需按对应 Parent 的 dependencyManagement 管理 Spring 与第三方依赖，避免混用不同 Boot/Cloud 主线。新项目优先用 Archetype 生成完整 Parent 配置。

[快速开始](/docs/latest/00_introduce/快速开始/)提供启动与项目生成步骤；[首次接入](/docs/latest/04_devmanual/首次接入macula-cloud/)说明应用和 OAuth Client 注册；[贡献规范](/docs/latest/11_about/贡献规范/)保留框架源码构建、测试和代码规范。

## 技术架构

![Macula 技术架构](https://macula.dev/docs/00_introduce/%E6%A6%82%E8%BF%B0/images/macula-tech-diagram.png)

Macula Boot 特别适合拥有多条产品线、希望统一技术栈和基础组件，同时允许业务按需组合能力的研发团队。

## License

Macula Boot 基于 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/LICENSE) 开源。
