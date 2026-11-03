---
aliases: ["/docs/01_services/框架基础/security/"]
title: "Macula Boot Starter Security"
linkTitle: "Security"
weight: 10
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "5.x"
source_commit: "8c57d381e86905e0b73d456ce012c9dd3e37dd54"
source_paths: ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Inner.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/aspect/SecurityInnerAspect.java", "macula-boot-starters/macula-boot-starter-system/src/main/java/dev/macula/boot/starter/system/service/PermissionService.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "5.x", "commit": "8c57d381e86905e0b73d456ce012c9dd3e37dd54", "paths": ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Inner.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/aspect/SecurityInnerAspect.java", "macula-boot-starters/macula-boot-starter-system/src/main/java/dev/macula/boot/starter/system/service/PermissionService.java"]}]
---

## 概览

Security Starter 运行在 BFF 和业务微服务中：验证网关 JWT、建立 Spring Security 认证上下文，并在业务方法上执行细粒度授权。网关的认证与 URL 控制见 [Gateway](/docs/5.x/01_services/微服务/gateway/)。

## 组件坐标

继承 Macula Boot 5.x Parent 时版本由父 POM 管理。以下 Passkey 用法以包含参数级注解的 5.x 制品为准，已有项目需确认实际依赖版本。

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
          jwk-set-uri: http://127.0.0.1:9000/oauth2/jwks
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

| 配置 | 默认 | 含义 |
| --- | --- | --- |
| `macula.security.passkey.enabled` | `false` | 开启资源凭证；关闭时列表正常返回且不签发，默认服务及 Clock 不装配；标注 Passkey 的请求参数拒绝，标准 PostAuthorize 独立工作 |
| `macula.security.passkey.ttl` | `5m` | 正数且至少 1 秒的凭证有效期 |
| `macula.security.passkey.secret-base64` | 无 | Base64 编码、解码后至少 32 字节的独立服务端密钥 |

#### JWT 验签配置

BFF 与业务服务使用本应用网关实际提供的公钥集。上例的地址为本机示例；容器或集群中应改为后端能够访问的网关地址。

| 配置 | 含义 |
| --- | --- |
| `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` | 网关 JWK 公钥集，用于验证内部 JWT |
| `jwt.public-key-location` | 同一 Spring Security JWT 前缀下的本地 RSA 公钥替代方式 |
| `jwt.issuer-uri` | 同一前缀下按 issuer 发现验签配置，目标必须与实际签发方式相符 |
| `jwt.jws-algorithms` | JWK / 公钥方式允许的签名算法，Boot 默认 RS256 |
| `macula.security.ignore-urls` | 合并内置白名单和 Inner 路径的放行配置 |

明确选择与网关对应的验签方式，不混用不同密钥模式。模块保留无 JWK / issuer / 公钥且无自定义 JwtDecoder 时的对称 `secret` 兼容模式；接入网关时显式配置 JWK，不依赖公开默认值。

## 核心功能

<span id="securityutils"></span>

### SecurityUtils：读取认证上下文

JWT 验签后建立认证上下文，业务可以读取：

| 方法 | 信息 |
| --- | --- |
| `getCurrentUser()` | 当前认证名，默认来自 JWT 的 sub |
| `getNickname()` | 当前用户昵称 / 姓名声明 |
| `getTokenId()` | 当前 JWT 的 jti |
| `isRoot()` | 当前身份是否包含 ROOT 角色 |
| `getRoles()` | 角色 Code，去掉 ROLE_ 前缀 |
| `getTenantId()` | Token 声明中的租户 |
| `getDeptId()` / `getDataScope()` | 部门与数据范围声明 |
| `getTokenAttributes()` | 已解析的 Token 声明 |

`SecurityUtils` 是信息读取工具，不会自动校验按钮、资源归属或过滤数据库查询。AK/SK / API Key 的认证名可能是应用标识，不能直接当作登录用户。

<span id="鉴权支持"></span>

### @PreAuthorize：执行前授权

Starter 已通过 `@EnableGlobalMethodSecurity(prePostEnabled = true)` 开启方法安全。常见表达式：

| 表达式 | 检查什么 |
| --- | --- |
| `hasRole('ADMIN')` | ROLE_ADMIN 角色，不写 ROLE_ 前缀 |
| `hasAuthority('ROLE_ADMIN')` | 精确的角色权限字符串 |
| `hasAuthority('SCOPE_orders.read')` | JWT scope/scp 转换得到的权限 |
| `@pms.hasPermission('order:cancel')` | 平台登记的按钮 / 操作权限标识 |

默认 JWT 转换器将 authorities 声明转为 `ROLE_` 权限，将 scope/scp 转为 `SCOPE_` 权限。直接写 `hasAuthority('order:cancel')` 不会自动查询平台按钮权限。

使用 PMS 表达式时，应用还需引入 System Starter，配置 `macula.cloud.endpoint`、`app-key`、`secret-key`，使 `pms` Bean 能获取当前用户的按钮权限。具体接入见 [System Starter](/docs/5.x/01_services/通用平台/system/)。

