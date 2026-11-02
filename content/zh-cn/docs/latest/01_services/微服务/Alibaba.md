---
title: "Macula Boot Starter Cloud Alibaba"
linkTitle: "Alibaba"
weight: 10
source_path: "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-alibaba-gray/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-alibaba-gray/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-alibaba/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
---

## 概述

基于 Nacos 实例元数据和 Spring Cloud LoadBalancer，按 `grayversion` 标签筛选实例，再在候选实例中轮询。适用于 Alibaba 服务调用和 Spring Cloud Gateway 的服务发现路由，不提供百分比放量、用户分群或强隔离策略。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba-gray</artifactId>
    <version>${macula.version}</version>
</dependency>
```

通常直接选择 [Alibaba Starter](/docs/latest/01_services/微服务/alibaba/) 或 `macula-boot-starter-cloud-alibaba-scg`，二者已传递引入本模块，无需重复声明。单独引入时还需提供 Nacos Discovery、Spring Cloud LoadBalancer；它们在本模块 POM 中为 optional 依赖。

## 使用配置

沿用最新 [Alibaba Provider application.yml](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml) 的注册发现配置，在需要灰度发布的实例上追加：

```yaml
spring:
  cloud:
    nacos:
      discovery:
        metadata:
          grayversion: v2
```

同一服务的基线实例不配置 `grayversion`，灰度实例配置如 `v2`。samples 中已有的 `metadata.version: v1` 不是灰度匹配键，不能代替 `metadata.grayversion`。

| 配置 / 输入 | 默认值 | 说明 |
| --- | --- | --- |
| `spring.cloud.nacos.discovery.metadata.grayversion` | 未设置 | 本实例灰度标签；未设置或空串视为基线，避免使用空白字符 |
| HTTP 请求头 `grayversion` | 未设置 | 本次请求希望访问的灰度标签，使用第一个头值、精确匹配 |
| `GrayVersionContextHolder` | 当前线程未设置 | 非 `RequestDataContext` 请求从该上下文读取标签 |
| `macula.cloud.gray.enabled` | `true` | **Gateway 模块**创建灰度过滤器的开关，不是本模块开关 |
| `macula.gateway.gray.enabled` | `false` | **Gateway 模块**读取请求头并设置灰度上下文的开关 |
| `spring.reactor.context-propagation` | samples 为 `auto` | WebFlux/Gateway 上下文传播配置，不是实例筛选开关 |

需要网关灰度上下文处理时，在 [Gateway 示例](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-examples/macula-example-alibaba-gateway/src/main/resources/application.yml) 上补充：

```yaml
macula:
  cloud:
    gray:
      enabled: true
  gateway:
    gray:
      enabled: true
```

本模块没有独立的 `enabled` 属性。关闭上述网关开关既不会卸载 `GrayRoundRobinLoadBalancer`，也不会移除原始请求头；负载均衡器仍可直接读取请求中的 `grayversion`。如需停用本模块，可通过 `spring.autoconfigure.exclude` 排除 `dev.macula.boot.starter.cloud.alibaba.gray.config.GrayNacosAutoConfiguration`，并核对应用剩余的负载均衡配置。

## 核心功能

### 实例选择规则

| 请求与实例情况 | 候选实例 |
| --- | --- |
| 指定标签，存在相同标签实例 | 仅匹配标签的实例 |
| 指定标签，但没有匹配实例 | 优先基线实例 |
| 未指定标签 | 优先基线实例 |
| 上述筛选后没有候选，但注册列表非空 | 回退到全部实例，包括其他灰度实例 |
| 注册列表为空 | 返回无可用实例响应，由调用端处理 |

候选集内使用轮询，不按 Nacos 权重分配。此实现优先保持可用性：即使请求未带灰度头，只有灰度实例存活时也可能访问灰度实例，不能将其作为租户或安全隔离边界。

### 标签传播

- `RequestDataContext` 类型的负载均衡请求直接读取请求头；即使头不存在，也不会再回退读取线程上下文。其他请求类型读取 `GrayVersionContextHolder`。
- 配合 Web Starter 的 `GrayHandlerInterceptor`，Servlet 入站灰度头写入请求线程上下文，请求完成后清理；Feign Starter 的 `HeaderRelayInterceptor` 将上下文标签传递给下游。
- 实例注册时，`GrayNacosRegistrationCustomizer` 将本实例标签写入 `GrayVersionMetaHolder`。这是实例级信息，不会自动让该实例发出的所有 HTTP 调用携带相同标签。
- 异步调用需配合 [Async Starter](/docs/latest/01_services/框架基础/) 的受管执行器传播上下文；手动设置线程上下文时应在 `finally` 中清理。

以已启动的 Alibaba 示例链路为例，可发送带标签请求：

```bash
curl -H 'grayversion: v2' \
  'http://127.0.0.1:5000/consumer/api/v1/consumer/echo/demo?str=hello'
