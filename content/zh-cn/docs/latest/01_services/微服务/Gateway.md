---
title: "Macula Boot Starter Gateway"
linkTitle: "Gateway"
weight: 3
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "a0178da198a79cbbf66f7b9354d2c8711703e81e"
source_paths: ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerAuthorizationManager.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/KongApiGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ApiKeyAuthenticationFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/JwtConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/NimbusJwkSetEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/pom.xml", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayProperties.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/crypto/CryptoService.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/constants/GatewayConstants.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/SignCheckGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/CryptoGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ProtectUrlsEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/RmOpaqueTokenEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/GrayscalePublishGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/TraceIdGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/BodyGlobalFilter.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/security/ResourceServerAuthorizationManager.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/KongApiGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ApiKeyAuthenticationFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/JwtConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/NimbusJwkSetEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/pom.xml", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/config/GatewayProperties.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/crypto/CryptoService.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/constants/GatewayConstants.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/SignCheckGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/CryptoGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/ProtectUrlsEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/RmOpaqueTokenEndpointFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/GrayscalePublishGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/TraceIdGlobalFilter.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/BodyGlobalFilter.java"]}]
---

## 概览

Gateway 是应用的统一入口，基于 Spring Cloud Gateway WebFlux 提供路由转发、入口认证与授权、接口加解密和签名、调用链关联及灰度标签传递。它既承担安全控制，也承担网关的流量转发与集成职责。

| 能力 | 内容 |
| --- | --- |
| 路由 | HTTP / WebSocket 转发、服务发现、路径过滤与 CORS |
| 认证授权 | Token、AK/SK、API Key，角色 / 菜单 / URL 规则 |
| 内部身份 | 签发内部 JWT，提供 JWK 公钥集供微服务验签 |
| 接口保护 | CryptoService 扩展、SM2 / SM4、请求签名与 nonce 检查 |
| 运行支撑 | 网关与 System Redis、Token 缓存移除、Trace ID 响应头 |
| 灰度接入 | 接收并传递 grayversion 标签，配合云平台负载均衡 |

下游 BFF / Service 继续使用 Security Starter 做 JWT 验签与细粒度授权，整体分层见[请求链路](/docs/latest/00_introduce/应用架构/请求链路/)。本页保留 Gateway 完整能力的接入与使用说明。

## 组件坐标

按实际云平台选择一种 SCG Starter：Alibaba / Nacos 或 Tencent / Polaris，不同时引入。

```xml
<!-- Alibaba / Nacos：与下方 Tencent 方案择一 -->
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba-scg</artifactId>
</dependency>

<!-- Tencent / Polaris：与上方 Alibaba 方案择一 -->
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-tencent-scg</artifactId>
</dependency>
```

两个 SCG Starter 均组合共享的 `macula-boot-starter-cloud-gateway`。继承 Macula Boot Parent 或导入相应 BOM 管理版本；完整云接入见 [Alibaba](/docs/latest/01_services/微服务/alibaba/) / [Tencent](/docs/latest/01_services/微服务/tencent/)。

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。不同应用、文件或替代方案分别标注，请按场景选用。

#### 网关 application.yml

