---
title: "快速开始"
linkTitle: "快速开始"
weight: 2
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
source_paths: ["macula-boot-examples/README.md", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-starters/macula-boot-starter-system/README.md"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "3fbd28dc74d683055d27b81929971c0e45047878", "paths": ["macula-boot-examples/README.md", "macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-consumer/src/main/resources/application.yml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-starters/macula-boot-starter-system/README.md"]}]
---

## 先理解最小链路

`浏览器携带 IAM Token → Gateway 验证并签发内部 JWT → BFF → Service`

`macula-boot-examples` 用来快速验证框架接入。以 Alibaba 示例为例，`gateway` 是统一入口，`consumer` 可对应 BFF / 服务消费方，`provider1` 对应业务 Service。Tencent 示例使用相同的角色划分。

| 角色 | 核心职责与配置 |
| --- | --- |
| Gateway | 接入 Macula Cloud IAM，验证客户端 Token，并向下游传递网关签发的 JWT |
| BFF | 聚合业务接口；通过 `macula.cloud.endpoint` 获取 Macula Cloud 的菜单和用户信息 |
| Service | 实现业务逻辑；与 BFF 一样，使用网关的 `jwk-set-uri` 验证内部 JWT |

网关与内层微服务如何协同授权，先看[安全架构](/docs/latest/00_introduce/安全架构/)；下文只列最小接入配置。

## 1. Gateway 接入 IAM

在 Gateway 的对应环境配置中设置 IAM introspection 地址和访问凭据：

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        opaquetoken:
          client-id: ${IAM_CLIENT_ID}
          client-secret: ${IAM_CLIENT_SECRET}
          introspection-uri: ${OAUTH2_INTROSPECTION_URI:http://127.0.0.1:9010/oauth2/introspect}
```

地址指向 IAM；Client 需先在平台登记。示例中的占位变量由运行环境提供。

## 2. BFF 接入 Macula Cloud

BFF 引入 System Starter，并配置 **Macula Cloud 网关**地址及登记的应用凭据：

```yaml
macula:
  cloud:
    endpoint: http://127.0.0.1:9000
    app-key: ${MACULA_CLOUD_APP_KEY}
    secret-key: ${MACULA_CLOUD_APP_SECRET}
```

System Starter 通过该入口访问菜单、用户等平台接口；`endpoint` 填基础地址，客户端会追加 `/system`。

## 3. 非网关后端验证内部 JWT

BFF、Service 等非网关的后端运行模块都配置**应用网关**的 JWK 地址：

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://127.0.0.1:5000/oauth2/jwks
```

此处验证的是 Gateway 签发的内部 JWT。Boot Examples 的 Alibaba 网关 HTTP 端口为 `5000`；下面开发指引采用的 Samples 网关端口为 `6000`，需要相应调整 JWK 地址。容器环境使用应用网关的服务名。

## 运行示例与继续开发

准备 Java 17、Maven，以及所选示例需要的 Nacos / Polaris 和 Macula Cloud IAM、System。按 [Boot Examples README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-examples) 启动 provider、consumer、gateway，确认上述三个地址与平台登记信息一致。

平台尚未启动时，先看[部署 Macula 平台](/docs/latest/04_devmanual/部署macula平台/)。开始编写业务应用后，转到 [Macula Samples 开发指引](/docs/latest/04_devmanual/)，了解各模块的职责及 [application.yml 配置规范](/docs/latest/04_devmanual/应用配置/)。
