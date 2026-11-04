---
title: "Macula Boot Starter Security"
linkTitle: "Security"
weight: 10
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "5ff9b5c8e6166449ced7512cd3bf74a672aa922e"
source_paths: ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-commons/src/main/java/dev/macula/boot/context/TenantContextHolder.java", "macula-boot-starters/macula-boot-starter-mybatis-plus/src/main/java/dev/macula/boot/starter/mp/config/MyBatisPlusAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "291e80dc296587cc1ec4f4979aa6fdb3bd087054", "paths": ["macula-cloud-system/README.md", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/SysApplicationServiceImpl.java", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/SysTenantServiceImpl.java", "macula-cloud-system/src/main/resources/db/migration/V12__application_auth_tenant.sql", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/service/userdetails/SysUserDetailsServiceImpl.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/protocol/oauth2/CustomOAuth2TokenCustomizer.java", "macula-cloud-system/src/main/java/dev/macula/cloud/system/form/OAuth2ClientForm.java"]}]
---

## 概览

Security Starter 运行在 BFF 和业务微服务中：验证网关 JWT、建立 Spring Security 认证上下文，并在业务方法上执行细粒度授权。网关的认证与 URL 控制见 [Gateway](/docs/latest/01_services/微服务/gateway/)，整体分层见[请求链路](/docs/latest/00_introduce/请求链路/)。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-security</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml：JWT 验签与可选 Passkey

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          # 按实际签发方式择一；接入应用网关优先使用 jwk-set-uri
          # public-key-location: classpath:gateway-public.pem
          # issuer-uri: https://issuer.example.com
          jws-algorithms: RS256
          jwk-set-uri: http://127.0.0.1:6000/oauth2/jwks
macula:
  security:
    ignore-urls: []
    # 可选功能；下方 true 为启用示例，不使用时设为 false
    passkey:
      enabled: true
      ttl: 5m
      secret-base64: ${PASSKEY_SECRET_BASE64}
```

### 关键配置

| 配置 | 说明 |
| --- | --- |
| `macula.security.passkey.enabled` | 资源凭证签发与执行前验证的开关；示例按启用场景配置，默认关闭。 |
| `macula.security.passkey.ttl / secret-base64` | 凭证有效期与服务端签名密钥。 |

#### JWT 验签配置

Samples 中，BFF、Service1、Basic、OpenAPI、Thirdparty 均指向本应用 Gateway 的公钥集：

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
| `getTenantId()` | 已认证 Token 的默认业务租户，不读取临时 Holder |
| `getDeptId()` / `getDataScope()` | 部门与数据范围声明 |
| `getTokenAttributes()` | 已解析的 Token 声明 |

`SecurityUtils` 是信息读取工具，不会自动校验按钮、资源归属或过滤数据库查询。AK/SK / API Key 的认证名可能是应用标识，不能直接当作登录用户。

### 认证租户与临时上下文

`SecurityUtils.getTenantId()` 读取认证声明中的 `tenantId`：用户登录时关联 OAuth Client 配置的租户；AK/SK 认证时使用应用的 `authTenantId`，未配置则使用该应用的归属租户。它表示身份认证后的默认业务租户。

`TenantContextHolder.getCurrentTenantId()` 是独立的临时执行上下文。设置它不改变 JWT、当前用户名或角色，也不会改变应用的归属租户。MyBatisPlus 在临时值存在时优先使用临时值，因此查询的实际租户可能不同于 `SecurityUtils.getTenantId()`。

需要跨租户操作时，先验证当前身份是否允许访问目标租户，再设置临时值，并在完成后恢复或清除。后端不能仅凭调用方传入的 `tenantId` 认定其有权限；具体作用范围与代码见 [MyBatisPlus 租户插件](/docs/latest/01_services/框架基础/mybatisplus/#租户插件)。

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

### @Passkey：Controller 参数资源凭证

{{< process-diagram name="passkey-sequence" title="Passkey 时序图：业务过滤列表、响应签发、携带凭证与 Controller 参数验证" >}}

先按时序理解三个阶段，再看下面的 DTO 与接口示例：

1. **列表阶段**：业务先限定资源可见范围，Web 响应处理调用签发器。
2. **请求阶段**：前端携带选中资源的 ID 和对应凭证，沿用登录身份。
3. **校验阶段**：绑定参数后验证身份、资源、签名和有效期；失败时 Controller 不执行。

列表 DTO 实现 `PasskeyResource`，框架自动填充 passkey；后续请求通过 Controller 参数上的 `@Passkey` 校验。接口定义如下：

```java
package dev.macula.boot.security;

import com.fasterxml.jackson.annotation.JsonIgnore;

public interface PasskeyResource {
    @JsonIgnore
    String getResourceId();

    String getPasskey();

    void setPasskey(String passkey);
}
```

列表 DTO 示例，`getResourceId()` 返回全局唯一且稳定的订单编号：

```java
import dev.macula.boot.security.PasskeyResource;
import lombok.Data;

@Data
public class OrderListItem implements PasskeyResource {
    private String orderId;
    private String orderName;
    private String passkey;

    @Override
    public String getResourceId() {
        return orderId;
    }
}
```

Lombok 生成 `getPasskey()` 和 `setPasskey(...)`；`passkey` 由框架在列表响应时填充。下方 `UpdateOrderRequest` 提供 `getOrderId()`。

#### 1. 查询已授权列表

```java
@PreAuthorize("isAuthenticated()")
@GetMapping("/orders")
public List<OrderListItem> list() {
    // 业务查询必须先按当前用户的数据权限过滤，再由响应 Advice 自动填充 passkey。
    return orderService.listVisibleTo(SecurityUtils.getCurrentUser());
}
```

响应示例（passkey 仅为示意值）：

```json
{
  "data": [
    {
      "orderId": "order-1001",
      "passkey": "v1.<过期时间>.<签名>"
    }
  ]
}
```

#### 2. 前端携带列表中的凭证

从列表选中记录后，携带其 `orderId` 和 `passkey`，沿用现有登录认证。以下方式二选一。

URL Query 参数：

```http
GET /orders/order-1001?passkey=<该记录的passkey，经URL编码>
```

Header（推荐）：

```http
GET /orders/order-1001
X-Resource-Passkey: <该记录的passkey>
```

JSON 请求体只传业务数据，凭证仍放在 Header 或 URL Query 中。

#### 3. 后端使用参数级 @Passkey

```java
import dev.macula.boot.starter.security.annotation.Passkey;

// 参数本身就是资源编号。
@GetMapping("/orders/{orderId}")
public OrderDetail detail(@PathVariable("orderId") @Passkey String orderId) {
    return orderService.getDetail(orderId);
}

// 从绑定完成的 DTO 中读取 orderId；嵌套属性可以写 @Passkey("order.id")。
@PreAuthorize("@pms.hasPermission('order:update')")
@PostMapping("/orders/update")
public void update(@RequestBody @Valid @Passkey("orderId") UpdateOrderRequest request) {
    orderService.update(request);
}
```

参数注解的写法与限制：

- 参数直接是资源 ID：使用 `@Passkey`。
- 参数为 DTO：使用 `@Passkey("orderId")`，嵌套属性如 `order.id`，通过 JavaBean getter 读取。
- 值是属性路径，不是 SpEL；不使用 `#p0`、`#p0.orderId` 或 `returnObject`。
- 资源编号只支持非空字符串或整数；注解放在 MVC Controller 参数上。
- 请求体示例的 `@Valid` 使用 `jakarta.validation.Valid`。

#### 配置与使用边界

签发与验证的启用配置见本页[使用配置](#使用配置)。

| 配置 | 默认 | 含义 |
| --- | --- | --- |
| `macula.security.passkey.enabled` | `false` | 开启资源凭证；关闭时列表正常返回且不签发，默认服务及 Clock 不装配；标注 Passkey 的请求参数拒绝，标准 PostAuthorize 独立工作 |
| `macula.security.passkey.ttl` | `5m` | 正数且至少 1 秒的凭证有效期 |
| `macula.security.passkey.secret-base64` | 无 | Base64 编码、解码后至少 32 字节的独立服务端密钥 |

- 列表必须先完成业务数据权限过滤。Web Starter 的响应 Advice 支持 Collection、PageVO、成功 Result 和 ResponseEntity 中的列表；单对象不自动签发。
- 各实例使用同一独立签名密钥，默认采用 HMAC-SHA256；可用 `PasskeyService` Bean 替换签发与验证。
- 凭证只从 Header/Query 读取，不读取表单或 DTO 字段；重复、冲突和空值拒绝。使用现有异常 Advice 时，凭证拒绝返回 HTTP 403/A0312。
- 仅保护 MVC Controller 请求；操作权限和返回值鉴权分别使用 `@PreAuthorize`、`@PostAuthorize`。凭证到期前可复用，不能代替业务状态、租户或实时权限检查。

### 组合规则与边界

- `@PreAuthorize` 检查操作权限，`@PostAuthorize` 检查实际返回值归属；这两类方法注解通过 Spring Bean 代理生效，同类自调用不经过代理。
- `@Passkey` 在 MVC 参数绑定后、Controller 执行前校验列表资源凭证；不用于 Service 代理、WebFlux 或后台任务，不代替登录认证。
- 网关放行、ROOT / ADMIN 角色不代表自动通过资源凭证校验。列表、分页、统计和导出仍须在查询条件中落实用户、租户和数据范围。
- 凭证到期前可复用；授权变化不会自动撤销已有凭证，签名不包含租户或 action，写操作仍应检查实时业务状态与权限。

实际应用组织参见 [Samples 模块说明](/docs/latest/04_devmanual/模块说明/)和[示例配置](/docs/latest/04_devmanual/模块说明/#示例配置)。

### 验证与排障

| 检查 | 预期与定位方法 |
| --- | --- |
| 身份与方法权限 | 分别使用有效身份、过期 Token、无角色身份调用同一业务入口；确认拒绝发生在写入之前。 |
| PMS 权限 | 调用带操作权限表达式的方法，分别授予 / 撤销对应权限；角色校验成功不代表 PMS 按钮权限也成功。 |
| 资源凭证 | 用有效列表凭证、缺失凭证、过期凭证及另一用户 / 资源的凭证请求同一 Controller；失败时方法不执行。关闭 Passkey 后确认列表不签发、带注解参数仍拒绝。 |
| 资源范围 | 用两个真实用户验证列表查询范围与单资源归属；Passkey 验证通过不能替代列表、租户及业务状态约束。 |
| 方法未被拦截 | 核对目标是否 Spring Bean、是否经过代理、注解声明的位置及调用方式，再看认证上下文，不能直接改成匿名放行。 |

## 依赖引入

以下为组件 POM 的直接依赖（不含测试依赖），用于了解依赖组成；引入上方 Starter 后由 Maven 传递解析，无需在应用中逐项重复声明。版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>

<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>oauth2-oidc-sdk</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