```

需在实际被调用的服务上部署并注册 `v2` 实例，再观察实例日志确认路由结果；仅返回 HTTP 成功不能证明命中灰度实例。公网入口应自行校验或重写灰度头，本模块不会验证调用者是否有权指定灰度标签。

## 依赖引入

| 依赖 | 是否传递 | 用途 |
| --- | --- | --- |
| `macula-boot-commons` | 是 | 灰度常量和上下文 |
| `spring-cloud-starter-loadbalancer` | 否，optional | 客户端实例选择 |
| `spring-cloud-starter-alibaba-nacos-discovery` | 否，optional | Nacos 服务发现与注册定制 |
| `spring-boot-starter-web` | 否，optional | 可选 Servlet 环境依赖，不会强制网关引入 MVC |

默认负载均衡 Bean 可由应用自定义的 `ReactorLoadBalancer<ServiceInstance>` 替代，需在对应 LoadBalancer 子上下文中配置。

## 版权说明

本模块遵循仓库 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/LICENSE)。


---

## 概述

基于[Spring Cloud Alibaba](https://github.com/alibaba/spring-cloud-alibaba)
的微服务开源套件[Nacos](https://nacos.io/zh-cn/)、[Sentinel](https://sentinelguard.io/zh-cn/)等搭建微服务平台。

## 组件坐标

```xml
<!-- 微服务模块依赖 -->
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba</artifactId>
    <version>${macula.version}</version>
</dependency>

        <!-- 网关模块依赖 -->
<dependency>
<groupId>dev.macula.boot</groupId>
<artifactId>macula-boot-starter-cloud-alibaba-scg</artifactId>
<version>${macula.version}</version>
</dependency>
```

## 使用配置

以下按当前 [Alibaba Provider application.yml](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-examples/macula-example-alibaba-provider1/src/main/resources/application.yml) 精简，Gateway / Consumer 使用相同的配置中心组织方式。示例值不是 Starter 默认值。

| 属性 | 示例值 / 说明 |
| --- | --- |
| `spring.profiles.active` | `@profile.active@` 由 Maven 资源过滤，默认构建 profile 为 local |
| `spring.profiles.group.docker` | `local`，Docker 复用本地配置并覆盖连接信息 |
| `spring.config.import` | 导入应用及应用-profile 两个 Nacos Data ID |
| `spring.config.nacos.*` | 示例自定义连接属性，按 profile 提供；通过占位符传入 `spring.cloud.nacos.*` |
| `spring.cloud.nacos.server-addr` / `username` / `password` | Nacos 地址与认证信息 |
| `spring.cloud.nacos.discovery.enabled` / `namespace` | 启用注册发现并显式指定命名空间 |
| `spring.cloud.nacos.discovery.metadata.version` | 示例为 `v1`，服务实例版本标签 |
| `spring.cloud.nacos.discovery.register-enabled` / `register-delayed` | 本模块延迟注册扩展，仅显式配置 `false` / `true` 时启用 |
| `spring.cloud.sentinel.transport.dashboard` / `port` | Sentinel 控制台地址 / 客户端通信端口 |
| `spring.cloud.sentinel.datasource.<名称>.nacos.*` | Sentinel 规则的 Nacos 地址、Data ID、namespace、data-type 和 rule-type |

```yaml
server:
  port: ${SERVER_PORT:5020}
spring:
  profiles:
    active: '@profile.active@'
    group:
      docker: local
  application:
    name: macula-example-alibaba-provider1
  config:
    import:
      - optional:nacos:${spring.application.name}.yml?refreshEnabled=true
      - optional:nacos:${spring.application.name}-${spring.profiles.active}.yml?refreshEnabled=true
  cloud:
    nacos:
      server-addr: ${spring.config.nacos.server-addr}
      namespace: ${spring.config.nacos.namespace}
      username: ${spring.config.nacos.username}
      password: ${spring.config.nacos.password}
      discovery:
        enabled: true
        namespace: ${spring.cloud.nacos.namespace}
        metadata:
          version: v1
---
spring:
  config:
    activate:
      on-profile: local
    nacos:
      server-addr: 127.0.0.1:${NACOS_SERVER_PORT:38848}
      namespace: ${NACOS_NAMESPACE:MACULA5}
      username: ${NACOS_USERNAME:nacos}
      password: ${NACOS_PASSWORD:nacos}
---
spring:
  config:
    activate:
      on-profile: docker
    nacos:
      server-addr: ${NACOS_SERVER_ADDR:nacos:8848}
      namespace: ${NACOS_NAMESPACE:MACULA5}
      username: ${NACOS_USERNAME:nacos}
      password: ${NACOS_PASSWORD:nacos}
```

`local` 使用 `NACOS_SERVER_PORT` 覆盖本机端口；远程地址可直接覆盖 `spring.config.nacos.server-addr`。`docker` 及共享环境使用 `NACOS_SERVER_ADDR` 提供完整地址。`dev/stg/pet/prd` 只保留配置中心连接信息，业务配置由对应 Data ID 提供；完整 Redis、Sentinel 和可观测性配置见上面的源文件。

`optional:` 仅表示导入可选，不保证注册中心等其他依赖不可用时应用仍可启动；生产环境是否允许缺失配置需明确选择。

## 核心功能

请参考[官方文档](https://sca.aliyun.com/zh-cn/)

## 依赖引入

微服务模块

```xml

<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-feign</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-loadbalancer</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.csp</groupId>
        <artifactId>sentinel-datasource-nacos</artifactId>
    </dependency>

</dependencies>
```

网关模块

```xml

<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-cloud-gateway</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-alibaba-sentinel-gateway</artifactId>
    </dependency>

    <dependency>
        <groupId>com.alibaba.csp</groupId>
        <artifactId>sentinel-datasource-nacos</artifactId>
    </dependency>
</dependencies>
```

## 版权说明

- spring-cloud-alibaba：https://github.com/alibaba/spring-cloud-alibaba/blob/2021.x/LICENSE
