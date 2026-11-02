---
title: "从 6.0.x 迁移到 latest（当前 6.1）"
linkTitle: "升级指南"
weight: 4
manual_content: true
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
migration_from_branch: "6.0.x"
migration_from_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
source_paths: ["README.md", "macula-boot-parent/pom.xml", "docs/migration/unified-observability.md", "macula-boot-starters/macula-boot-starter-observability/README.md"]
---

本指南面向已经使用 Macula Boot **6.0.x** 的应用，目标为 **latest 对应的 main 分支（当前 6.1）**。内容整理自上述提交的 README、依赖管理和统一可观测性迁移文档。latest 会随 main 演进，实际升级时应以选定制品版本及对应提交为准。

详细升级说明统一维护在“运维指引 → 升级指南”；概述仅保留入口。从 5.x 开始升级的应用，应先参考 [5.x → 6.0.x 升级指南](/docs/6.0.x/05_ops/升级指南/)，再核对本页。

## 1. 确认升级基线

| 项目 | 6.0.x 分支对照值 | latest / main 分支对照值 |
| --- | --- | --- |
| Macula revision | 6.0.1-SNAPSHOT | 6.1.0-SNAPSHOT |
| Java | 17 | 17 |
| Spring Boot | 3.5.13 | 4.0.8 |
| Spring Framework | 6.x | 7.x |
| Spring Cloud | 2025.0.2 | 2025.1.3 |
| Jackson 数据绑定 API | Jackson 2 | Jackson 3 |
| Redisson | 3.52.0 | 4.7.0 |
| Springdoc | 2.8.14 | 3.1.1 |

以上是分支快照的对照值，不表示对应 SNAPSHOT 或所有依赖均已有正式版本发布。业务应选择已确认可获取的目标制品，按 Parent 管理依赖，检查并清理旧版本覆盖项。Java 基线仍为 17，不需要因本次升级强制切到 Java 21。

## 2. 建议迁移顺序

1. 固定可回退的 6.0.x 应用制品与配置，保存当前 API、数据库、缓存和消息链路的测试结果。
2. 更新 Parent 及配套 Starter，检查实际依赖树，处理 Boot 4、Jackson 3 与安全扩展接口的编译错误。
3. 更新 Redis、Cache、Nacos 配置和 Web 容器相关自定义项。
4. 替换可观测性依赖、日志配置及线程上下文传播方式，并准备可用的 OpenTelemetry Collector。
5. 在真实中间件测试环境验证，再灰度发布；不要将仅编译通过视为迁移完成。

```bash
java -version
mvn -version
mvn help:effective-pom
mvn dependency:tree
mvn clean verify
```

上述命令在业务项目中执行时，应使用该项目的构建配置和实际运行条件。Macula Boot 仓库中的 `mvn test` 仅运行单元测试，`mvn verify` 还运行 Failsafe 集成测试。

## 3. 源码与配置变更

Macula Boot 6.1 基于 Spring Boot 4、Spring Framework 7、Spring Cloud 2025.1 和 Jackson 3。升级应用时需要同步处理以下源码与配置变化：

