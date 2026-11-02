---
title: "开发指引"
linkTitle: "开发指引"
weight: 5
manual_content: true
source_repository: "https://cnb.cool/macula-projects/macula-samples-workspace"
source_branch: "main"
source_commit: "f4624d4d4ebb87e7240c04f24b3cdb29ad46702a"
source_paths: ["README.md", "pom.xml", "deploy/README.md"]
source_refs: [{"repository": "https://cnb.cool/macula-projects/macula-samples-workspace", "branch": "main", "commit": "f4624d4d4ebb87e7240c04f24b3cdb29ad46702a", "paths": ["README.md", "pom.xml", "deploy/README.md"]}]
---

本章以 **Macula Samples** 的已提交源码为例，介绍真实业务应用的模块划分、配置、开发和运行方式。框架的轻量接入示例放在[快速开始](/docs/latest/00_introduce/快速开始/)。

建议按以下顺序阅读：

1. [开发环境准备](/docs/latest/04_devmanual/开发环境准备/)：工具、外部平台和本地基础设施。
2. [获取与组织项目](/docs/latest/04_devmanual/创建应用平台/)：聚合工作区和独立模块仓库。
3. [模块说明](/docs/latest/04_devmanual/模块说明/)：Gateway、BFF、业务服务、API 契约与管理端。
4. [配置规范](/docs/latest/04_devmanual/应用配置/)：application.yml、profile、Nacos 和认证地址。
5. [开发业务服务](/docs/latest/04_devmanual/创建服务模块/)：以 Service1 的应用管理接口串联各层。
6. [运行与测试](/docs/latest/04_devmanual/运行与测试/)及[打包部署](/docs/latest/04_devmanual/打包部署/)。

源码入口：[macula-samples-workspace](https://cnb.cool/macula-projects/macula-samples-workspace)。各页记录对应仓库、提交和文件路径；工作区中尚未提交的业务扩展不作为这里的源码依据。
