---
title: "开发指引"
linkTitle: "开发指引"
weight: 5
manual_content: true
source_repository: "https://github.com/macula-projects/macula-samples"
source_branch: "main"
source_commit: "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e"
source_paths: ["README.md", "pom.xml", "deploy/README.md"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["README.md", "pom.xml", "deploy/README.md"]}]
---

本章以 [Macula Samples 单仓项目](https://github.com/macula-projects/macula-samples)为主线，介绍真实业务应用的模块划分、配置、开发和运行方式。框架的轻量接入示例放在[快速开始](/docs/latest/00_introduce/快速开始/)。

建议按以下顺序阅读：

1. [开发环境准备](/docs/latest/04_devmanual/开发环境准备/)：工具、外部平台和本地基础设施。
2. [获取与组织项目](/docs/latest/04_devmanual/创建应用平台/)：单仓目录结构与模块依赖。
3. [模块说明](/docs/latest/04_devmanual/模块说明/)：Gateway、BFF、业务服务、API 契约与管理端。
4. [配置规范](/docs/latest/04_devmanual/应用配置/)：application.yml、profile、Nacos 和认证地址。
5. [开发业务服务](/docs/latest/04_devmanual/创建服务模块/)：以 Service1 的应用管理接口串联各层。
6. [运行与测试](/docs/latest/04_devmanual/运行与测试/)及[打包部署](/docs/latest/04_devmanual/打包部署/)。

各模块在同一仓库内协作，后端由根 POM 聚合构建，前端在 Admin 目录构建。也支持多仓模式，可参考 [macula-samples-workspace](https://cnb.cool/macula-projects/macula-samples-workspace)。
