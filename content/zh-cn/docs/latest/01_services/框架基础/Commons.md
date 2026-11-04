---
title: "Macula Boot Commons"
linkTitle: "Commons"
weight: -1
source_path: "macula-boot-commons/README.md"
source_paths: ["macula-boot-commons/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-commons/src/main/java/dev/macula/boot/context/TenantContextHolder.java", "macula-boot-starters/macula-boot-starter-mybatis-plus/src/main/java/dev/macula/boot/starter/mp/config/MyBatisPlusAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-commons/src/main/java/dev/macula/boot/result/Result.java", "macula-boot-commons/src/main/java/dev/macula/boot/result/ResultCode.java", "macula-boot-commons/src/main/java/dev/macula/boot/result/ApiResultCode.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyResource.java", "macula-boot-commons/src/main/java/dev/macula/boot/security/PasskeyIssuer.java", "macula-boot-commons/src/main/java/dev/macula/boot/context/TenantContextHolder.java"]}]
---

## 概览

提供公共返回结构、结果码、异常、常量及上下文工具，无独立 YAML 配置项。Jackson API 使用 `tools.jackson.*`，共享注解仍为 `com.fasterxml.jackson.annotation.*`；空值注解使用 JSpecify。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
</dependency>
```

## 使用配置

Commons 提供公共数据结构与工具契约，无独立 YAML 配置项；按下文接口在业务代码中使用。

## 核心功能

### 统一的返回结构

`Result<T>` 的字段定义如下（源码节选，省略工厂方法）。业务数据使用 `data`，失败原因使用 `cause`。完整实现见 [Result.java](https://github.com/macula-projects/macula-boot/blob/5ff9b5c8e6166449ced7512cd3bf74a672aa922e/macula-boot-commons/src/main/java/dev/macula/boot/result/Result.java)。

```java
@Data
public class Result<T> implements Serializable {

    /**
     * 响应是否成功
     */
    private boolean success;

    /**
     * 响应码
     */
    private String code;

    /**
     * 响应消息
     */
    private String msg;

    /**
     * 错误原因
     */
    private String cause;

    /**
     * 响应数据
     */
    private T data;

    // 工厂方法等省略，完整实现见下方源码链接。
}
```

```java
Result<String> ok = Result.success("完成");
Result<Void> failed = Result.failed(ApiResultCode.BIZ_ERROR, "业务失败原因");
Result<Void> status = Result.judge(true);
```

业务可实现以下 `ResultCode` 接口定义自己的错误码：

```java
package dev.macula.boot.result;

/**
 * 返回码接口
 *
 * @author pangu
 * @since 5.0.0
 */
public interface ResultCode {

    /**
     * 返回码
     *
     * @return String
     */
    String getCode();

    /**
     * 返回消息
     *
     * @return String
     */
    String getMsg();
}
```

`ApiResultCode` 的常用枚举项源码节选如下；完整枚举见 [ApiResultCode.java](https://github.com/macula-projects/macula-boot/blob/5ff9b5c8e6166449ced7512cd3bf74a672aa922e/macula-boot-commons/src/main/java/dev/macula/boot/result/ApiResultCode.java)。

```java
/**
     * 请求成功
     */
    SUCCESS("00000", "请求成功"),

    /**
     * 请求失败
     */
    FAILED("99999", "请求失败"),

    // 访问异常
    /**
     * 未授权的访问
     */
    ACCESS_UNAUTHORIZED("A0301", "未授权的访问"),

    /**
     * 访问令牌无效或已过期
     */
    TOKEN_INVALID_OR_EXPIRED("A0311", "访问令牌无效或已过期"),

    /**
     * 令牌没有访问授权
     */
    TOKEN_ACCESS_FORBIDDEN("A0312", "令牌没有访问授权"),
```

Web Starter 负责 Controller 响应包装，Commons 本身不注册 Web 处理器。

### 全局常量

| 类型 | 用途 |
| --- | --- |
| `GlobalConstants` | 请求 ID、租户、Token 和灰度标签；默认租户 ID 为 `1` |
| `SecurityConstants` | 安全相关头、权限标识和默认白名单 |
| `CacheConstants` | 框架缓存键约定 |

跨线程传递 `TenantContextHolder`、`GrayVersionContextHolder` 时配合 [Async Starter](/docs/latest/01_services/框架基础/async/)；业务手动设置上下文后应及时清理。

### Hutool工具类

模块传递引入 `hutool-all`，可按需使用 `StrUtil`、`CollUtil`、`DateUtil` 等工具。涉及对外 JSON 契约时优先使用应用统一的 Jackson Mapper，避免不同工具的日期、数值及空值规则不一致。

### 全局异常类

| 类型 | 用途 |
| --- | --- |
| `MaculaException` | 框架运行时异常基类 |
| `BizException` | 带业务错误码和消息的业务异常 |
| `BizCheckException` | 需要业务确认或检查的异常 |

```java
throw new BizException(ApiResultCode.BIZ_ERROR, "订单状态不允许此操作");
```

异常到 HTTP 状态及响应体的映射见 [Web Starter](/docs/latest/01_services/框架基础/web/)；异常消息中不要包含密码、凭据或内部堆栈。


### 资源访问凭证公共契约

`PasskeyResource` 的接口源码如下。业务须先按当前用户的数据权限过滤列表；实现接口即表示允许框架为该资源签发凭证。

```java
package dev.macula.boot.security;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * A list record whose visibility authorizes the current user to access its globally unique resource.
 * Only use this contract on lists already filtered by business data permissions.
 *
 * @author Macula
 * @since 6.1.0
 */
