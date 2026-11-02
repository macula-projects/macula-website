---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "a0178da198a79cbbf66f7b9354d2c8711703e81e"
source_paths: ["macula-boot-examples/README.md", "macula-boot-examples/docker/README.md", "macula-boot-examples/docker/scripts/compose.sh", "macula-boot-examples/docker/.env.example", "macula-boot-examples/docker/docker-compose.yml", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-archetype/README.md", "macula-boot-archetype/pom.xml", "macula-boot-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml", "macula-boot-archetype/src/main/resources/archetype-resources/README.md", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-parent/pom.xml"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-examples/README.md", "macula-boot-examples/docker/README.md", "macula-boot-examples/docker/scripts/compose.sh", "macula-boot-examples/docker/.env.example", "macula-boot-examples/docker/docker-compose.yml", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-archetype/README.md", "macula-boot-archetype/pom.xml", "macula-boot-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml", "macula-boot-archetype/src/main/resources/archetype-resources/README.md", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-parent/pom.xml"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["deploy/README.md", "deploy/scripts/compose.sh", "deploy/.env.example"]}]
---

准备好 Git 和 Docker Compose v2，按下面两步启动平台与 Alibaba 示例链路。

## 1. 下载并启动 Macula Cloud

```bash
git clone https://github.com/macula-projects/macula-cloud.git
cd macula-cloud
cp deploy/.env.example deploy/.env
./deploy/scripts/compose.sh up-apps
```

启动完成后，访问管理端 `http://127.0.0.1:5900/`。平台提供 IAM 登录认证、用户、菜单和权限管理；本机端口等配置可在 `deploy/.env` 中调整。

## 2. 下载 Macula Boot，启动 Examples

回到上一级目录，下载框架并启动示例：

```bash
cd ..
git clone https://github.com/macula-projects/macula-boot.git
cd macula-boot/macula-boot-examples/docker
cp .env.example .env
./scripts/compose.sh up-apps alibaba
```

该命令启动示例所需的中间件，并依次启动 Provider、Consumer、Gateway。示例网关通过 `.env` 中的 `MACULA_CLOUD_IAM_URL` 连接第一步的 IAM，默认适用于同机部署。

通过网关调用回声接口，验证整条链路：

```bash
curl "http://127.0.0.1:5000/consumer/api/v1/consumer/echo/demo?str=hello"
```

这个演示接口已配置免认证，用于先验证服务调用是否连通。

## 三个关键模块

`请求 → Gateway → Consumer（BFF）→ Provider（Service）`

| 模块 | 职责与关键配置 |
| --- | --- |
| Gateway（`alibaba-gateway`） | 统一路由入口，验证 IAM Token，并向下游传递内部 JWT；配置 IAM introspection 地址。 |
| Consumer（`alibaba-consumer`，BFF） | 聚合前端接口，通过 Feign 调用 Provider；获取平台菜单、用户信息时，配置指向 Macula Cloud 网关的 `macula.cloud.endpoint` 和应用凭据。 |
| Provider（`alibaba-provider1`，Service） | 提供业务接口，实现具体业务逻辑。Consumer 与 Provider 均通过 `jwk-set-uri` 配置示例网关的 `/oauth2/jwks`，验证内部 JWT。 |

模块目录均位于 `macula-boot-examples/` 下，完整名称以 `macula-example-` 开头。IDE 启动和更多示例见 [Examples README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-examples)。

## 3. 用 Archetype 创建自己的项目

跑通示例后，可用 Archetype 生成包含 Gateway、Admin BFF、Service1、API 契约和 Admin 前端等模块的单仓项目。需要 Java 17 和 Maven 3.9+。

在前面下载的 **macula-boot 仓库根目录**安装当前模板，再回到仓库外生成项目；输出目录 `demo-app` 应尚不存在：

```bash
mvn -pl macula-boot-archetype -am install -DskipTests -Dgpg.skip=true -Pdeploy
cd ..
mvn archetype:generate \
  -DarchetypeGroupId=dev.macula.boot \
  -DarchetypeArtifactId=macula-boot-archetype \
  -DarchetypeVersion=6.1.0-SNAPSHOT \
  -DgroupId=com.example \
  -DartifactId=demo-app \
  -Dpackage=com.example.demo \
  -Dversion=1.0.0-SNAPSHOT \
  -Dgitignore=.gitignore \
  -DinteractiveMode=false
```

将 `groupId`、`package` 和 `artifactId` 换成自己的组织、包名与项目名；`version` 是业务项目版本，`archetypeVersion` 是模板版本，两者独立。

生成后进入 `demo-app/`，按其中的 `deploy/README.md` 配置 Macula Cloud 应用与 OAuth Client，再运行项目。模板参数见 [Archetype README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-archetype)，业务开发见[开发指引](/docs/latest/04_devmanual/)，认证配置见[安全架构](/docs/latest/00_introduce/安全架构/)。
