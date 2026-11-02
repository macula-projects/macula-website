---
title: "服务创建"
linkTitle: "服务创建"
weight: 1
manual_content: true
---

## 准备可交付制品

新项目用[快速开始的 Archetype](/docs/latest/00_introduce/快速开始/#3-用-archetype-创建自己的项目)生成，现有项目参考[创建服务模块](/docs/latest/04_devmanual/创建服务模块/)。首次使用 latest 快照先安装完整 Boot 框架，生成模板不等于所有依赖已安装。

发布前固定源码提交、框架版本、构建 profile、API 契约及数据库迁移版本。在业务单仓根目录构建：

```bash
mvn clean verify -Pprd -Dgpg.skip=true
```

该命令会执行单元与集成测试，需先按[运行与测试](/docs/latest/04_devmanual/运行与测试/)准备外部依赖；缺少环境时不得将跳过集成测试标为验证通过。Admin 在其目录执行 `npm ci` 与 `npm run build`；前端构建环境按 Vite 配置选择，不使用 Maven profile 推断。

检查目标模块的可运行 JAR、镜像构建文件及前端 dist。镜像使用不可变标签或 digest，与源码提交建立对应关系；不要部署 `latest` 可变标签来代替发布记录。后续按[服务配置](/docs/latest/05_ops/服务配置/)注入环境，按[服务部署](/docs/latest/05_ops/服务部署/)验证和回滚。
