---
title: "框架基础"
linkTitle: "框架基础"
weight: 1
source_path: "macula-boot-commons/README.md"
source_paths: ["macula-boot-commons/README.md", "macula-boot-starters/macula-boot-starter-async/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
---

# Macula Boot Commons

提供公共返回结构、结果码、异常、常量及上下文工具，无独立 YAML 配置项。Jackson API 使用 `tools.jackson.*`，共享注解仍为 `com.fasterxml.jackson.annotation.*`；空值注解使用 JSpecify。

## 统一的返回结构

`Result<T>` 包含 `success`、`code`、`msg`、`cause` 和 `data`。业务数据使用 `data`，失败原因使用 `cause`，不要混用。

```java
Result<String> ok = Result.success("完成");
Result<Void> failed = Result.failed(ApiResultCode.BIZ_ERROR, "业务失败原因");
Result<Void> status = Result.judge(true);
```

业务可实现 `ResultCode` 定义自己的错误码。Web Starter 负责 Controller 响应包装，Commons 本身不注册 Web 处理器。

## 全局常量

| 类型 | 用途 |
| --- | --- |
| `GlobalConstants` | 请求 ID、租户、Token 和灰度标签；默认租户 ID 为 `1` |
| `SecurityConstants` | 安全相关头、权限标识和默认白名单 |
| `CacheConstants` | 框架缓存键约定 |

跨线程传递 `TenantContextHolder`、`GrayVersionContextHolder` 时配合 [Async Starter](/docs/latest/01_services/框架基础/)；业务手动设置上下文后应及时清理。

## Hutool工具类

模块传递引入 `hutool-all`，可按需使用 `StrUtil`、`CollUtil`、`DateUtil` 等工具。涉及对外 JSON 契约时优先使用应用统一的 Jackson Mapper，避免不同工具的日期、数值及空值规则不一致。

## 全局异常类

| 类型 | 用途 |
| --- | --- |
| `MaculaException` | 框架运行时异常基类 |
| `BizException` | 带业务错误码和消息的业务异常 |
| `BizCheckException` | 需要业务确认或检查的异常 |

```java
throw new BizException(ApiResultCode.BIZ_ERROR, "订单状态不允许此操作");
```

异常到 HTTP 状态及响应体的映射见 [Web Starter](/docs/latest/01_services/框架基础/web/)；异常消息中不要包含密码、凭据或内部堆栈。


## 资源访问凭证公共契约

`dev.macula.boot.security.PasskeyResource` 声明 `getResourceId()`、`getPasskey()`、`setPasskey(String)`。实现类的列表可见性必须已经由业务完成当前用户的数据权限过滤；接口实现即表示允许框架为该记录签发访问凭证。资源编号须全局唯一；接口辅助 resourceId 在 JSON 中忽略，实际业务编号和 passkey 正常输出。

`PasskeyIssuer` 是 Web 响应处理可调用的签发扩展，由安全模块实现，无需 Commons 或 Web 依赖具体认证框架。`PasskeyResources` 仅从 Collection、PageVO、成功 Result 的明确包装中提取列表资源，拒绝循环/过深结构，不遍历任意业务属性，单对象不自动签发。

`ResourceAccessDenied` 是跨模块的资源拒绝标记，`ResourceAccessException` 提供无安全库依赖的拒绝异常；现有 Web 异常 Advice 将其转换为 HTTP 403 / A0312。签名密钥、当前身份与实际验签留在 Security Starter，不放入 DTO 或公共模块。


---

## 概述

本模块提供 Spring 异步任务与定时任务的基础配置，并基于 Micrometer Context Propagation 在 Spring
托管线程池之间传播调用上下文。

主要功能包括：

- 启用 Spring `@Async` 和 `@Scheduled` 能力
- 为 Spring 托管 Executor 提供 `ContextPropagatingTaskDecorator`
- 传播 Observation、Trace、MDC、Tenant 和 GrayVersion 上下文
- 在任务执行结束后恢复工作线程原状态，避免线程复用造成上下文污染
- 支持与用户自定义的有序 `TaskDecorator` 组合使用

Macula Boot 6.1 已移除 Alibaba TTL、`TtlRunnable`、`TtlCallable` 和 `TtlWrappers`，统一使用
Micrometer Context Propagation。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-async</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用说明

本模块没有独立的 `macula.async.*` 配置。Spring Boot 自动创建的线程池使用以下属性；自行声明 Executor 时需自行应用配置与 TaskDecorator。

| 属性 | 说明 |
| --- | --- |
| `spring.task.execution.pool.core-size` / `max-size` | 异步线程池核心 / 最大线程数 |
| `spring.task.execution.pool.queue-capacity` | 异步队列容量，影响扩容与拒绝行为 |
| `spring.task.execution.thread-name-prefix` | 异步线程名前缀 |
| `spring.task.scheduling.pool.size` | 定时任务线程池大小 |
| `spring.task.scheduling.thread-name-prefix` | 定时任务线程名前缀 |
| `spring.reactor.context-propagation` | Reactor 传播模式，WebFlux/Gateway 按下文设为 `auto` |

### `@Async` 上下文传播

引入组件后，Spring Boot 管理的异步执行器会使用
`maculaContextPropagatingTaskDecorator`。调用 `@Async` 方法时，提交线程中的 Observation、Trace、
MDC、Tenant 和 GrayVersion 会传播到异步线程，并在任务完成后自动清理。

```java
@Service
public class OrderService {

    @Async
    public void processAsync(Long orderId) {
        // 当前 Trace、MDC、Tenant 和 GrayVersion 均可在此处获取
    }
}
```

### `CompletableFuture` 使用方式

使用 `CompletableFuture` 时必须显式传入同一个 Spring 托管 Executor：

```java
CompletableFuture.runAsync(() -> {
    // do your business
}, taskExecutor);
```

未指定 Executor 的 `CompletableFuture.*Async` 默认使用 JDK common pool，不会自动传播上下文。

### 原生 Executor 接入

自行创建的 `ExecutorService` 可使用 Micrometer `ContextExecutorService` 显式包装：

```java
ExecutorService executor = ContextExecutorService.wrap(
    Executors.newFixedThreadPool(4)
);

executor.submit(() -> {
    // 当前上下文可在此处获取
});
```

包装器在任务提交时捕获上下文。应用仍需按照自身生命周期管理并关闭底层 Executor。

### Reactor 上下文传播

WebFlux 和 Gateway 应开启 Reactor 自动上下文传播：

```yaml
spring:
  reactor:
    context-propagation: auto
```

开启后，已注册的 Observation、Trace/MDC、Tenant 和 GrayVersion 上下文可跨 `publishOn`、
`subscribeOn` 等线程切换恢复。

### 自定义 TaskDecorator

Starter 提供的 `TaskDecorator` 使用最高优先级。用户可以继续声明其他带 `@Order` 的
`TaskDecorator`，由 Spring Boot 按顺序组合。自行创建 Executor 时，必须显式把容器中的 Decorator
组合并应用到该 Executor，单独声明 Bean 不会自动接管任意线程池。

### 不支持自动传播的边界

以下执行方式不会自动传播上下文：

- 直接创建的 `Thread`
- 未包装的 `Executors.*`
- 未指定受管 Executor 的 `CompletableFuture.*Async`
- 第三方组件内部创建且未开放定制入口的私有线程池

这些场景应改用 Spring 托管 Executor，或通过 `ContextExecutorService.wrap(...)` 显式接入。

## 版权说明

- Spring Framework：https://github.com/spring-projects/spring-framework/blob/main/LICENSE.txt
- Spring Boot：https://github.com/spring-projects/spring-boot/blob/main/LICENSE.txt
- Micrometer Context Propagation：https://github.com/micrometer-metrics/context-propagation/blob/main/LICENSE
