---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "a0178da198a79cbbf66f7b9354d2c8711703e81e"
source_paths: ["macula-boot-examples/README.md", "macula-boot-examples/docker/README.md", "macula-boot-examples/docker/scripts/compose.sh", "macula-boot-examples/docker/.env.example", "macula-boot-examples/docker/docker-compose.yml", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-archetype/README.md", "macula-boot-archetype/pom.xml", "macula-boot-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml", "macula-boot-archetype/src/main/resources/archetype-resources/README.md", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-parent/pom.xml"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-examples/README.md", "macula-boot-examples/docker/README.md", "macula-boot-examples/docker/scripts/compose.sh", "macula-boot-examples/docker/.env.example", "macula-boot-examples/docker/docker-compose.yml", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-archetype/README.md", "macula-boot-archetype/pom.xml", "macula-boot-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml", "macula-boot-archetype/src/main/resources/archetype-resources/README.md", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-parent/pom.xml", "macula-boot-starters/macula-boot-starter-web/pom.xml", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java", "macula-boot-parent/pom.xml"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["deploy/README.md", "deploy/scripts/compose.sh", "deploy/.env.example"]}]
---

本页主线验证 Cloud 与 Boot Examples 的协作；只接入独立 Starter 可直接看[依赖接入](#依赖接入)。准备好 Git 和 Docker Compose v2，按前两步启动平台与 Alibaba 示例链路；跑通后，可用 Archetype 创建自己的项目。

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

这个演示接口已配置免认证，用于先验证服务调用是否连通。成功时应在响应业务数据中看到传入的 `hello`；若只有容器启动、接口报错或找不到目标服务，尚未完成本步。登录与权限验证继续按[首次接入](/docs/latest/04_devmanual/首次接入macula-cloud/)执行。

## 三个关键模块

`请求 → Gateway → Consumer（BFF）→ Provider（Service）`

| 模块 | 职责与关键配置 |
| --- | --- |
| Gateway（`alibaba-gateway`） | 统一路由入口，验证 IAM Token，并向下游传递内部 JWT；配置 IAM introspection 地址。 |
| Consumer（`alibaba-consumer`，BFF） | 聚合前端接口，通过 Feign 调用 Provider；获取平台菜单、用户信息时，配置指向 Macula Cloud 网关的 `macula.cloud.endpoint` 和应用凭据。 |
| Provider（`alibaba-provider1`，Service） | 提供业务接口，实现具体业务逻辑。Consumer 与 Provider 均通过 `jwk-set-uri` 配置示例网关的 `/oauth2/jwks`，验证内部 JWT。 |

模块目录均位于 `macula-boot-examples/` 下，完整名称以 `macula-example-` 开头。IDE 启动和更多示例见 [Examples README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-examples)。

## 3. 用 Archetype 创建自己的项目

latest 使用开发快照。首次使用先在 Boot 根目录安装完整框架与模板，确保生成项目依赖的 Parent 和 Starter 都已进入本地 Maven 仓库。

跑通示例后，可用 Archetype 生成包含 Gateway、Admin BFF、Service1、API 契约和 Admin 前端等模块的单仓项目。需要 Java 17 和 Maven 3.9+。

前一步的终端仍位于 `macula-boot/macula-boot-examples/docker`，先执行 `cd ../..` 回到 **macula-boot 仓库根目录**。在该目录安装当前框架与模板，再回到仓库外生成项目；输出目录 `demo-app` 应尚不存在：

```bash
mvn clean install -DskipTests=true -Dgpg.skip=true -Pdeploy
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

生成后进入 `demo-app/`，按其中的 `deploy/README.md` 配置 Macula Cloud 应用与 OAuth Client，再运行项目。模板参数见 [Archetype README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-archetype)，业务开发见[开发指引](/docs/latest/04_devmanual/)，认证配置见[请求链路](/docs/latest/00_introduce/请求链路/)。

自己的应用还需在 Cloud 注册应用与 OAuth Client，按[首次接入 Macula Cloud](/docs/latest/04_devmanual/首次接入macula-cloud/)完成登录和受保护接口验证。

## 依赖接入

Archetype 已生成 Parent 配置；已有项目可按下面的 POM 示例接入。完整平台登记和业务开发步骤继续参见[开发指引](/docs/latest/04_devmanual/)。

优先继承 Macula Boot Parent，由其管理 Starter 版本及构建配置：

```xml
<parent>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-parent</artifactId>
    <version>6.1.0-SNAPSHOT</version>
    <relativePath/>
</parent>
```

已有其他 Parent 的项目，可显式定义 Macula 版本，并在所选依赖上填写版本；第三方依赖需另按目标 Parent 的 dependencyManagement 对齐：

```xml
<properties>
    <macula.version>6.1.0-SNAPSHOT</macula.version>
</properties>

<dependencies>
    <!-- 示例：只引入实际需要的组件 -->
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-web</artifactId>
        <version>${macula.version}</version>
    </dependency>
</dependencies>
```

仅导入依赖版本管理不会继承 Parent 的构建插件。新项目优先通过 Archetype 生成，已有项目按对应组件说明核对编译插件。快照无法远程解析时，使用前文的完整框架安装命令准备本地制品；跳过测试的安装不能作为验证结果。

### 只接入 Web Starter

最小 Servlet 应用可先只引入 Web Starter，不需要部署 Cloud。新建 `demo-web` 目录，使用以下 `pom.xml`；已有应用按前面的依赖接入方式调整即可。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-parent</artifactId>
        <version>6.1.0-SNAPSHOT</version>
        <relativePath/>
    </parent>
    <groupId>com.example</groupId>
    <artifactId>demo-web</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>dev.macula.boot</groupId>
            <artifactId>macula-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

创建 `src/main/java/com/example/demo/DemoApplication.java`：

```java
package com.example.demo;

import java.util.Map;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** 最小 Web 接入示例。 */
@SpringBootApplication
@RestController
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @GetMapping("/demo")
    public Map<String, String> demo() {
        return Map.of("message", "hello");
    }
}
```

在该应用根目录执行 `mvn spring-boot:run`，再访问 `curl http://127.0.0.1:8080/demo`。预期是统一 Result 响应，业务数据 `data.message` 为 `hello`。这是独立 Web 接入验证，不包含认证与分布式服务调用。无法解析快照时，先完成本页的框架安装；修改返回包装等行为见 [Web](/docs/latest/01_services/框架基础/web/)。
