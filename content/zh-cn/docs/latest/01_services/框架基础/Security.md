---
title: "Security：方法授权与资源归属"
linkTitle: "Security"
weight: 10
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
source_paths: ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/CheckOwner.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/authorization/CheckOwnerAdvisor.java", "macula-boot-starters/macula-boot-starter-system/src/main/java/dev/macula/boot/starter/system/service/PermissionService.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "3fbd28dc74d683055d27b81929971c0e45047878", "paths": ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/CheckOwner.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/authorization/CheckOwnerAdvisor.java", "macula-boot-starters/macula-boot-starter-system/src/main/java/dev/macula/boot/starter/system/service/PermissionService.java"]}]
---

## 概览

Security Starter 运行在 BFF 和业务微服务中：验证网关 JWT、建立 Spring Security 认证上下文，并在业务方法上执行细粒度授权。网关的认证与 URL 控制见 [Gateway](/docs/latest/01_services/微服务/gateway/)，整体分层见[安全架构](/docs/latest/00_introduce/安全架构/)。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-security</artifactId>
</dependency>
```

## 使用配置

### JWT 验签配置

Samples 中，BFF、Service1、Basic、OpenAPI、Thirdparty 均指向本应用 Gateway 的公钥集：

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://127.0.0.1:6000/oauth2/jwks
macula:
  security:
    ignore-urls: []
```

容器环境将 JWK 地址改为 `http://macula-samples-gateway:6000/oauth2/jwks`；其他应用按自己的网关地址配置。

| 配置 | 含义 |
| --- | --- |
| `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` | 网关 JWK 公钥集，用于验证内部 JWT |
| `jwt.public-key-location` | 同一 Spring Security JWT 前缀下的本地 RSA 公钥替代方式 |
| `jwt.issuer-uri` | 同一前缀下按 issuer 发现验签配置，目标必须与实际签发方式相符 |
| `jwt.jws-algorithms` | JWK / 公钥方式允许的签名算法，Boot 默认 RS256 |
| `macula.security.ignore-urls` | 合并内置白名单和 Inner 路径的放行配置 |

明确选择与网关对应的验签方式，不混用不同密钥模式。模块保留无 JWK / issuer / 公钥且无自定义 JwtDecoder 时的对称 `secret` 兼容模式；接入网关时显式配置 JWK，不依赖公开默认值。

## 核心功能

### SecurityUtils：读取认证上下文

JWT 验签后建立认证上下文，业务可以读取：

| 方法 | 信息 |
| --- | --- |
| `getCurrentUser()` | 当前认证名，默认来自 JWT 的 sub |
| `getRoles()` | 角色 Code，去掉 ROLE_ 前缀 |
| `getTenantId()` | Token 声明中的租户 |
| `getDeptId()` / `getDataScope()` | 部门与数据范围声明 |
| `getTokenAttributes()` | 已解析的 Token 声明 |

`SecurityUtils` 是信息读取工具，不会自动校验按钮、资源归属或过滤数据库查询。AK/SK / API Key 的认证名可能是应用标识，不能直接当作登录用户。

### @PreAuthorize：执行前授权

Starter 已通过 `@EnableMethodSecurity` 开启方法安全。常见表达式：

| 表达式 | 检查什么 |
| --- | --- |
| `hasRole('ADMIN')` | ROLE_ADMIN 角色，不写 ROLE_ 前缀 |
| `hasAuthority('ROLE_ADMIN')` | 精确的角色权限字符串 |
| `hasAuthority('SCOPE_orders.read')` | JWT scope/scp 转换得到的权限 |
| `@pms.hasPermission('order:cancel')` | 平台登记的按钮 / 操作权限标识 |

默认 JWT 转换器将 authorities 声明转为 `ROLE_` 权限，将 scope/scp 转为 `SCOPE_` 权限。直接写 `hasAuthority('order:cancel')` 不会自动查询平台按钮权限。

使用 PMS 表达式时，应用还需引入 System Starter，配置 `macula.cloud.endpoint`、`app-key`、`secret-key`，使 `pms` Bean 能获取当前用户的按钮权限。

```java
@PreAuthorize("@pms.hasPermission('order:cancel')")
public void cancel(String orderId) {
    orderService.cancel(orderId);
}
```

`order:cancel` 是业务在平台登记的操作标识。前端可用它控制按钮显示，后端使用注解验证操作权限；仅隐藏按钮不能替代后端检查。

### @PostAuthorize：根据真实结果检查

