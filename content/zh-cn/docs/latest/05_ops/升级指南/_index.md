---
title: "从 5.x 迁移到 latest（当前 6.1）"
linkTitle: "升级指南"
weight: 4
manual_content: true
aliases: ["/docs/6.0.x/05_ops/升级指南/"]
source_repository: "https://github.com/macula-projects/macula-boot"
source_branch: "main"
source_commit: "a0178da198a79cbbf66f7b9354d2c8711703e81e"
migration_from_branch: "5.x"
migration_from_commit: "7d8435df4d0edd59ddb6a440fc282b81fab3246d"
source_paths: ["README.md", "macula-boot-parent/pom.xml", "docs/migration/unified-observability.md", "macula-boot-starters/macula-boot-starter-observability/README.md", "macula-boot-starters/macula-boot-starter-web/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-redis/pom.xml", "macula-boot-starters/macula-boot-starter-cache/README.md", "macula-boot-starters/macula-boot-starter-mybatis-plus/pom.xml", "macula-boot-starters/macula-boot-starter-cloud/pom.xml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-starters/macula-boot-starter-task/README.md", "macula-boot-starters/macula-boot-starter-task/pom.xml"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["README.md", "macula-boot-parent/pom.xml", "docs/migration/unified-observability.md", "macula-boot-starters/macula-boot-starter-observability/README.md", "macula-boot-starters/macula-boot-starter-web/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-redis/pom.xml", "macula-boot-starters/macula-boot-starter-cache/README.md", "macula-boot-starters/macula-boot-starter-mybatis-plus/pom.xml", "macula-boot-starters/macula-boot-starter-cloud/pom.xml", "macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml", "macula-boot-starters/macula-boot-starter-task/README.md", "macula-boot-starters/macula-boot-starter-task/pom.xml"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "5.x", "commit": "7d8435df4d0edd59ddb6a440fc282b81fab3246d", "paths": ["README.md", "macula-boot-parent/pom.xml", "macula-boot-starters/macula-boot-starter-web/pom.xml", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java", "macula-boot-starters/macula-boot-starter-cache/src/main/java/dev/macula/boot/starter/cache/TwoLevelCacheProperties.java", "macula-boot-starters/macula-boot-starter-mybatis-plus/pom.xml", "macula-boot-starters/macula-boot-starter-task/pom.xml"]}]
---

本指南面向 Macula Boot **5.x** 应用，直接对照 **latest / main（当前 6.1）** 整理升级事项。目标涵盖 Java 17、Jakarta、Spring Boot 4、Jackson 3、统一可观测性和任务调度等变化。

latest 会随 main 演进。以下表格是记录在文件头中的分支提交快照；落地时选择可获取的目标制品，并核对实际依赖与配置。

## 1. 确认升级基线

| 项目 | 5.x 分支对照值 | latest / main 分支对照值 |
| --- | --- | --- |
| Macula revision | 5.0.21-SNAPSHOT | 6.1.0-SNAPSHOT |
| Java | README 标注 JDK 8+ | Java 17 |
| Spring Boot | 2.7.18 | 4.0.8 |
| Spring Framework | 5.3.x | 7.x |
| Spring Cloud | 2021.0.9 | 2025.1.3 |
| Spring Cloud Alibaba | 2021.0.6.0 | 2025.1.0.0 |
| Jackson 数据绑定 API | Jackson 2 | Jackson 3 |
| Springdoc | 1.7.0 | 3.1.1 |
| MyBatis Plus | 3.5.7 | 3.5.17 |
| Redisson | 3.25.2 | 4.7.0 |

SNAPSHOT 是开发标识，不表示已经正式发布。统一由 Macula Boot Parent 管理配套版本，清理业务 POM 中对旧 Boot、Cloud、Security、Springdoc 和 Redis 适配器的覆盖；不要逐项照表手工锁定全部依赖。Java 基线为 17，无需因本次迁移强制切到 Java 21。

本页合并列出从 5.x 到最新的变化，不代表 Spring Boot 支持直接跳过所有中间适配步骤。官方建议在迁移到 Boot 4 前先完成 Boot 3.5 的适配和弃用 API 清理；可在临时升级分支分阶段验证，最终以目标 Macula 版本统一交付。参考 [Boot 3.0 迁移指南](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)与 [Boot 4.0 迁移指南](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)。

## 2. 构建环境与迁移顺序

1. 保存现有 5.x 制品、配置、依赖清单及数据库备份，建立接口和集成测试基线。
2. 将本地、CI、构建镜像和运行镜像统一到 Java 17，核对 Maven 使用的 JDK。
3. 调整 Parent 与配套 Starter，处理 Jakarta、Security、Jackson 和第三方扩展的编译及启动问题。
4. 迁移 Redis、缓存、配置中心、任务和可观测性配置，先验证一个代表性服务，再验证完整链路。
5. 在真实中间件环境完成回归后灰度发布，观察错误率、延迟、任务执行和消息积压。

```bash
java -version
mvn -version
mvn help:effective-pom
mvn dependency:tree
mvn clean verify
```

命令在业务项目中执行，使用该项目的测试配置。Macula Boot 仓库的 `mvn test` 仅运行单元测试，`mvn verify` 还运行 Failsafe 集成测试；单元测试通过不等于外部链路已验证。

## 3. Java API、Web 与安全

### 从 Java EE 迁移到 Jakarta

业务代码和第三方依赖中的 Servlet、Validation、JPA 与生命周期注解需要同步调整：

| 5.x 常见引用 | 目标引用 |
| --- | --- |
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.annotation.PostConstruct` / `PreDestroy` | `jakarta.annotation.PostConstruct` / `PreDestroy` |

不要全局替换所有 `javax.*`，JDK 的 `javax.crypto`、`javax.sql` 等包仍保留。应用自有自动配置的 `EnableAutoConfiguration` 注册由旧 `spring.factories` 条目迁移到 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`；其他用途的 `spring.factories` 条目按职责保留。

### Security、WebSocket 与 Web 容器

- 自定义 Security 配置按目标 Security 7 API 重编译；将旧 `antMatchers`、`authorizeRequests`、`@EnableGlobalMethodSecurity` 等用法迁移到当前过滤器链、`requestMatchers` 和 `@EnableMethodSecurity` 配置。旧 `WebSecurityConfigurerAdapter` 不再适用，避免与 Starter 过滤器链重复。
- WebSocket 扩展 `MessageSecurityMetaSourceCustomizer` 使用 `MessageMatcherDelegatingAuthorizationManager.Builder`，旧扩展实现需要调整。
- 5.x Web Starter 使用 Undertow，latest 使用 Boot 默认 Tomcat；检查上传、Filter、Servlet、异常处理、跨域与容器定制。
- 回归匿名白名单、JWT 验签与过期、401/403、网关身份传递和方法授权，细节见 [Security](/docs/latest/01_services/框架基础/security/)及[请求链路](/docs/latest/00_introduce/请求链路/)。

### Jackson 与接口文档

- 数据绑定 API 从 `com.fasterxml.jackson.databind` 迁移到 `tools.jackson.databind`；Boot JSON 构建器定制使用 `org.springframework.boot.jackson.autoconfigure.JsonMapperBuilderCustomizer`。
- 检查 `OperationLogDTO` 等公共模型暴露的 `JsonNode`、自定义序列化器及 HTTP / RocketMQ 消息转换。`com.fasterxml.jackson.annotation` 是共享注解包，继续保留；第三方所需的 Jackson 2 不做全局排除。
- Springdoc 从 1.x 迁移到 3.x，使用目标版本的 Starter；移除旧 `springdoc-openapi-ui` 和重复文档依赖，验证 `/v3/api-docs`、`/swagger-ui/index.html`、接口分组及网关代理路径。

## 4. Redis、缓存与数据访问

### Redis 与 Redisson

普通业务服务将原 `spring.redis.*` 连接配置迁移为 `spring.data.redis.*`，认证、TLS、Sentinel 和 Cluster 按实际部署核对：

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
```

Redis 自动配置扩展使用 `org.springframework.boot.data.redis.autoconfigure.DataRedisProperties`；Redisson 适配器改为 `redisson-spring-data-40`，移除旧 `-27` 等冲突版本。Redisson 4 的 `config` / `file` 仅支持 YAML，旧 JSON 配置和固定 `retryInterval` 分别迁移为 YAML 与 `retryDelay` 策略。

自定义 `@ConfigurationProperties` 绑定仍以项目代码为准，不机械替换业务自定义前缀。升级前用真实旧数据测试反序列化、缓存失效、分布式锁和 Leader 选举；格式变化需安排兼容窗口或定向重建。

### 多级缓存

latest 的 Cache Starter 不再依赖 Resilience4j，删除 `spring.cache.two-level.open-circuit-breaker`、`spring.cache.two-level.circuit-breaker.*` 及相关构造函数/API 使用。Redis 连接与超时故障时保留当前实例 Caffeine 能力；Pub/Sub 故障可能使其他实例的旧值持续到本地 TTL 到期。详细边界见 [Cache](/docs/latest/01_services/框架基础/cache/)。

### MyBatis Plus 与 JPA

MyBatis Plus 从 Boot 2 适配包迁移为 `mybatis-plus-spring-boot4-starter`，配套 `mybatis-plus-jsqlparser`；清理旧适配包，回归分页、租户、数据权限、字段加解密、审计填充和乐观锁。

JPA 实体使用 Jakarta 注解，自定义 Hibernate 扩展按新 API 验证 SQL、方言、关联加载和事务。数据库驱动升级不代表数据库服务器可直接升级，结构变化仍由正式数据库迁移管理。

## 5. 微服务治理与配置中心

Alibaba 应用使用 `spring.config.import` 导入 Nacos 配置，不再沿用 `bootstrap.yml` / 旧 Bootstrap Starter 的组织方式。默认导入应用和应用-profile 两个 Data ID，并保留实际命名空间、分组、凭据与刷新策略。

```yaml
spring:
  config:
    import:
      - optional:nacos:${spring.application.name}.yml?refreshEnabled=true
      - optional:nacos:${spring.application.name}-${spring.profiles.active}.yml?refreshEnabled=true
```

Tencent 应用按当前 Polaris 接入文档配置。Tencent / Tencent SCG 已排除暂未兼容当前 Springdoc 的 Polaris Contract；确需合约上报时先核对兼容版本。

main 已移除 `macula-boot-starter-cloud-tsf` 与 `macula-boot-starter-cloud-tsf-scg`。旧 TSF 应用根据部署环境选择 [Alibaba](/docs/latest/01_services/微服务/alibaba/)或 [Tencent](/docs/latest/01_services/微服务/tencent/)接入，旧用法见 [5.x TSF 文档](/docs/5.x/01_services/微服务/tsf/)。

5.x 与最新服务并行运行时，分别验证服务发现、Feign/Dubbo 协议、JWT Claims、异常响应与序列化契约，注册成功不能代替互通验证。

## 6. 任务调度迁移

5.x Task 依赖包含 XXL-JOB 与 PowerJob；latest 以 **SnailJob 1.9 Server** 为唯一任务服务端。不要假定旧服务端、调度记录和执行器配置会自动迁移。

- 新任务使用 SnailJob 原生 `@JobExecutor` / `@Retryable`。
- 旧 XXL Bean Handler 可通过内置兼容桥保留 `@XxlJob` 写法，应用移除官方 `xxl-job-core`，不再连接 XXL-JOB Admin；兼容桥只覆盖明确支持的最小 API。
- PowerJob Processor、调度计划、参数、重试和回调需明确映射到目标任务模型，再验证注册、执行、日志与结果。
- 更新 `snail-job.server.host/port`、namespace、group 和 token 等配置，验证切换期间不会重复调度。配置与兼容边界见 [Task](/docs/latest/01_services/通用平台/task/)。

## 7. 统一可观测性与异步上下文迁移

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

## 8. 验收与回退

| 范围 | 需要验证的结果 |
| --- | --- |
| 构建与启动 | Java 17 下可编译、启动，Jakarta 与第三方扩展无旧 API 冲突 |
| JSON 与消息 | 自定义序列化、DTO、HTTP 与 MQ 格式正确，灰度期间新旧服务互通 |
| Web 与安全 | Tomcat、参数校验、异常响应、跨域、JWT、方法权限和 WebSocket 正常 |
| 数据与缓存 | CRUD、事务、数据权限、旧 Redis 数据、锁与缓存失效符合预期 |
| 服务治理 | 配置导入、刷新、命名空间、注册发现、网关与远程调用正常 |
| 任务 | SnailJob 注册与执行、旧 Handler 兼容、重试和日志正常，无重复调度 |
| 可观测性 | Collector 收到指标、链路和日志，跨服务关联与异步上下文正常 |
| 回退 | 5.x 制品与配置可恢复，新写入的数据库、Redis 和 MQ 数据仍兼容 |

详细可观测性配置见 [Observability](/docs/latest/01_services/生产准备/observability/)。集成验收需连接实际数据库、Redis、MQ、注册中心、任务服务和 Collector。

回退时同时恢复 5.x 应用版本和对应配置；关闭 OTLP 导出不会恢复被移除的旧 Starter。数据库、Redis 序列化和消息格式变化不会随应用回退自动撤销，应提前验证兼容窗口和独立回退步骤。

## 参考源码

本页人工维护，README 同步不会覆盖正文；文件头记录两条分支的来源提交。

- [5.x 依赖基线](https://github.com/macula-projects/macula-boot/blob/7d8435df4d0edd59ddb6a440fc282b81fab3246d/macula-boot-parent/pom.xml)
- [latest 依赖基线](https://github.com/macula-projects/macula-boot/blob/a0178da198a79cbbf66f7b9354d2c8711703e81e/macula-boot-parent/pom.xml)
- [main README](https://github.com/macula-projects/macula-boot/blob/a0178da198a79cbbf66f7b9354d2c8711703e81e/README.md)
- [统一可观测性迁移原文](https://github.com/macula-projects/macula-boot/blob/a0178da198a79cbbf66f7b9354d2c8711703e81e/docs/migration/unified-observability.md)
- [Task 迁移与兼容边界](https://github.com/macula-projects/macula-boot/blob/a0178da198a79cbbf66f7b9354d2c8711703e81e/macula-boot-starters/macula-boot-starter-task/README.md)
