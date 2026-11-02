---
title: "Macula Boot Starter Cloud Tencent"
linkTitle: "Tencent"
weight: 20
manual_content: true
source_path: "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-tencent/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-tencent/README.md", "macula-boot-starters/macula-boot-starter-cloud/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-tencent-scg/pom.xml"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
---

## 概览

Tencent 接入面向 Java 17、Spring Boot 4 与 Spring Cloud 2025.1，提供 Polaris 配置、服务发现与 Feign 调用能力；业务服务与网关按角色选择对应 Starter。

基于[Spring Cloud Tencent](https://github.com/tencent/spring-cloud-tencent)
的微服务开源套件[Polarismesh](https://polarismesh.cn/)搭建微服务平台。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

业务服务选择 `macula-boot-starter-cloud-tencent`，网关选择 `macula-boot-starter-cloud-tencent-scg`。SCG 已组合共享 `macula-boot-starter-cloud-gateway`，无需重复引入。通常按项目选择 Tencent 或 Alibaba 一套云平台。

`macula-boot-starter-cloud` 是聚合 POM，不是启用全部云能力的运行时 Starter。以下子模块均使用 `dev.macula.boot` 坐标，版本由 Macula Boot Parent 管理；未采用统一版本管理时显式指定版本。

```xml
<!-- 微服务模块依赖 -->
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-tencent</artifactId>
</dependency>

        <!-- 网关模块依赖 -->
<dependency>
<groupId>dev.macula.boot</groupId>
<artifactId>macula-boot-starter-cloud-tencent-scg</artifactId>
</dependency>
```

## 使用配置

以下按当前 [Tencent Provider application.yml](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-examples/macula-example-tencent-provider/src/main/resources/application.yml) 精简；网关差异见 [Tencent Gateway application.yml](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-examples/macula-example-tencent-gateway/src/main/resources/application.yml)。

| 属性 | 示例值 / 说明 |
| --- | --- |
| `spring.config.import` | `optional:polaris`，通过 Config Data 导入配置 |
| `spring.profiles.group.docker` | `local`，Docker 复用本地默认配置 |
| `spring.cloud.polaris.config.enabled` / `auto-refresh` | 示例均为 `true`，启用配置中心和刷新 |
| `spring.cloud.polaris.config.groups[].name` | 应用名对应的配置组 |
| `spring.cloud.polaris.discovery.enabled` / `register` | 示例均为 `true`，启用发现和注册 |
| `spring.cloud.polaris.address` | local：`grpc://127.0.0.1:38091`；docker：`grpc://polaris:8091` |
| `spring.cloud.polaris.namespace` | `POLARIS_NAMESPACE`，示例为 `macula-dev` |
| `spring.cloud.nacos.discovery.server-addr` | Polaris Nacos 兼容地址：local `127.0.0.1:38849`，docker `polaris:8848` |

本模块无额外自有属性；表中地址和开关是 samples 配置，不是所有应用的默认值。

```yaml
server:
  port: ${SERVER_PORT:4020}
spring:
  profiles:
    active: '@profile.active@'
    group:
      docker: local
  application:
    name: macula-example-tencent-provider
  config:
    import: optional:polaris
  cloud:
    polaris:
      config:
        enabled: true
        auto-refresh: true
        groups:
          - name: ${spring.application.name}
      discovery:
        enabled: true
        register: true
---
spring:
  config:
    activate:
      on-profile: local
  cloud:
    nacos:
      discovery:
        server-addr: ${POLARIS_NACOS_SERVER_ADDR:127.0.0.1:38849}
    polaris:
      address: ${POLARIS_SERVER_ADDR:grpc://127.0.0.1:38091}
      namespace: ${POLARIS_NAMESPACE:macula-dev}
---
spring:
  config:
    activate:
      on-profile: docker
  cloud:
    nacos:
      discovery:
        server-addr: ${POLARIS_NACOS_SERVER_ADDR:polaris:8848}
    polaris:
      address: ${POLARIS_SERVER_ADDR:grpc://polaris:8091}
      namespace: ${POLARIS_NAMESPACE:macula-dev}
```

`dev/stg/pet/prd` 仅保留配置中心连接信息，其他配置由 Polaris 配置组提供。`optional:polaris` 只放宽配置导入，不代表服务发现等依赖可以完全离线运行。

Redis 连接使用 `spring.data.redis.*`，详见 [Redis](/docs/latest/01_services/框架基础/redis/)；可观测性导出使用 `management.*`，详见 [Observability](/docs/latest/01_services/生产准备/observability/)。云平台示例普通 profile 默认关闭 OTLP 网络导出，叠加 `observability` profile 时开启。

## 核心功能

- 通过 Polaris 加载配置、注册和发现服务，结合 Feign 调用下游服务。
- Tencent SCG 组合共享 Gateway，提供 HTTP / WebSocket 转发；路由、认证、签名与加解密见 [Gateway](/docs/latest/01_services/微服务/gateway/)。Reactive 网关不混入 Servlet Web Starter，加解密与签名扩展由业务提供 `CryptoService`。
- Tencent 不使用 Alibaba 的 Nacos 灰度模块；两套云平台的配置与依赖按实际选择分别接入。

Polaris、Redis 与 IAM 等运行服务需单独部署；启动和本地容器环境见 [Examples README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-examples)。

请参考[官方文档](https://github.com/tencent/spring-cloud-tencent)

## 依赖引入

微服务模块

```xml

<dependencies>
    <!-- Spring Cloud -->
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-feign</artifactId>
    </dependency>

    <!-- Spring Cloud Tencent -->
    <dependency>
        <groupId>com.tencent.cloud</groupId>
        <artifactId>spring-cloud-starter-tencent-all</artifactId>
    </dependency>
</dependencies>
```

网关模块

```xml

<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-cloud-gateway</artifactId>
    </dependency>

    <dependency>
        <groupId>com.tencent.cloud</groupId>
        <artifactId>spring-cloud-starter-tencent-all</artifactId>
    </dependency>
</dependencies>
```

Macula Boot 6.1 的 Tencent 与 Tencent SCG Starter 默认排除 Polaris Contract。该组件当前仍依赖 Springdoc
2.x：在普通应用中会导致合约上报出现 `NoSuchMethodError`，在 reactive gateway 中会直接导致启动失败。
确需合约上报时，请等待 Spring Cloud Tencent 提供 Springdoc 3 兼容版本后再显式引入
`spring-cloud-starter-tencent-polaris-contract`。

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/LICENSE)。

- spring-cloud-tencent：https://github.com/Tencent/spring-cloud-tencent/blob/2021.0/LICENSE