```yaml
server:
  port: ${GATEWAY_PORT:8080}
spring:
  application:
    name: ${APP_NAME:application-gateway}
  data:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
      # 独立 System Redis 可选；需配合“独立 System Redis”的 Java Bean
      system:
        host: ${SYSTEM_REDIS_HOST:127.0.0.1}
        port: ${SYSTEM_REDIS_PORT:6379}
        password: ${SYSTEM_REDIS_PASSWORD}
  cloud:
    gateway:
      server:
        webflux:
          # 如需跨域，按实际来源配置 globalcors，避免照搬通配来源
          # globalcors:
          #   cors-configurations:
          #     "[/**]":
          #       allowed-origins: ["https://admin.example.com"]
          #       allowed-methods: [GET, POST, PUT, PATCH, DELETE, OPTIONS]
          #       allowed-headers: [Authorization, Content-Type]
          routes:
            - id: business-api
              uri: lb://business-service
              predicates:
                - Path=/api/**
              filters:
                - StripPrefix=1
            - id: business-websocket
              uri: lb:ws://message-service
              predicates:
                - Path=/ws/**
              filters:
                - StripPrefix=1
  security:
    oauth2:
      resourceserver:
        opaquetoken:
          client-id: ${IAM_CLIENT_ID}
          client-secret: ${IAM_CLIENT_SECRET}
          introspection-uri: ${IAM_INTROSPECTION_URI}
  reactor:
    context-propagation: auto
macula:
  gateway:
    # 接口保护可选；启用时还需提供 CryptoService Bean
    sign-switch: true
    crypto-switch: true
    force-sign: true
    force-crypto: true
    protect-urls:
      sign:
        - /api/**
      crypto:
        - /api/**
    security:
      ignore-urls: []
      only-auth-urls: []
      default-url-require-check: true
    trace-id-response-header-enabled: true
    rm-opaque-token:
      enabled: true
    rm-opaque-token-endpoint: /gateway/rm/opaqueToken
    force-hmac-rm-opaque-token-endpoint: true
    apikey:
      enabled: true
    # 灰度能力按需开启
    gray:
      enabled: true
  cloud:
    gray:
      enabled: true
```

