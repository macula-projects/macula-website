---
aliases: ["/docs/01_services/框架基础/security/"]
title: "Macula Boot Starter Security"
linkTitle: "Security"
weight: 10
manual_content: true
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "5.x"
source_commit: "8c57d381e86905e0b73d456ce012c9dd3e37dd54"
source_paths: ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "5.x", "commit": "8c57d381e86905e0b73d456ce012c9dd3e37dd54", "paths": ["macula-boot-starters/macula-boot-starter-security/README.md", "macula-boot-starters/macula-boot-starter-security/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/SecurityProperties.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/annotation/Passkey.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/web/PasskeyArgumentResolverPostProcessor.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/PasskeyRequestResolver.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/passkey/HmacPasskeyService.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/advice/ControllerResponseAdvice.java"]}]
---

## 概览

该模块为安全模块，以资源服务器的角色和网关交互。

1. 资源服务器的安全依赖，支持对JWT的验证，不依赖任何认证服务器
2. 内部REST服务依赖该模块，通过JWT来获取用户信息；
3. 网关或者直接对外的REST服务通过OpaqueToken验证登陆信息
4. 网关处理入口 URL 与角色权限并生成内部 JWT；本模块解析身份，支持方法操作权限、返回值归属和 MVC 参数级资源凭证校验。

## 组件坐标

继承 Macula Boot 5.x Parent 时版本由父 POM 管理；使用已包含本次变更的 5.x 制品，不能假定旧版制品已提供 `@Passkey`。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-security</artifactId>
</dependency>
```

## 使用配置

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://127.0.0.1:9000/oauth2/jwks
macula:
  security:
    ignore-urls: []
    # 不使用资源凭证时设为 false（默认）
    passkey:
      enabled: true
      ttl: 5m
      secret-base64: ${PASSKEY_SECRET_BASE64}
```

JWK 地址使用本应用网关实际提供的公钥集。Passkey 开关、有效期与密钥约束见下文；签发端与验证端各实例使用相同的独立密钥。

## 核心功能

### SecurityUtils

```java
/**
 * {@code SecurityUtils} 安全助手
 *
 * @author rain
 * @since 2022/7/25 15:16
 */
public class SecurityUtils {

    public static String getCurrentUser() {
        if (SecurityContextHolder.getContext() != null && SecurityContextHolder.getContext()
            .getAuthentication() != null && SecurityContextHolder.getContext().getAuthentication().isAuthenticated()) {
            return SecurityContextHolder.getContext().getAuthentication().getName();
        }
        return null;
    }

    /**
     * 获取用户昵称/姓名
     *
     * @return nickname
     */
    public static String getNickname() {
        return Convert.toStr(getTokenAttributes().get(SecurityConstants.JWT_NICKNAME_KEY));
    }

    /**
     * 获取用户角色
     *
     * @return 角色Code集合
     */
    public static Set<String> getRoles() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null && CollectionUtil.isNotEmpty(authentication.getAuthorities())) {
            return authentication.getAuthorities().stream()
                .map(item -> StrUtil.removePrefix(item.getAuthority(), "ROLE_")).collect(Collectors.toSet());
        }
        return Collections.emptySet();
    }

    /**
     * 获取部门ID
     *
     * @return deptId
     */
    public static Long getDeptId() {
        return Convert.toLong(getTokenAttributes().get(SecurityConstants.JWT_DEPTID_KEY));
    }

    /**
     * 获取数据权限
     *
     * @return DataScope
     */
    public static Integer getDataScope() {
        return Convert.toInt(getTokenAttributes().get(SecurityConstants.JWT_DATASCOPE_KEY));
    }

    /**
     * 获取当前租户ID
     *
     * @return 租户ID
     */
    public static Long getTenantId() {
        return Convert.toLong(getTokenAttributes().get(GlobalConstants.TENANT_ID_NAME));
    }

    public static String getTokenId() {
        if (SecurityContextHolder.getContext() != null && SecurityContextHolder.getContext()
            .getAuthentication() instanceof JwtAuthenticationToken) {
            JwtAuthenticationToken token =
                (JwtAuthenticationToken)SecurityContextHolder.getContext().getAuthentication();
            if (token != null && token.getToken() != null) {
                return token.getToken().getId();
            }
        }
        return null;
    }

    /**
     * 判断用户是否为超级管理员
     *
     * @return true/false
     */
    public static boolean isRoot() {
        return getRoles().contains(SecurityConstants.ROOT_ROLE_CODE);
    }

    public static Map<String, Object> getTokenAttributes() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null) {
            if (authentication instanceof AbstractOAuth2TokenAuthenticationToken) {
                AbstractOAuth2TokenAuthenticationToken<?> tokenAuthenticationToken =
                    (AbstractOAuth2TokenAuthenticationToken<?>)authentication;
                return tokenAuthenticationToken.getTokenAttributes();
            }
        }
        return Collections.emptyMap();
    }
}
```

