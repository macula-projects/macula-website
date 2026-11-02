---
title: "从 5.x 迁移到 6.0.x"
linkTitle: "升级指南"
weight: 4
manual_content: true
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
migration_from_branch: "5.x"
migration_from_commit: "beaa74b1639786306aa817bef0e522a23c995fd4"
source_paths: ["README.md", "macula-boot-parent/pom.xml", "macula-boot-starters/macula-boot-starter-cloud/pom.xml", "macula-boot-starters/macula-boot-starter-web/pom.xml", "macula-boot-starters/macula-boot-starter-redis/pom.xml", "macula-boot-starters/macula-boot-starter-task/pom.xml", "macula-boot-starters/macula-boot-starter-sleuth/pom.xml"]
---

本指南面向已经使用 Macula Boot 5.x 的应用，目标是迁移到 **6.0.x 分支**。以下结论来自上述提交的 POM、自动配置、示例和 README 对照；实际选用的补丁版本不同，应重新核对其依赖管理和变更。

6.0.x 基于 Spring Boot 3.5，属于需要重新编译和回归测试的大版本升级。本文不包含 latest / 6.1 的 Spring Boot 4、Jackson 3 和统一 OTLP Starter 改造。

## 1. 确认升级基线

| 项目 | 5.x 分支对照值 | 6.0.x 分支对照值 |
| --- | --- | --- |
| Java | README 标注 JDK 8+ | Java 17 |
| Spring Boot | 2.7.18 | 3.5.13 |
| Spring Cloud | 2021.0.9 | 2025.0.2 |
| Spring Cloud Alibaba | 2021.0.6.0 | 2025.0.0.0 |
| Spring Cloud Tencent | 1.13.2-2021.0.9 | 2.1.2.0-2025.0.2 |
| Springdoc | 1.7.0 | 2.8.14 |
| MyBatis Plus | 3.5.7 | 3.5.15 |
| Redisson | 3.25.2 | 3.52.0 |
| MySQL Connector/J | 8.0.33 | 9.5.0 |

版本表来自两分支的 `macula-boot-parent/pom.xml`，用于说明技术栈变化，不要求业务应用逐项手工指定版本。驱动升级也不表示数据库服务器可以不经兼容性验证直接升级。

建议按以下顺序推进：

1. 在现有 5.x 环境固定可回退的制品、配置与数据库备份，保存当前接口和集成测试结果。
2. 将本地、CI、构建镜像和运行镜像统一到 Java 17，核对 Maven 实际使用的 JDK。
3. 切换 Macula Parent 与配套 Starter，处理编译错误和配置迁移。
4. 先验证一个有代表性的服务，再验证网关、认证、服务调用及基础设施链路。
5. 在测试环境完成真实中间件验证后，再安排灰度发布。