#### 下游 BFF / Service application.yml

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: ${GATEWAY_JWK_SET_URI}
```

### 关键配置

#### 网关基础配置与开关

在网关应用中设置应用名、Redis、服务发现路由和 IAM introspection。示例中的服务名、端口与环境变量应替换为自己的部署值。

路由中的服务名对应注册中心里的应用名；注册发现及配置中心接入见 [Alibaba](/docs/latest/01_services/微服务/alibaba/) / [Tencent](/docs/latest/01_services/微服务/tencent/)。IAM Client 与凭据由平台登记，URL 权限规则按下文配置。

| 配置 | 用途 |
| --- | --- |
| `server.port` / `server.ssl.*` | 监听端口与 HTTPS 证书 |
| `spring.cloud.gateway.server.webflux.routes` | HTTP / WebSocket 路由、断言与过滤器 |
| `spring.cloud.gateway.server.webflux.globalcors` | 跨域来源、方法与请求头 |
| `spring.data.redis.*` | 网关自身的 Redis 连接 |
| `spring.security.oauth2.resourceserver.opaquetoken.*` | IAM Token introspection 地址及凭据 |
| `spring.reactor.context-propagation` | Reactor 上下文传播，配置为 auto |

Metrics、Traces、Logs 的采集及导出见 [Observability](/docs/latest/01_services/生产准备/observability/)，Collector 地址由应用部署配置提供。

下列属性前缀为 `macula.gateway`：

| 属性 | 默认值 | 说明 |
| --- | --- | --- |
| `sign-switch` / `crypto-switch` | `true` / `true` | 签名 / 加解密全局开关；对应过滤器还需 CryptoService Bean |
| `force-sign` / `force-crypto` | `true` / `false` | 是否强制校验已配置的受保护接口 |
| `protect-urls.sign` / `protect-urls.crypto` | 空列表 | 需签名 / 加密的路径 |
| `trace-id-response-header-enabled` | `true` | 有有效 Span 时输出 `x-traceId` |
| `gray.enabled` | `false` | 启用网关灰度路由处理 |
| `apikey.enabled` | `true` | 创建 API Key 认证过滤器 |
| `rm-opaque-token.enabled` | `true` | 创建 Token 缓存移除端点过滤器 |
| `rm-opaque-token-endpoint` | `/gateway/rm/opaqueToken` | 缓存移除路径 |
| `force-hmac-rm-opaque-token-endpoint` | `true` | 移除 Token 缓存时强制 HMAC 校验 |
| `security.ignore-urls` | 空列表并合并内置白名单 | 放行认证的路径 |
| `security.only-auth-urls` | 空列表 | 只认证、不检查 URL 角色权限的路径 |
| `security.default-url-require-check` | `false` | 未配置 URL 权限时是否要求鉴权，生产需明确评估 |

灰度过滤器的创建另受 `macula.cloud.gray.enabled` 控制（默认 `true`），与 `macula.gateway.gray.enabled` 的运行开关不同。应用还需提供 `spring.application.name`，OAuth2 凭证和签名材料须由部署环境注入。

#### 接口保护配置

注册 CryptoService Bean 后，配置需要保护的**原始入口路径**。上方示例显式要求命中的接口同时提交签名和加密参数；`force-crypto` 默认是 `false`，示例将其设为 `true`：

`protect-urls.sign` 与 `protect-urls.crypto` 分别管理签名和加密范围，可以按业务配置不同清单。只有 CryptoService 存在时，接口签名、加解密及保护规则 / 公钥端点才会注册；仅设置 YAML 不会创建密钥实现。

当前过滤器中，`sign-switch` / `crypto-switch` 参与“缺少参数时是否强制拒绝”的判断；请求已携带完整签名或加密参数时仍会进入相应处理，不能将这两个配置理解为无条件跳过已提交参数的校验。

## 核心功能

### 请求处理全景

先看一条业务请求怎样穿过网关，再阅读下方对应功能。图中的 `WebFilter` 与 `GlobalFilter` 属于不同层次，不能把它们的 `order` 混排成一条链。

![Gateway 请求处理全景：WebFilter、本地端点、Spring Security、路由过滤链、下游服务与响应处理](/diagrams/gateway-filters.svg)

[独立查看过滤器全景图](/diagrams/gateway-filters.svg)，点击图片可放大。图中展示 Starter 默认注册的过滤器及其相对关系；应用自定义过滤器、路由配置和框架内置过滤器会共同影响实际执行链。

Spring Security 通过外层 `WebFilter` 参与请求处理；只有请求通过相关入口规则并匹配路由后，才进入 `FilteringWebHandler` 组织的网关过滤链。后者将 `GlobalFilter` 与当前路由的 `GatewayFilter` 合并，按 `Ordered` 排序。前置处理通常从小到大，响应逻辑则取决于回调、响应装饰器及写回位置。参见 [WebFlux Security](https://docs.spring.io/spring-security/reference/reactive/configuration/webflux.html) 与 [Global Filters](https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/global-filters.html)。

### 入口 WebFilter 与本地端点

这里的顺序仅在外层 `WebFilter` 链中比较，`MIN` 表示 `Integer.MIN_VALUE`。

| 过滤器 | order | 职责与后续流向 |
| --- | --- | --- |
| `NimbusJwkSetEndpointFilter` | MIN + 100 | 匹配 `/oauth2/jwks`，输出公开 JWK 后直接返回；需有 JWKSource |
| `RmOpaqueTokenEndpointFilter` | MIN + 200 | 匹配缓存移除请求，按本端点的 HMAC 规则校验并处理后返回；可通过开关关闭 |
| `ProtectUrlsEndpointFilter` | MIN + 300 | 返回保护路径清单或 SM2 公钥，需有 CryptoService；匹配后就地响应 |
| `ApiKeyAuthenticationFilter` | MIN + 400 | 识别 API Key，校验并建立认证上下文，随后继续进入安全链；可通过开关关闭 |

这些本地端点在 Spring Security 与路由过滤链之前处理，不能指望后面的 URL 授权或 HMAC GlobalFilter 替它们校验。缓存移除端点有自己的 HMAC 检查；公钥与保护规则端点按各自实现返回公开接入资料。未命中本地端点的请求继续向后执行。

### API Key：平台应用身份

这是图中进入 Spring Security 之前的认证分支。当前识别方式为：

```http
Authorization: Bearer sk-<平台签发的APIKey>
```

`ApiKeyAuthenticationFilter` 在 System Redis 查找 `macula:cloud:system:application:apikey:<完整APIKey>` 对应的 Hash 记录，读取 `applicationCode`、`applicationId` 和可选 `tenantId`。校验成功后建立 `authType=apikey` 的认证上下文，再由 JWT 过滤器向下游传递内部 Token。

配置见本页[配置示例](#配置示例)。

`macula.gateway.apikey.enabled` 默认 `true`，控制默认过滤器是否创建。API Key 需由平台维护有效应用记录，任意 `sk-` 字符串不会通过认证。

当前 API Key 使用应用身份，默认没有用户角色，不走 Token 的菜单 / URL 角色匹配分支；所需的应用操作限制应明确落实在服务端授权规则中。

### Token 的角色、菜单与 URL 权限

这是图中的 Spring Security 分支，由 `ResourceServerConfiguration` 配置认证，`ResourceServerAuthorizationManager` 执行 URL 授权。Token 请求按以下流程接入：

1. 客户端通过 `Authorization: Bearer <access_token>` 访问 Gateway。
2. Gateway 调用配置的 IAM introspection 接口，取得身份、角色等声明，并按 Token 有效期缓存认证信息。
3. 通过对应的 URL 访问规则后，由 AddJwtGlobalFilter 转换为内部 JWT，传给下游 Security Starter 验签。

System 维护角色、菜单、按钮与接口关联；网关读取 System Redis 中的 URL 角色规则。当前实现用 `spring.application.name:HTTP方法:请求路径` 匹配规则，再与认证身份的角色比较。

配置见本页[配置示例](#配置示例)。

集中配置中的 `default-url-require-check: true` 显式选择严格的未匹配 URL 策略。启用前先在 System 中维护与应用名、请求方法、路径对应的 URL 角色规则。配置项含义与默认值为：

| 配置 | 默认值 | 含义 |
| --- | --- | --- |
| `security.ignore-urls` | 空列表，合并内置白名单 | 入口放行路径，不走常规认证与 URL 角色检查 |
| `security.only-auth-urls` | 空列表 | Token 有效即可，不执行该路径的 URL 角色匹配 |
| `security.default-url-require-check` | `false` | 未匹配 URL 规则时是否仍要求角色授权；默认并非所有路径严格拦截 |

配置前缀均为 `macula.gateway`。仅认证路径要有明确用途；具体业务操作仍由服务端注解控制。

当前 URL 角色匹配要求命中允许的正向角色且不命中反向角色；网关的 ROOT 角色有专门的放行逻辑。这不表示内层的所有注解也自动豁免 ROOT。

### HTTP 与 WebSocket 路由

通过 `spring.cloud.gateway.server.webflux.routes` 声明路由。基础配置中的 HTTP 路由使用 `lb://<服务名>`，WebSocket 路由使用 `lb:ws://<服务名>`，结合 Path 和 StripPrefix 过滤器转发至注册中心中的服务实例。