### 鉴权支持

- URL鉴权是在gateway实现的，本模块不支持URL鉴权
- 方法级别的注解鉴权：默认已经解锁 @PreAuthorize 和 @PostAuthorize 两个注解。

示例中的 `@pms.hasPermission('order:update')` 检查平台按钮 / 操作权限。使用前需引入 [System Starter](/docs/5.x/01_services/通用平台/system/)，配置 `macula.cloud.endpoint`、`app-key`、`secret-key` 并注册相应权限；单独引入 Security 不会创建 `pms` Bean。

### 返回值鉴权 @PostAuthorize

拥有者可从查询结果明确判断时，直接使用 Spring Security 的 `@PostAuthorize`。需要在查询前拦截未登录用户时，同时标注 `@PreAuthorize("isAuthenticated()")`。拥有者字段必须采用与 `authentication.name` 相同的身份标识；默认 JWT 的 name 来自 sub。

```java
@PreAuthorize("isAuthenticated()")
@PostAuthorize("returnObject != null and returnObject.buyerUsername != null and returnObject.buyerUsername == authentication.name")
public OrderView getOrder(Long orderId) {
    return orderRepository.findViewById(orderId);
}
```

表达式按方法实际返回值编写，例如包装对象可以访问 `returnObject.data?.buyerUsername`；后续 Advice 的包装不属于方法返回值。ADMIN/ROOT 是否可放行由业务表达式明确决定。返回后拒绝不能撤销写入、消息发送等副作用，不用于阻止写操作；列表数据权限仍应在查询条件中落实。标准 PostAuthorize 异常由现有 Spring Security/业务异常处理负责，不自动套用 Passkey 的 HTTP 403/A0312 映射。

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

旧 `@CheckOwner` 已移除：返回值归属改用 `@PostAuthorize`，资源凭证改用 Controller 参数上的 `@Passkey`，不能沿用旧方法注解与 SpEL。5.x 已启用 Spring Security 方法鉴权，无需再为这些示例切换到 main 的方法安全配置。

### 内部接口注解@Inner

默认情况下依赖了本模块的接口都要有token才能访问，对于一些内部接口，比如定时任务调用的接口，没有经过网关，没有token，这个时候你可以在你的Controller上的方法上加上@Inner注解。调用方需要设置请求header为`from=Y`

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

### 验证与排障

| 场景 | 预期结果 |
| --- | --- |
| 已授权列表 → 携带对应 ID 与凭证请求 | 身份、资源、签名及有效期匹配时执行 Controller |
| 缺失 / 过期 / 另一用户或资源的凭证 | Controller 不执行；使用默认异常 Advice 时返回 HTTP 403 / A0312 |
| 重复 Header / Query、两处值冲突、只在 JSON 中传凭证 | 拒绝请求；Header 与 Query 建议择一传递 |
| 关闭 Passkey 或缺少有效验证服务 | 列表不签发；带 `@Passkey` 的参数拒绝，不因关闭功能而放行 |
| 缺少操作权限或返回结果不属于当前用户 | 分别由 `@PreAuthorize`、`@PostAuthorize` 拒绝；不能用资源凭证代替 |

## 依赖引入

```xml
<dependencies>
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
        <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
    </dependency>

    <dependency>
        <groupId>com.nimbusds</groupId>
        <artifactId>oauth2-oidc-sdk</artifactId>
    </dependency>
</dependencies>
```

## 版权说明

- oauth2-oidc-sdk：https://github.com/hidglobal/oauth-2.0-sdk-with-openid-connect-extensions/blob/master/LICENSE.txt