- Jackson 数据绑定 API 从 `com.fasterxml.jackson.databind` 迁移到 `tools.jackson.databind`；自定义 Boot JSON 构建器改用 `org.springframework.boot.jackson.autoconfigure.JsonMapperBuilderCustomizer`。`OperationLogDTO` 暴露的 `JsonNode` 类型也相应变为 Jackson 3 类型。
- Macula 自有 Jackson 序列化代码（含 RocketMQ 消息转换链）统一使用 Jackson 3；`com.fasterxml.jackson.annotation` 是两代共享的注解包，继续保留。第三方组件所需的 Jackson 2 运行依赖不做全局排除。
- WebSocket 鉴权扩展 `MessageSecurityMetaSourceCustomizer` 的参数改为 Spring Security 7 的 `MessageMatcherDelegatingAuthorizationManager.Builder`。
- Redis 配置属性使用 `org.springframework.boot.data.redis.autoconfigure.DataRedisProperties`；Redisson 使用与 Spring Data Redis 4 对应的 `redisson-spring-data-40`。Redisson 4 的 `config`/`file` 仅支持 YAML，旧 JSON 配置和固定 `retryInterval` 需要分别迁移为 YAML 与 `retryDelay` 策略。
- Cache Starter 不再依赖 Resilience4j，删除 `spring.cache.two-level.open-circuit-breaker` 和 `spring.cache.two-level.circuit-breaker.*` 配置。Redis 可用性故障改为 fail-open：当前实例继续使用 Caffeine，但跨实例失效通知可能延迟到本地 TTL 到期。
- Springdoc 升级到 3.x；OpenAPI JSON 和 Swagger UI 地址仍分别为 `/v3/api-docs` 与 `/swagger-ui/index.html`。
- Spring Boot 4 不再提供 Undertow Starter，Web Starter 使用 Boot 默认 Tomcat。如应用依赖 Undertow 特性，需要在升级前评估替代实现。
- Alibaba 应用不再依赖 `bootstrap.yml`，通过 `spring.config.import` 导入 Nacos 配置。默认示例导入 `${spring.application.name}.yml` 和 `${spring.application.name}-${spring.profiles.active}.yml`，并保留原有地址、命名空间和凭据环境变量。

这些变化会影响实现 Macula 扩展接口、直接操作 Jackson 节点或自定义基础设施 Bean 的下游源码；升级到 6.1 时应重新编译并运行应用集成测试。

### 已移除的 TSF 接入

main 已移除 `macula-boot-starter-cloud-tsf` 与 `macula-boot-starter-cloud-tsf-scg`。现有应用需根据部署环境选择 [Alibaba](/docs/latest/01_services/微服务/alibaba/) 或 [Tencent](/docs/latest/01_services/微服务/tencent/) 接入，并调整配置中心、服务发现和网关依赖；旧版用法保存在 [5.x TSF 历史文档](/docs/5.x/01_services/微服务/tsf/)。

## 4. 统一可观测性与异步上下文迁移

### 依赖替换

删除以下依赖：

- `macula-boot-starter-prometheus`
- `macula-boot-starter-logstash`
- `macula-boot-starter-sleuth`
- `macula-boot-starter-skywalking`

统一替换为 `dev.macula.boot:macula-boot-starter-observability`。Macula Boot 6.1 不提供兼容 artifact、
旧配置别名或双运行路径。

### 配置映射

| 旧能力 | 新配置/行为 |
| --- | --- |
| `/actuator/prometheus` 与 Prometheus Pull | `management.otlp.metrics.export.url`，应用向 Collector OTLP Push |
| Sleuth/Zipkin endpoint | `management.opentelemetry.tracing.export.otlp.endpoint` |
| Brave 采样 | `management.tracing.sampling.probability` 或 OpenTelemetry sampler |
| Logstash TCP appender | `management.opentelemetry.logging.export.otlp.endpoint` |
| `logback-skywalking.xml` | Spring Boot `logging.structured.*` 加默认 OpenTelemetry Logback appender |
| SkyWalking toolkit/agent trace API | Micrometer `Tracer` 与 W3C `traceparent`/`tracestate` |
| 全量 MDC 捕获 | `macula.observability.logging.capture-mdc-attributes` 显式 allowlist |

Gateway 继续返回 `x-traceId`，但只在 Micrometer 当前 Span 有效且
`macula.gateway.trace-id-response-header-enabled=true` 时写入。

### Alibaba TTL 迁移

`com.alibaba:transmittable-thread-local` 已移除。Tenant 与 GrayVersion 的公共 Holder 方法保持不变，
底层改为普通 `ThreadLocal` 并由 Micrometer `ThreadLocalAccessor` 接入 `ContextSnapshot`。

