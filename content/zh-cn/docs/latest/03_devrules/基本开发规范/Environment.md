---
title: "环境管理"
linkTitle: "环境管理"
weight: 1
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "dcd7fd36ee55ea43e17958264d0c6609455bb114", "paths": ["content/zh-cn/docs/latest/03_devrules/基本开发规范/Environment.md"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["pom.xml", "macula-samples-parent/pom.xml"]}]
---

Samples 当前 Maven profiles 为 `local`（默认）、`dev`、`stg`、`pet`、`prd`；`test` 可作为团队环境名称，但不是当前工程预置的 Maven profile。`docker` 为 Spring profile，复用 local 并覆盖地址。业务配置按 Nacos namespace 与 Data ID 隔离，详见[应用配置](/docs/latest/04_devmanual/应用配置/)。

## 概述

每套系统都需要经过开发、测试、预发等环节才能够上线，所以这里定义一套标准的环境命名规则。

## 环境命名

| 环境名称 | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| local    | 本地环境，默认的开发人员本地的环境                           |
| dev      | 开发环境，用于开发阶段的部署                                 |
| test     | 测试环境，开发提测后测试人员进行测试的环境（有时会和dev公共，减少部署） |
| stg      | 准生产环境，开发阶段测试完成后需要发版前的回归测试环境，代码与生产一致 |
| pet      | 压测环境，用于性能测试                                       |
| prd      | 生产环境                                                     |