上面的 `StripPrefix=1` 去掉第一层入口前缀，例如 `/api/orders` 会转发为业务服务的 `/orders`。WebSocket 路由同样按自身的端点路径设置；调整路由时一起核对调用方路径与下游 Controller / WebSocket 端点。

跨域通过 `spring.cloud.gateway.server.webflux.globalcors` 配置。来源、请求头及方法按应用填写，接口保护协议使用的自定义请求头也要纳入允许范围；保护端点跨域处理还可使用 CorsConfigurationSource Bean。

### 网关过滤器链

路由匹配后，下列 `GlobalFilter` 与路由过滤器合并排序。表格列出 Macula 过滤器的**相对请求顺序**，不代表连续执行，中间仍可能插入框架或路由自带的过滤器。

| GlobalFilter | order | 做什么 / 何时生效 |
| --- | --- | --- |
| `GrayscalePublishGlobalFilter` | HIGHEST_PRECEDENCE | 读取并传递灰度标签；创建与运行分别受灰度开关控制 |
| `BodyGlobalFilter` | -10 | 对带签名、加密或 HMAC 的 POST / PUT / PATCH 请求缓存原始 Body 字节，供后续读取 |
| `SignCheckGlobalFilter` | -8 | 检查接口签名、时间戳与 nonce，验签使用实际收到的载荷；需有 CryptoService |
| `CryptoGlobalFilter` | -5 | 解密请求，安装后续写回时使用的响应加密装饰器；需有 CryptoService |
| `KongApiGlobalFilter` | 200 | 对 HMAC 请求检查应用密钥、Date、签名及应用允许 URL |
| `AddJwtGlobalFilter` | 1000 | 将已确认的 Token / HMAC / API Key 身份转为内部 JWT |
| `TraceIdGlobalFilter` | LOWEST_PRECEDENCE | 注册链执行成功后的回调，在有效 Span 中补充响应 Trace ID |