| TTL 用法 | Micrometer/Spring 替换 |
| --- | --- |
| `TtlRunnable.get(runnable)` | Spring 受管 Executor + `ContextPropagatingTaskDecorator` |
| `TtlCallable.get(callable)` | `ContextSnapshot.wrap(callable)` |
| `TtlWrappers.wrapSupplier(...)` | 显式使用受管 Executor，或自行捕获 `ContextSnapshot` |
| `TtlExecutors.getTtlExecutorService(...)` | `ContextExecutorService.wrap(executorService)` |

`@Async`、异步事件监听器及显式传入受管 Executor 的 `CompletableFuture` 在提交时捕获
Observation、Trace/MDC、Tenant、GrayVersion，并在任务结束后恢复线程。未指定 Executor 的
`CompletableFuture.*Async`、JDK common pool、直接创建的 Thread 和第三方私有线程池不自动传播。

Reactor/WebFlux 使用：

```yaml
spring:
  reactor:
    context-propagation: auto
```

上下文传播只延续父上下文，不会为每个 Runnable 自动创建子 Span；需要独立耗时和错误信息时，
业务代码应显式创建子 Observation。

### 禁用与回退

Metrics、Traces、Logs 可分别通过各自 `enabled=false` 关闭。Spring Boot 4.0.8 没有统一的
`management.opentelemetry.enabled` 开关；同时关闭三类导出可停止 OTLP 网络发送。
`macula.observability.enabled=false` 只关闭 Macula 增量配置，不恢复已删除的旧 Starter。

6.1 的回退方式是回退应用和 Macula Boot 版本；不能在同一应用中同时依赖新 Starter 与四个旧 Starter。
升级前应搜索下游对 Brave、SkyWalking toolkit、TTL 类型、旧 Logback include 和
`/actuator/prometheus` 的直接引用。

## 5. 验收与回退

| 范围 | 需要验证的结果 |
| --- | --- |
| JSON | 自定义序列化器、DTO 节点、HTTP 和 RocketMQ 消息的 Jackson 类型及数据格式正确 |
| Web 与安全 | Tomcat 下接口、上传、异常响应、跨域和 WebSocket 授权正常 |
| Redis 与 Cache | 旧数据可读、Redisson YAML 可加载、锁与选举正常；Redis 故障时本地缓存行为及跨实例一致性边界符合预期 |
| Nacos | 主配置及环境配置均成功导入，命名空间、凭据与刷新行为正确 |
| 可观测性 | Collector 收到 Metrics、Traces、Logs；跨服务 Trace 关联与日志关联正常 |
| 异步上下文 | 受管线程池下 Trace/MDC、Tenant、GrayVersion 正确传播，任务结束后无串租户或上下文残留 |
| 运维 | 任务执行、MQ 生产消费、健康检查、资源使用和灰度错误率符合预期 |

统一可观测性的详细配置见 [Observability](/docs/latest/01_services/生产准备/observability/)。验收时需要连接实际 Redis、数据库、MQ、Nacos 和 Collector；未提供相关设施时，不应将单元测试结果写成完整链路验收通过。

升级前保留 6.0.x 的配置、依赖清单及镜像。需要回退时同时恢复应用版本和对应配置：仅关闭 OTLP 导出不会恢复被移除的旧 Starter，6.1 的新旧可观测性依赖也不能在同一应用内混用。

若升级同时涉及数据库、Redis 序列化或消息格式变化，应事先验证旧应用仍能读取灰度期间写入的数据。回退应用制品不会自动撤销这些数据变化。

## 参考源码

本页为人工维护的综合迁移指南，后续 README 同步不会覆盖正文。

- [6.0.x 依赖基线](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-parent/pom.xml)
- [latest 依赖基线](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-parent/pom.xml)
- [main README 中的升级说明](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/README.md)
- [统一可观测性迁移原文](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/docs/migration/unified-observability.md)
- [Observability Starter 配置参考](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-starters/macula-boot-starter-observability/README.md)
