---
title: "Gateway：入口认证与访问控制"
linkTitle: "Gateway"
weight: 3
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
source_paths: ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerAuthorizationManager.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/KongApiGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ApiKeyAuthenticationFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/JwtConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/NimbusJwkSetEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayAutoConfiguration.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "3fbd28dc74d683055d27b81929971c0e45047878", "paths": ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerAuthorizationManager.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/KongApiGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ApiKeyAuthenticationFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/JwtConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/NimbusJwkSetEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayAutoConfiguration.java"]}]
---

## 概览

Gateway 是外层入口，处理 Token、AK/SK、API Key 认证及对应的访问规则，并把可信身份转为内部 JWT。下游 BFF / Service 继续使用 Security Starter 做 JWT 验签与方法、数据权限控制。整体原理见[安全架构](/docs/latest/00_introduce/安全架构/)。

按云平台选择 `macula-boot-starter-cloud-alibaba-scg` 或 `macula-boot-starter-cloud-tencent-scg`，组合中包含共享 Gateway 模块，版本由 Parent 管理。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba-scg</artifactId>
</dependency>
```

## 使用配置

### Token：对接 IAM

客户端携带 `Authorization: Bearer <access_token>`。网关通过 IAM introspection 验证 Token，读取身份、角色等声明，并按有效期缓存认证信息。

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

地址指向 Macula Cloud IAM，Client 与凭据先在平台登记。网关还需要可用的缓存 Redis；菜单 / 角色 / 应用规则通过 System Redis 提供。

## 核心功能

### Token 的角色、菜单与 URL 权限

System 维护角色、菜单、按钮与接口关联；网关读取 System Redis 中的 URL 角色规则。当前实现用 `spring.application.name:HTTP方法:请求路径` 匹配规则，再与认证身份的角色比较。

```yaml
macula:
  gateway:
    security:
      ignore-urls: []
      only-auth-urls: []
      default-url-require-check: true
```

上例显式选择严格的未匹配 URL 策略。启用前先在 System 中维护与应用名、请求方法、路径对应的 URL 角色规则。配置项含义与默认值为：

| 配置 | 默认值 | 含义 |
| --- | --- | --- |
| `security.ignore-urls` | 空列表，合并内置白名单 | 入口放行路径，不走常规认证与 URL 角色检查 |
| `security.only-auth-urls` | 空列表 | Token 有效即可，不执行该路径的 URL 角色匹配 |
| `security.default-url-require-check` | `false` | 未匹配 URL 规则时是否仍要求角色授权；默认并非所有路径严格拦截 |

配置前缀均为 `macula.gateway`。仅认证路径要有明确用途；具体业务操作仍由服务端注解控制。

当前 URL 角色匹配要求命中允许的正向角色且不命中反向角色；网关的 ROOT 角色有专门的放行逻辑。这不表示内层的所有注解也自动豁免 ROOT。


### AK/SK：应用 HMAC 认证

系统调用通过 HMAC Authorization Header 表明应用并提交签名：

```http
Authorization: hmac username="<AK>", algorithm="hmac-sha256", signature="<Base64签名>"
Date: <当前请求的 HTTP-date>
```

这是协议结构示意，签名必须根据本次请求生成。SK 只用于生成签名，不随请求发送。

网关的 `KongApiGlobalFilter` / `KongApiUtils` 会：

1. 根据应用标识读取 System Redis 中的密钥、租户和应用允许 URL。
2. 如果配置了 `permitUrls`，使用 `HTTP方法:请求路径` 匹配；未配置时该项不限制 URL。
3. 校验 Date 的时间窗口（当前为 5 分钟）和 HMAC 签名。
4. 将通过校验的应用身份、可用租户信息交给 JWT 转换。

GET / DELETE 的签名串包含 `date`、方法、路径及原始 Query；其他请求追加原始请求体的 SHA-256 摘要。Query 的编码、顺序和 body 字节应与实际发送内容一致。

AK/SK 的应用 URL 范围与 Token 的角色 URL 规则是两套不同判断，不能把 HMAC 认证成功理解为获得登录用户角色。

### API Key：平台应用身份

当前识别方式为：

```http
Authorization: Bearer sk-<平台签发的APIKey>
```

`ApiKeyAuthenticationFilter` 在 System Redis 查找 `macula:cloud:system:application:apikey:<完整APIKey>` 对应的 Hash 记录，读取 `applicationCode`、`applicationId` 和可选 `tenantId`。校验成功后建立 `authType=apikey` 的认证上下文，再由 JWT 过滤器向下游传递内部 Token。

```yaml
macula:
  gateway:
    apikey:
      enabled: true
```

该开关默认 `true`，控制默认过滤器是否创建。API Key 需由平台维护有效应用记录，任意 `sk-` 字符串不会通过认证。

当前 API Key 使用应用身份，默认没有用户角色，不走 Token 的菜单 / URL 角色匹配分支；所需的应用操作限制应明确落实在服务端授权规则中。

### 转换为内部 JWT

三种入口使用各自的认证和访问控制路径，通过后由 `AddJwtGlobalFilter` 写入：

```http
Authorization: Bearer <网关签发的JWT>
```

JWT 携带对应 Principal 的可信声明；Token 可带用户角色 / scope，AK/SK 和 API Key 则以应用身份为主。应用身份不能假定具有用户角色，额外声明可通过 `JwtClaimsCustomizer` 定制。

网关公开 `/oauth2/jwks` 供下游验签。Samples 的非网关服务配置：

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://127.0.0.1:6000/oauth2/jwks
```

这里指向 Samples Gateway，既不是 IAM introspection 地址，也不是 BFF 的 Cloud endpoint。Boot Examples 的 Alibaba 网关 HTTP 端口为 `5000`，应使用对应端口。

当前 `JwtConfiguration` 从 `jwk/jose.jks` 加载 RSA 签名材料，可通过自定义 `JWKSource<SecurityContext>` Bean 覆盖；没有单独的 YAML key-store 配置项。部署时提供目标环境的签名材料，使网关签发与下游验签保持一致。

### 路由、Redis 与其他保护

| 范围 | 配置 / 接入点 |
| --- | --- |
| 路由 | `spring.cloud.gateway.server.webflux.routes`，Samples 通过 `/admin/**`、`/openapi/**` 转发 |
| Token / JWT 缓存 | 网关自身 Redis |
| URL 角色、应用密钥、API Key | System Redis，默认相关 Bean 使用 `sysRedisTemplate` |
| 接口签名 / 加解密 | `macula.gateway.sign-switch`、`crypto-switch`、`force-sign`、`force-crypto`、`protect-urls.*`，相关过滤器还需 CryptoService Bean |
| Trace ID | `macula.gateway.trace-id-response-header-enabled`，有有效 Span 时返回 `x-traceId` |

接口签名 / 加解密的开关与 AK/SK 的 HMAC 应用认证不是同一组机制。Samples Gateway 的双 Redis 前缀和 profile 配置见[配置规范](/docs/latest/04_devmanual/应用配置/)。

详细源码：[Gateway 模块](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway)。方法和数据授权继续阅读 [Security](/docs/latest/01_services/框架基础/security/)。

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway-server-webflux</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-loadbalancer</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-redis</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>oauth2-oidc-sdk</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