```java
@PreAuthorize("@pms.hasPermission('order:cancel')")
public void cancel(String orderId) {
    orderService.cancel(orderId);
}
```

`order:cancel` 是业务在平台登记的操作标识。前端可用它控制按钮显示，后端使用注解验证操作权限；仅隐藏按钮不能替代后端检查。

<span id="返回值鉴权-postauthorize"></span>

### @PostAuthorize：根据真实结果检查

适用于同步、无副作用的查询。以下为业务示意，OrderView 提供 ownerUsername 属性，使用与认证名相同的标识体系：

```java
@PreAuthorize("isAuthenticated()")
@PostAuthorize("returnObject != null and returnObject.ownerUsername == authentication.name")
public OrderView getById(String orderId) {
    return orderRepository.findViewById(orderId);
}
```

这发生在方法返回后。表达式针对方法实际返回值；若方法返回 Result，按实际 data 层访问属性，后续 Advice 包装不属于方法返回值。ADMIN / ROOT 是否放行由业务表达式决定。检查失败拒绝返回，但不能撤销已经发生的写入、消息或其他副作用；写操作的权限在执行前检查。标准方法鉴权异常沿用 Spring Security / 业务异常处理，不自动套用 Passkey 的 HTTP 403 / A0312 映射。

### @Passkey：Controller 参数资源凭证

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

`@Passkey` 校验当前用户、资源编号、签名和有效期，失败时 Controller 不执行。编号支持非空字符串或整数，DTO 属性通过 JavaBean getter 读取。`@Passkey("orderId")` 是属性路径，不是 SpEL；不能写 `#p0`、`#p0.orderId` 或 `returnObject`，也不标在 Service 方法上。请求体示例的 `@Valid` 使用 `javax.validation.Valid`。

#### 配置与使用边界

签发与验证配置及默认值见本页[使用配置](#使用配置)。需要同时接入 Web Starter 的响应签发与 Security 的参数验证；单独引入 Security 不会自动为列表签发。

- 列表必须先完成业务数据权限过滤。Web Starter 的响应 Advice 支持 Collection、PageVO、成功 Result 和 ResponseEntity 中的列表；单对象不自动签发。
- 各实例使用同一独立签名密钥，默认采用 HMAC-SHA256；可用 `PasskeyService` Bean 替换签发与验证。
- 凭证只从 Header/Query 读取，不读取表单或 DTO 字段；重复、冲突和空值拒绝。使用现有异常 Advice 时，凭证拒绝返回 HTTP 403/A0312。
- 仅保护 MVC Controller 请求；操作权限和返回值鉴权分别使用 `@PreAuthorize`、`@PostAuthorize`。凭证到期前可复用，不能代替业务状态、租户或实时权限检查。

<span id="内部接口注解inner"></span>

### @Inner：内部接口访问

`@Inner` 将内部接口路径加入认证放行范围，再由内部调用切面检查请求头 `from=Y`。下面保留平台菜单接口的调用示例；实际使用时按业务定义接口与返回类型。

该请求头只是内部来源标记，外部调用方也可伪造；应通过网关规则、网络隔离等限制此类接口的可达性，不把 Header 本身当作可信身份或权限。

```java
@FeignClient(value = "macula-cloud-system", url = "${macula.cloud.endpoint}", contextId = "systemFeignClient",
    configuration = FeignClientConfiguration.class)
public interface SystemFeignClient {
    @GetMapping(value = "/system/api/v1/menus/routes", headers = SecurityConstants.HEADER_FROM_IN)
    List<RouteVO> listRoutes();
}

public class TestController {
    @Operation(summary = "路由列表")
    @GetMapping("/api/v1/menus/routes")
    @Inner
    public List<RouteVO> listRoutes() {
        return systemService.listRoutes();
    }
}
```

### 组合规则与边界

- `@PreAuthorize` 检查操作权限，`@PostAuthorize` 检查实际返回值归属；这两类方法注解通过 Spring Bean 代理生效，同类自调用不经过代理。
- `@Passkey` 在 MVC 参数绑定后、Controller 执行前校验列表资源凭证；不用于 Service 代理、WebFlux 或后台任务，不代替登录认证。
- 网关放行、ROOT / ADMIN 角色不代表自动通过资源凭证校验。列表、分页、统计和导出仍须在查询条件中落实用户、租户和数据范围。
- 凭证到期前可复用；授权变化不会自动撤销已有凭证，签名不包含租户或 action，写操作仍应检查实时业务状态与权限。

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
    <artifactId>spring-boot-starter-aop</artifactId>
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

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/5.x/LICENSE)。第三方组件遵循各自许可证；[oauth2-oidc-sdk 许可](https://github.com/hidglobal/oauth-2.0-sdk-with-openid-connect-extensions/blob/master/LICENSE.txt)。