public interface PasskeyResource {

    /**
     * Returns a stable, globally unique resource identifier without adding an auxiliary JSON property.
     * @return resource identifier
     */
    @JsonIgnore
    String getResourceId();

    /**
     * Returns the server-issued resource access credential.
     * @return passkey, or null before issuance
     */
    String getPasskey();

    /**
     * Replaces the credential for the current response's authenticated user.
     * @param passkey server-issued credential
     */
    void setPasskey(String passkey);
}
```

`PasskeyIssuer` 为响应处理提供签发入口，安全模块实现它，Commons 与 Web 不依赖具体认证框架：

```java
package dev.macula.boot.security;

/**
 * Response processing extension for issuing a credential using a trusted current identity.
 * Implementations must reject unauthenticated calls and invalid signing configuration.
 *
 * @author Macula
 * @since 6.1.0
 */
@FunctionalInterface
public interface PasskeyIssuer {

    /**
     * Assigns a fresh credential to an already authorized list record.
     * @param resource authorized record
     */
    void issue(PasskeyResource resource);
}
```

`PasskeyResources` 只提取 Collection、PageVO、成功 Result 等明确包装内的列表资源；拒绝循环或过深结构，不遍历任意业务属性，单对象不自动签发。

`ResourceAccessDenied` 是跨模块的资源拒绝标记，`ResourceAccessException` 提供无安全库依赖的拒绝异常；现有 Web 异常 Advice 将其转换为 HTTP 403 / A0312。签名密钥、当前身份与实际验签留在 Security Starter，不放入 DTO 或公共模块。

### 验证与排障

| 检查 | 预期与定位方法 |
| --- | --- |
| 模型与 HTTP | Commons 提供 Result 等契约；Servlet 返回自动包装由 Web Starter 完成，不能仅引入 Commons 就期待所有接口被拦截。 |
| 公共异常 | 构造一个受控业务异常，通过实际使用的 Web 异常处理链验证错误码与信息，避免暴露内部堆栈。 |

### 临时租户上下文

`TenantContextHolder` 的源码如下，用于当前线程的临时租户上下文。它不修改认证租户或应用归属，也不负责目标租户授权。

```java
package dev.macula.boot.context;

/**
 * {@code TenantContextHolder} 租户ID的上下文
 *
 * @author rain
 * @since 2023/3/1 15:42
 */
public class TenantContextHolder {

    /**
     * 私有构造函数，防止实例化
     */
    private TenantContextHolder() {
    }

    private final static ThreadLocal<Long> THREAD_LOCAL_VERSION = new ThreadLocal<>();

    /**
     * 获取当前上下文租户ID
     *
     * @return 租户ID
     */
    public static Long getCurrentTenantId() {
        return THREAD_LOCAL_VERSION.get();
    }

    /**
     * 设置当前租户ID
     *
     * @param tenantId 租户ID
     */
    public static void setCurrentTenantId(Long tenantId) {
        THREAD_LOCAL_VERSION.set(tenantId);
    }

    /**
     * 清除当前租户ID
     */
    public static void clearCurrentTenantId() {
        THREAD_LOCAL_VERSION.remove();
    }
}
```

业务须先授权，再设置，并在 `finally` 中恢复原值或清除；MyBatisPlus 的租户插件优先读取此值。选择顺序和同步代码示例见 [MyBatisPlus](/docs/latest/01_services/框架基础/mybatisplus/#租户插件)。

## 依赖引入

以下为组件 POM 的直接依赖（不含测试依赖），用于了解依赖组成；引入上方 Starter 后由 Maven 传递解析，无需在应用中逐项重复声明。版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>tools.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>

<dependency>
    <groupId>org.jspecify</groupId>
    <artifactId>jspecify</artifactId>
</dependency>

<dependency>
    <groupId>io.swagger.core.v3</groupId>
    <artifactId>swagger-annotations</artifactId>
</dependency>

<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
</dependency>

<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>context-propagation</artifactId>
</dependency>

<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk18on</artifactId>
</dependency>

<dependency>
    <groupId>jakarta.validation</groupId>
    <artifactId>jakarta.validation-api</artifactId>
</dependency>

<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-annotation</artifactId>
</dependency>

<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