适用于同步、无副作用的查询。以下为业务示意，OrderView 提供 ownerUsername 属性，使用与认证名相同的标识体系：

```java
@PreAuthorize("isAuthenticated()")
@PostAuthorize("returnObject != null and returnObject.ownerUsername == authentication.name")
public OrderView getById(String orderId) {
    return orderRepository.findViewById(orderId);
}
```

这发生在方法返回后。检查失败拒绝返回，但不能撤销已经发生的写入、消息或其他副作用；写操作的权限在执行前检查。

### @CheckOwner：两种资源控制模式

通过必填的 value 表达式区分两种模式，不按 HTTP 动词或是否携带 Header 自动选择：

| 表达式 | 时机 | 校验依据 |
| --- | --- | --- |
| `returnObject.ownerUsername` | 方法返回后 | 从服务端真实结果取得拥有者，与 authentication.name 相等 |
| `#p0` / `#p0.orderId` | 方法执行前 | 指定资源 ID 的 Passkey 与当前身份、资源及有效期匹配 |

#### 返回值归属

```java
@CheckOwner("returnObject.ownerUsername")
public OrderView getById(String orderId) {
    return orderRepository.findViewById(orderId);
}
```

需要导入 `dev.macula.boot.starter.security.annotation.CheckOwner`。拥有者标识应来自服务端数据，并与当前认证名保持相同标识体系和类型。返回为空、拥有者为空或不匹配会拒绝，ROOT / ADMIN 不自动豁免。

表达式针对被标注方法的实际返回值：若方法直接返回 OrderView，就访问其属性；若方法本身返回 Result 包装，按实际 data 层取值。后续响应 Advice 统一包装不改变方法的表达式层级。

#### 执行前资源 Passkey

业务先按当前用户、租户和数据范围查询授权列表。列表 DTO 实现 Commons 的 `dev.macula.boot.security.PasskeyResource`，提供稳定、全局唯一的 resourceId 和 passkey 字段，Web Starter 的响应 Advice 才能为授权列表签发凭证。

```yaml
macula:
  security:
    passkey:
      enabled: true
      ttl: 5m
      secret-base64: ${PASSKEY_SECRET_BASE64}
```

| 配置 | 默认 / 约束 |
| --- | --- |
| `enabled` | false；关闭时不签发，入参模式拒绝，返回值归属模式仍可使用 |
| `ttl` | 5m，须为至少 1 秒的正有效期 |
| `secret-base64` | 无默认值，解码后至少 32 字节的独立服务端密钥 |

需要同时接入 Web Starter 的列表签发与 Security 的验证；单独引入 Security 不会自动为响应签发。

```java
@PreAuthorize("@pms.hasPermission('order:cancel')")
@CheckOwner("#p0")
public void cancel(String orderId) {
    orderService.cancel(orderId);
}
```

调用方携带 `X-Resource-Passkey` Header（推荐）或 `passkey` Query。缺失、冲突、过期或与身份 / 资源不匹配时，在执行前拒绝；同一资源的凭证不能授权请求中的其他资源。前置模式失败不会降级为返回值归属模式。

### 组合规则与边界

- 注解通过 Spring Bean 代理生效，同类内自调用、手动 new 对象不经过这些拦截器。
- 角色、scope、PMS 操作权限与资源归属分别检查；网关放行不表示业务方法自动有权执行。
- Gateway URL 匹配与 PMS 各自有明确的 ROOT 放行逻辑，CheckOwner 没有统一管理员豁免。
- 后置注解不逐条过滤集合。列表、分页、统计、导出由查询条件落实用户、租户与数据范围。
- CheckOwner 用于同步单对象；资源凭证不能替代操作权限、租户边界或业务事务条件。
- Passkey 到期前可复用，业务授权变化不会自动撤销已签发凭证；其签名不包含租户 / action，应用仍要落实相应边界。
- 当前 CheckOwner 的前置 / 后置模式由统一 Advisor 实现；注解模板 Bean 可供其他组合注解使用，不用它代替 CheckOwner 的资源校验。

更多返回包装、参数解析与 Passkey 扩展说明见 [Security 源码 README](https://github.com/macula-projects/macula-boot/tree/main/macula-boot-starters/macula-boot-starter-security)。实际应用组织参见 [Samples 模块说明](/docs/latest/04_devmanual/模块说明/)和[配置规范](/docs/latest/04_devmanual/应用配置/)。

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
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
    <groupId>com.nimbusds</groupId>
    <artifactId>oauth2-oidc-sdk</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