`BodyGlobalFilter` 的缓存位于当前请求的 exchange 属性中，用于重复读取一次性请求流；它不是 Redis 缓存。后续签名校验与请求重写需要这些字节，因此不要在自定义过滤器中提前消费 Body 却不恢复请求流。

接口签名的 `-8` 先于解密的 `-5`，所以前端对实际发送的密文载荷签名；HMAC 的 `200` 是另一套应用认证协议，不等于接口签名。二者若与路径重写或载荷改写叠加使用，需要按实际过滤链核对签名所用的路径、Query 与 Body，不能假定各过滤器看到的请求都相同。

路由上的 `StripPrefix`、`RewritePath` 等也进入这条合并链；原始入口路径与转发路径可能不同。URL 权限、接口保护和 HMAC 允许范围应分别按对应环节的路径匹配，而不是直接复用一份重写后的路径。

框架随后负责目标 URL 构造、`lb` 服务实例解析以及 HTTP / WebSocket 转发。灰度过滤器提供标签，实际实例筛选由云平台负载均衡接入完成；`TraceIdGlobalFilter` 的数字虽排在末端，它的主要作用仍是响应侧回调，不表示必须在网络转发前完成全部 Trace 处理。

### 灰度标签传递

配置见本页[配置示例](#配置示例)。

`macula.cloud.gray.enabled` 控制灰度过滤器是否创建（默认 `true`），`macula.gateway.gray.enabled` 控制其运行行为（默认 `false`）。开启后从请求头读取 `grayversion`，设置并传递灰度上下文，再在处理后清理。

该过滤器负责入口标签接入；服务实例的筛选与负载均衡由云平台接入模块完成，Alibaba 的 Nacos 元数据与灰度选择规则见 [Alibaba](/docs/latest/01_services/微服务/alibaba/)。它本身不提供百分比放量或用户分群策略。

### 接口加解密与签名

接口保护由 `SignCheckGlobalFilter`、`CryptoGlobalFilter` 和 `ProtectUrlsEndpointFilter` 协作完成。它与上面的 AK/SK HMAC 应用认证分别处理不同协议，不能互相替代。

#### 1. 实现并注册 CryptoService

实现 `dev.macula.boot.starter.cloud.gateway.crypto.CryptoService`，作为 Spring Bean 提供公钥、SM4 密钥解密和数据加解密能力：

```java
public interface CryptoService {
    String getSm2PublicKey();
    String decryptSm4Key(String key);
    String encrypt(String plainText, String sm4Key);
    String decrypt(String secretText, String sm4Key);
}
```

可以对接独立密钥服务。下面是本地 CryptoService 实现：SM4 密钥采用 **32 位十六进制字符串**，先解码为 16 字节；SM2 公钥使用未压缩点编码，与前端约定一致。

```java
import cn.hutool.core.util.HexUtil;
import cn.hutool.crypto.SecureUtil;
import cn.hutool.crypto.SmUtil;
import cn.hutool.crypto.asymmetric.KeyType;
import cn.hutool.crypto.asymmetric.SM2;
import dev.macula.boot.starter.cloud.gateway.crypto.CryptoService;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.stereotype.Component;

import java.security.KeyPair;

/**
 * {@code LocalCryptoService} 本地加解密服务
 *
 * @author rain
 * @since 5.0.0
 */
@Component
public class LocalCryptoService implements CryptoService, InitializingBean {
    private SM2 sm2;

    @Override
    public String getSm2PublicKey() {
        return HexUtil.encodeHexStr(sm2.getQ(false));
    }

    @Override
    public String decryptSm4Key(String key) {
        // TODO 缓存解密过后的密钥
        return sm2.decryptStr(key, KeyType.PrivateKey);
    }

    @Override
    public String encrypt(String plainText, String sm4Key) {
        return SmUtil.sm4(HexUtil.decodeHex(sm4Key)).encryptBase64(plainText);
    }

    @Override
    public String decrypt(String secretText, String sm4Key) {
        return SmUtil.sm4(HexUtil.decodeHex(sm4Key)).decryptStr(secretText);
    }

    @Override
    public void afterPropertiesSet() {
        KeyPair pair = SecureUtil.generateKeyPair("SM2");
        sm2 = SmUtil.sm2(pair.getPrivate(), pair.getPublic());
    }
}
```

该示例每次启动生成临时 SM2 密钥，适用于单实例联调；多实例或重启后仍需使用相同密钥的环境，应由部署环境或密钥服务统一提供密钥材料。私钥留在服务端。此实现约定 SM4 密钥是 32 位十六进制字符串，前后端统一按十六进制解码为 16 字节。

#### 2. 前端获取规则与公钥

| 端点 | 返回内容 |
| --- | --- |
| `/gateway/protect/urls` | Result.data 中的 crypto / sign 路径清单 |
| `/gateway/protect/key` | Result.data 中的 SM2 公钥 |

前端先按原始请求路径匹配规则，再生成随机 SM4 密钥。使用 **SM2 公钥**加密此密钥，将密文放入 `sm4-key` 请求头；SM4 是对称算法，不存在“SM4 公钥”。

#### 3. 请求加密与响应解密

| 请求 | 加密载荷约定 |
| --- | --- |
| GET / DELETE | 对原始 Query 参数文本进行 SM4 加密，将 Base64 密文放入 `?data=<密文>` |
| POST / PUT / PATCH | 对 JSON 请求体文本进行 SM4 加密，以 `{"data":"<Base64密文>"}` 发送 |

携带 `sm4-key` 与 `sym-alg: SM4`。GET / DELETE 的 Base64 值需要正确做 URL 编码，保留 `+`、`/`、`=` 等字符；参数顺序和前后端处理方式一致。

网关先解出 SM4 密钥，恢复 Query / JSON Body 后向业务服务转发；在响应阶段加密 Result 的 `data` 字段，前端用同一 SM4 密钥解密。Result 的状态字段仍用于处理请求结果，不能把整个返回 JSON 当作密文。

当前请求体解密针对 `application/json`；不要把 form-data、文件上传、任意流式响应当作已有的自动加解密能力。`sym-alg` 是协议头约定，具体算法仍由 CryptoService 实现，不会仅根据该头自动创建算法实现。

#### 4. 请求签名与 nonce 检查

需要签名的请求携带：

```http
sm4-key: <SM2加密后的SM4密钥>
timestamp: <Unix毫秒时间戳>
nonce: <本次请求的唯一随机串>
algorithm: SHA-256
signature: <签名的十六进制字符串>
```

即使只签名、不加密业务载荷，也需要 `sm4-key`，因为网关解出的密钥参与签名计算。当前默认摘要算法为 SHA-256；与 AK/SK 的 `Authorization: hmac ...` 签名串不同。

网关按当前过滤器实现构造签名原文：

```text
params = Query 按 key 排序，仅取每个 key 的第一个值，非空时用 & 连接 key=value
POST / PUT / PATCH 且请求体非空时：
  params = params + "SHA-256=" + lowercaseHex(SHA256(原始请求体字节))

plain = 原始请求路径 + params + 解密得到的SM4密钥字符串 + timestamp + nonce
signature = hex(Digest(algorithm, plain))
```

路径使用网关入口的原始路径；请求体摘要是 **十六进制**，不是 Base64。若载荷已经加密，签名计算使用实际发送的加密 Query / Body。不要额外插入未约定的分隔符，也不要让 Query 编码、参数顺序、Body 字节在签名后发生变化。

网关要求请求时间与服务器时间差小于 300 秒；检查 nonce 是否已存在于网关 Redis，并登记 300 秒。缺少必需头、时间超限、nonce 重复或摘要不匹配会返回相应失败结果。默认签名过滤器顺序为 `-8`，加解密过滤器为 `-5`，即先验证实际收到的数据，再解密转发。

#### 5. 后端处理顺序

1. 按原始 URL 与强制规则决定缺少签名 / 加密参数时是否拒绝。
2. 验证时间戳、nonce 和签名。
3. 使用 CryptoService 解密 SM4 密钥及请求内容。
4. 转发给业务微服务执行原有接口。
5. 加密响应 Result.data，前端收到后解密。

### AK/SK：应用 HMAC 认证

HMAC 请求在入口授权管理器中先进入系统调用分支，随后由 `KongApiGlobalFilter`（order 200）实际验签；入口放行不代表签名已经通过。系统调用通过 HMAC Authorization Header 表明应用并提交签名：

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

### 转换为内部 JWT

这是图中 order 1000 的身份转接点。三种入口使用各自的认证和访问控制路径，通过后由 `AddJwtGlobalFilter` 写入：

```http
Authorization: Bearer <网关签发的JWT>
```

JWT 携带对应 Principal 的可信声明；Token 可带用户角色 / scope，AK/SK 和 API Key 则以应用身份为主。应用身份不能假定具有用户角色，额外声明可通过 `JwtClaimsCustomizer` 定制。

网关公开 `/oauth2/jwks` 供下游验签。后端微服务配置本应用网关的公钥地址：

配置见本页[配置示例](#配置示例)。

`GATEWAY_JWK_SET_URI` 填写可访问的网关公钥 URL，例如 `http://application-gateway:8080/oauth2/jwks`；它用于验证网关签发的 JWT，与 IAM 的 introspection 地址分别配置。

当前 `JwtConfiguration` 从 `jwk/jose.jks` 加载 RSA 签名材料，可通过自定义 `JWKSource<SecurityContext>` Bean 覆盖；没有单独的 YAML key-store 配置项。部署时提供目标环境的签名材料，使网关签发与下游验签保持一致。

JWT 的 `iss` 声明由 `spring.security.oauth2.resourceserver.jwt.issuer-uri` 设置，当前默认 `http://127.0.0.1:9010`。这里是网关签发内部 JWT 的标识配置；JWK 验签材料与下文接口保护使用的 SM2 / SM4 密钥各自独立。

### 独立 System Redis

网关自身的 Redis 保存认证缓存与签名 nonce，System Redis 提供角色与应用信息。两者独立部署时，在应用中提供两套连接及模板。集中配置中的 `spring.data.redis.system.*` 为应用手动绑定的自定义前缀，需要配合下方 Java Bean 声明。

配置见本页[配置示例](#配置示例)。

`SYSTEM_REDIS_*` 连接信息由部署环境注入。

```java
/**
 * {@code RedisConfiguration} Redis配置
 *
 * @author rain
 * @since 2023/4/21 11:50
 */
@Configuration
public class RedisConfiguration {
    @Bean
    @Primary
    @ConfigurationProperties(prefix = "spring.data.redis")
    public DataRedisProperties redisProperties() {
        return new DataRedisProperties();
    }

    @Bean
    @ConfigurationProperties(prefix = "spring.data.redis.system")
    public DataRedisProperties sysRedisProperties() {
        return new DataRedisProperties();
    }

    @Primary
    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClient(ApplicationContext ctx, DataRedisProperties redisProperties) throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, redisProperties, new RedissonProperties());
        return Redisson.create(config);
    }

    @Bean(destroyMethod = "shutdown")
    public RedissonClient sysRedissonClient(ApplicationContext ctx, DataRedisProperties sysRedisProperties)
        throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, sysRedisProperties, new RedissonProperties());
        return Redisson.create(config);
    }

    @Bean(name = "sysRedisTemplate")
    public RedisTemplate<String, Object> sysRedisTemplate(
        @Qualifier("sysRedissonClient") RedissonClient sysRedissonClient) {
        //数据泛型类型
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        //设置连接工厂（Jedis或Lettuce）
        template.setConnectionFactory(new RedissonConnectionFactory(sysRedissonClient));

        //设置key的序列化方式---String
        template.setKeySerializer(RedisSerializer.string());
        template.setHashKeySerializer(RedisSerializer.string());
        //初始化RedisTemplate的参数设置
        template.afterPropertiesSet();
        return template;
    }
}
```

上述扩展明确提供网关自身 `redisTemplate` 和访问平台数据的 `sysRedisTemplate`。外部 Token / JWT 缓存、签名 nonce 使用网关 Redis；URL 角色、应用密钥、API Key 使用 System Redis。单 Redis 与独立 System Redis 的连接配置按工程选择，不能只新增一个前缀就假定自动创建第二连接。

### Token 缓存移除

默认提供 `POST /gateway/rm/opaqueToken`，用于清除网关缓存的外部 Token 身份信息和关联 JWT 缓存：

```http
POST /gateway/rm/opaqueToken
Authorization: hmac username="<AK>", algorithm="hmac-sha256", signature="<Base64签名>"
Date: <当前请求的HTTP-date>
Content-Type: application/json

{"token":"<需要清除网关缓存的外部Token>"}
```

默认要求有效 HMAC，调用方需按 AK/SK 规则为本次请求（包括 JSON Body）签名。开关为 `macula.gateway.rm-opaque-token.enabled`，路径可通过 `rm-opaque-token-endpoint` 调整；`force-hmac-rm-opaque-token-endpoint` 默认 `true`。

该操作只移除网关缓存，不等于撤销 IAM Token，也不会使已经签发给调用方的 JWT 立即失效。凭据撤销与有效期仍需结合认证平台和实际验证链路处理。

### Trace ID 响应头

有 Micrometer Tracer 且存在当前有效 Span 时，网关返回 `x-traceId` 以关联入口、下游调用与日志。`macula.gateway.trace-id-response-header-enabled` 默认 `true`；无 Tracer、无当前 Span 或关闭此项时不输出空响应头。

指标、链路、日志的采集与 OTLP 导出由 [Observability](/docs/latest/01_services/生产准备/observability/) 负责。WebFlux / Gateway 使用 `spring.reactor.context-propagation: auto` 传播上下文，Trace ID 响应头开关不等于开启三类遥测导出。

响应阶段还会执行框架的代理响应写回；启用加解密时，`CryptoGlobalFilter` 安装的装饰器在写回过程中处理 Result.data。因此不能将请求侧 order 简单倒过来，当作所有响应逻辑的固定顺序。某个早期 WebFilter 或安全链直接返回时，后面的 Crypto、JWT、Trace 等 GlobalFilter 不会全部执行。

## 依赖引入

以下为组件 POM 的直接依赖（不含测试依赖），用于了解依赖组成；引入上方 Starter 后由 Maven 传递解析，无需在应用中逐项重复声明。版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway-server-webflux</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-loadbalancer</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-redis</artifactId>
</dependency>

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
</dependency>

<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>oauth2-oidc-sdk</artifactId>
</dependency>

<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
</dependency>

<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing</artifactId>
</dependency>
```

## 版权说明

- oauth2-oidc-sdk：https://github.com/hidglobal/oauth-2.0-sdk-with-openid-connect-extensions/blob/master/LICENSE.txt
- caffeine：https://github.com/ben-manes/caffeine/blob/master/LICENSE
- spring-cloud-gateway：https://github.com/spring-cloud/spring-cloud-gateway/blob/main/LICENSE.txt

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/LICENSE)。