Spring Boot 2.7 到 3.5 跨越多个功能版本，除 [Spring Boot 3.0 官方迁移指南](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide) 外，也应检查跳过版本的发布说明；参见 [Spring Boot 3.5 升级说明](https://docs.spring.io/spring-boot/3.5/upgrading.html)。

## 2. 调整 Maven 依赖与构建环境

业务项目继续继承 `dev.macula.boot:macula-boot-parent`，将 Parent 版本换成已确认可获取的 **6.0.x 发布版本**。本次对照分支的 `revision` 是 `6.0.1-SNAPSHOT`，它是开发版本标识，不代表 Maven Central 已发布该版本。

操作步骤：

- 检查业务 POM 中显式锁定的 Spring Boot 2、Spring Cloud 2021、Spring Security 5、旧 Springdoc、旧 Redis 适配器等版本，移除不再需要的覆盖项。
- Parent 管理的 Starter 通常不必单独写版本；若业务自行导入 BOM 或锁定版本，需要确保所有 Macula 模块来自同一条 6.0.x 版本线。
- 核对 Lombok、MapStruct、测试插件和其他注解处理器在 Java 17 下的编译结果。
- 应用自有模块或第三方 Starter 若仍只支持 Boot 2，需要一并升级；不要靠添加旧 Servlet API 包解决启动错误。

```bash
java -version
mvn -version
mvn help:effective-pom
mvn dependency:tree
mvn clean verify
```

`UnsupportedClassVersionError` 应检查运行 JDK；`NoSuchMethodError`、`ClassNotFoundException` 应优先检查混入的旧依赖及重复版本。

## 3. 将 Java EE API 迁移到 Jakarta

业务代码及其依赖库中使用 Java EE API 的部分需要同步迁移，例如：

| 旧包名 | 新包名 | 常见位置 |
| --- | --- | --- |
| `javax.servlet.*` | `jakarta.servlet.*` | Filter、拦截器、请求和响应封装 |
| `javax.validation.*` | `jakarta.validation.*` | DTO 校验注解、自定义校验器 |
| `javax.persistence.*` | `jakarta.persistence.*` | JPA Entity、Converter |
| `javax.annotation.PostConstruct` | `jakarta.annotation.PostConstruct` | Bean 初始化 |
| `javax.annotation.PreDestroy` | `jakarta.annotation.PreDestroy` | Bean 销毁 |

```java
// 迁移前
import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;

// 迁移后（替换旧 import）
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
```

不要全局替换所有 `javax.*`：JDK 提供的 `javax.crypto`、`javax.sql` 等包仍然保留。自定义 Filter、校验器或实体引用的第三方库也必须与 Jakarta API 兼容。

应用自有的自动配置若仍通过 `spring.factories` 的 `EnableAutoConfiguration` 条目注册，需要迁移到 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`，并验证自动配置发现。`spring.factories` 的其他扩展注册用途不能一并删除。

## 4. Web、认证与接口文档

### Web 与安全扩展

6.0.x 的 Web Starter **仍使用 Undertow**；不要套用 6.1 / Boot 4 改用默认 Tomcat 的迁移结论。

自定义 Spring Security 配置需要核对 Security 6 API。该分支的资源服务器使用 `SecurityFilterChain`、`requestMatchers` 和 `@EnableMethodSecurity`。如果业务代码仍使用 `WebSecurityConfigurerAdapter`、`antMatchers` 等旧配置方式，需要重写，并避免与 Starter 已创建的过滤器链重复。

重点回归：匿名白名单、JWT 验签与过期、角色和权限校验、内部调用、跨域、401/403 响应，以及网关透传身份。不要通过扩大白名单或关闭鉴权来掩盖迁移失败。

### Springdoc

Macula Springdoc Starter 已接入 `springdoc-openapi-starter-webmvc-ui`。业务不要再额外引入旧 `springdoc-openapi-ui` 1.x；自定义 Springdoc 扩展也需按 2.x API 重新编译。

启动后检查 `/v3/api-docs` 和 `/swagger-ui/index.html`，同时验证接口分组、鉴权信息和网关代理路径。Swagger/OpenAPI 注解应按业务实际依赖检查，避免同时维护两套旧文档框架。

## 5. Redis、缓存与数据访问

### Redis 配置前缀

检查原有 `spring.redis.*` 配置，迁移为 Boot 3 的 `spring.data.redis.*`。例如，下面只展示主机和端口两项的对应关系，认证、TLS、Sentinel、Cluster 等配置需要分别核对：

```yaml
# 5.x
spring:
  redis:
    host: ${REDIS_HOST:127.0.0.1}
    port: ${REDIS_PORT:6379}
```

```yaml
# 6.0.x
spring:
  data:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
```

6.0.x 的 Redis Starter 使用 `redisson-spring-data-35`，应清理业务显式引入的 `redisson-spring-data-27` 等旧适配器。自定义 `RedisConnectionFactory`、序列化器和 Redisson 配置扩展也需要回归。

6.0.x 的多级缓存仍包含 Resilience4j，仍存在 `spring.cache.two-level.open-circuit-breaker` 和 `circuit-breaker` 配置。**不要按 latest / 6.1 的迁移说明删除这些配置。**

升级前用真实旧数据验证 Redis 反序列化、缓存失效通知、分布式锁和 Leader 选举；若序列化格式发生变化，设计版本隔离或定向缓存重建，避免将 Redis 整库清空作为常规迁移步骤。

### MyBatis Plus 与 JPA

6.0.x 的 MyBatis Plus Starter 使用 `mybatis-plus-spring-boot3-starter` 与 `mybatis-plus-jsqlparser`。业务若显式引入 Boot 2 适配包，应移除冲突项。重点验证分页 SQL、租户隔离、数据权限、字段加解密、审计填充和乐观锁。

JPA 应用需要将实体注解迁移到 Jakarta，并测试生成 SQL、方言、自定义类型、关联加载和事务行为；涉及 Hibernate 的自定义扩展应单独核对其新 API。不要使用自动建表更新直接替代经过评审的数据库迁移。

本次升级的 6.0.x 仍使用 Jackson 2 的 `com.fasterxml.jackson.databind`；业务无需为此迁移到 `tools.jackson.databind`。

## 6. 微服务治理与配置中心

6.0.x 保留 Alibaba、Tencent、Gateway 及对应 SCG 组合；该分支的 Cloud 聚合模块中已不再列出 TSF 模块。使用旧 TSF Starter 的应用，应先确定继续使用 5.x 还是另行适配目标平台，不能仅修改 Parent 后假定其可用。

对照同一分支的示例核对服务名、注册中心地址、命名空间、分组、凭据和网关路由。5.x 与 6.0.x 混合运行时，需要验证 Feign/Dubbo 协议、JWT Claims、异常响应和序列化契约，不能仅以“注册成功”判断兼容。

6.0.x 的 Alibaba Starter 仍引入 `spring-cloud-starter-bootstrap`，示例仍保留 `bootstrap.yml`；不要直接照搬 latest / 6.1 删除 bootstrap、全面改写为 `spring.config.import` 的做法。也不要只因复制了示例就把命名空间改成示例值，应先确认业务配置实际存放的位置。

## 7. 定时任务与链路追踪

### 任务客户端

6.0.x Task POM 管理的客户端包含 XXL-JOB 与 SnailJob，相关依赖为 optional，业务需按需显式引入。该分支 `TaskAutoConfiguration` 仅显式导入 `XxlJobConfiguration`；这不等于复制一份 SnailJob 配置就能完成旧任务迁移。

该分支 Task README 中仍有 PowerJob 旧说明，但 POM 已不再引入 PowerJob。原有 PowerJob Processor、调度记录和任务配置不应视为会自动迁移：应先明确目标引擎、任务映射、服务端与客户端版本，再逐项验证注册、执行、重试、日志及回调。没有迁移方案前，不应直接切换生产调度流量。

### 链路追踪

6.0.x 仍有名为 `macula-boot-starter-sleuth` 的模块，但其 POM 已使用 Micrometer Tracing 的 Brave Bridge 与 Zipkin Reporter。使用旧 Spring Cloud Sleuth API 或 `spring.sleuth.*` 配置的业务应检查并调整埋点与配置，验证 HTTP、Feign、异步线程和 MQ 的 Trace 上下文传递。

6.1 的 `macula-boot-starter-observability` 统一接入方案不属于这次 5.x → 6.0.x 升级范围。

## 8. 配置诊断与验收

迁移环境可临时添加 Spring Boot 的配置迁移器，查看被重命名或移除的配置诊断。它用于定位问题，不代替配置文件的正式修改；完成迁移后移除该依赖。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

验收时至少覆盖以下范围：

| 范围 | 需要验证的结果 |
| --- | --- |
| 构建与启动 | Java 17 下可构建并启动，无旧 API 缺失和依赖冲突 |
| API 与安全 | 参数校验、错误响应、跨域、白名单、权限和令牌行为符合预期 |
| 数据 | 真实数据库中的 CRUD、事务、租户与数据权限正常 |
| Redis | 旧数据兼容、缓存失效和分布式锁正常 |
| 治理与消息 | 注册发现、配置刷新、服务调用、网关、MQ 生产消费正常 |
| 运维 | 任务注册与执行、日志、指标、Trace 和健康检查正常 |
| 回退 | 旧制品与旧配置可恢复，共享数据库及消息格式兼容性已核对 |

在 Macula Boot 仓库验证时，`mvn test` 只运行单元测试，`mvn verify` 还会运行 Failsafe 集成测试。业务应用应检查自己的测试插件配置；外部 Redis、数据库、MQ 等未接入时，不能把单元测试通过当作完整迁移验收。

灰度期间同时观察错误率、延迟、资源使用、任务重复执行和消息积压。代码回退不一定能撤销数据库或消息格式变化，涉及这些变化时应提前安排兼容窗口和独立回退步骤。

## 参考源码

本页为人工维护的跨分支迁移说明，参考资料如下；它不会被 README 同步工具覆盖。

- [5.x Parent 依赖基线](https://github.com/macula-projects/macula-boot/blob/beaa74b1639786306aa817bef0e522a23c995fd4/macula-boot-parent/pom.xml)
- [6.0.x Parent 依赖基线](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-parent/pom.xml)
- [6.0.x Web POM](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-web/pom.xml)
- [6.0.x Redis POM](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-redis/pom.xml)
- [6.0.x 资源服务器配置](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/config/ResourceServerConfiguration.java)
- [6.0.x Cloud 模块列表](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-cloud/pom.xml)
- [6.0.x Task POM](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-task/pom.xml)
- [6.0.x Task 自动配置](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-task/src/main/java/dev/macula/boot/starter/task/config/TaskAutoConfiguration.java)
- [6.0.x Sleuth 模块实际依赖](https://github.com/macula-projects/macula-boot/blob/fbd20cfd4020734880ff4cc41f7cec95a0bfd70e/macula-boot-starters/macula-boot-starter-sleuth/pom.xml)
