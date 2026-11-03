---
title: "Macula Boot Starter Redis"
linkTitle: "Redis"
weight: 4
source_path: "macula-boot-starters/macula-boot-starter-redis/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-redis/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

该模块提供连接Redis的相关配置，使用了[redisson库](https://redisson.pro/)

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-redis</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。不同应用、文件或替代方案分别标注，请按场景选用。

#### application.yml：Spring Data 连接选项

```yaml
spring:
  data:
    redis:
      database:
      host:
      port:
      username:
      password:
      ssl:
        enabled: false
      timeout:
      cluster:
        nodes:
      sentinel:
        master:
        nodes:
```

#### application.yml：Redisson YAML 方案（与上一方案择一）

```yaml
spring:
  redis:
    redisson:
      file: classpath:redisson.yaml  # file和config选一个
      config: |
        clusterServersConfig:
          idleConnectionTimeout: 10000
          connectTimeout: 10000
          timeout: 3000
          retryAttempts: 3
          retryDelay: !<org.redisson.config.EqualJitterDelay> {baseDelay: PT1S, maxDelay: PT2S}
          reconnectionDelay: !<org.redisson.config.EqualJitterDelay> {baseDelay: PT0.1S, maxDelay: PT10S}
          failedSlaveNodeDetector: !<org.redisson.client.FailedConnectionDetector> {}
          subscriptionsPerConnection: 5
          clientName: null
          loadBalancer: !<org.redisson.connection.balancer.RoundRobinLoadBalancer> {}
          subscriptionConnectionMinimumIdleSize: 1
          subscriptionConnectionPoolSize: 50
          slaveConnectionMinimumIdleSize: 24
          slaveConnectionPoolSize: 64
          masterConnectionMinimumIdleSize: 24
          masterConnectionPoolSize: 64
          readMode: "SLAVE"
          subscriptionMode: "SLAVE"
          nodeAddresses:
          - "redis://127.0.0.1:7004"
          - "redis://127.0.0.1:7001"
          - "redis://127.0.0.1:7000"
          scanInterval: 1000
          pingConnectionInterval: 0
          keepAlive: false
          tcpNoDelay: false
        password: null
        threads: 16
        nettyThreads: 32
        codec: !<org.redisson.codec.Kryo5Codec> {}
        transportMode: "NIO"
```

#### application.yml：多连接 Redisson 方案

```yaml
spring:
  redis:
    redisson:
      one:
        config: |
          singleServerConfig:
            address: "redis://127.0.0.1:6379"
      two:
        config: |
          singleServerConfig:
            address: "redis://127.0.0.1:6380"
```

#### application.yml：多连接 Spring Data 方案

```yaml
spring:
  data:
    redis:
      one:
        host: ${REDIS_ONE_HOST:127.0.0.1}
        port: ${REDIS_ONE_PORT:6379}
      two:
        host: ${REDIS_TWO_HOST:127.0.0.1}
        port: ${REDIS_TWO_PORT:6380}
```

### 关键配置

使用时有两种方式配置，一种使用 Spring Boot 连接属性，另一种使用 Redisson YAML。具体属性如下。

| 属性 | 默认值 / 行为 | 说明 |
| --- | --- | --- |
| `spring.data.redis.host` / `port` | `localhost` / `6379` | 单机地址 |
| `spring.data.redis.database` | `0` | 数据库编号，Cluster 不支持切库 |
| `spring.data.redis.username` / `password` | 未设置 | Redis 认证信息 |
| `spring.data.redis.timeout` | 未设置时本模块使用 `10000ms` | 自动构造 Redisson 时用作建连超时 |
| `spring.data.redis.ssl.enabled` | `false` | 自动构造连接地址时启用 TLS |
| `spring.data.redis.sentinel.master` / `nodes` | 未设置 | Sentinel 主节点名称 / 哨兵地址列表 |
| `spring.data.redis.cluster.nodes` | 未设置 | Cluster 节点地址列表 |
| `spring.redis.redisson.config` | 未设置 | 内嵌 Redisson YAML，优先于 `file` |
| `spring.redis.redisson.file` | 未设置 | Redisson YAML 资源路径 |

两种命名空间有意不同；显式 Redisson YAML 与 `spring.data.redis.*` 不会逐项合并。

启用 `spring.data.redis.ssl.enabled` 时，单机、Sentinel 和 Cluster 地址都会使用 `rediss://`。
当前自动构建的 Redisson 配置不支持 Spring Boot SSL Bundle；如需自定义证书或信任库，请使用上方的
`spring.redis.redisson` YAML 配置并按 Redisson TLS 选项显式配置。

Redisson 支持单机、主从和集群，上方配置示例展示集群模式。

Macula Boot 6.1 使用 Redisson 4，`spring.redis.redisson.config` 和 `file` 仅支持 Redisson YAML 格式；
Redisson 4 已移除 JSON 配置解析。固定的 `retryInterval` 应迁移为 `retryDelay`，并显式选择延迟策略。

## 核心功能

### 默认提供的Bean

- RedissonClient
- RedissonRxClient
- RedissonReactiveClient
- RedissonConnectionFactory
- RedisTemplate
- StringRedisTemplate
- ReactiveRedisTemplate
- ReactiveStringRedisTemplate

### 多Redis源的配置-Redisson方式

先采用[配置示例](#配置示例)中的“多连接 Redisson 方案”，为每个连接提供独立配置。

然后添加配置Bean，注意其中一个要设置@Primary注解，以便给默认的RedisConnectionFactory使用

```java
public class Config {
    @Bean
    @ConfigurationProperties(prefix = "spring.redis.redisson.one")
    public RedissonProperties redissonPropertiesOne() {
        return new RedissonProperties();
    }

    @Primary
    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClientOne(ApplicationContext ctx, RedissonProperties redissonPropertiesOne) throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, null, redissonPropertiesOne);
        return Redisson.create(config);
    }

    @Bean
    @ConfigurationProperties(prefix = "spring.redis.redisson.two")
    public RedissonProperties redissonPropertiesTwo() {
        return new RedissonProperties();
    }

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClientTwo(ApplicationContext ctx, RedissonProperties redissonPropertiesTwo) throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, null, redissonPropertiesTwo);
        return Redisson.create(config);
    }
}
```

### 多Redis源的配置-Redis方式

先采用[配置示例](#配置示例)中的“多连接 Spring Data 方案”，分别填写连接属性。

然后添加配置Bean，注意其中一个要设置@Primary注解，以便给默认的RedisConnectionFactory使用

```java

@Configuration
public class Config {
    @Bean
    @ConfigurationProperties(prefix = "spring.data.redis.one")
    public DataRedisProperties redisPropertiesOne() {
        return new DataRedisProperties();
    }

    @Primary
    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClientOne(ApplicationContext ctx, DataRedisProperties redisPropertiesOne)
        throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, redisPropertiesOne, new RedissonProperties());
        return Redisson.create(config);
    }

    @Bean
    @ConfigurationProperties(prefix = "spring.data.redis.two")
    public DataRedisProperties redisPropertiesTwo() {
        return new DataRedisProperties();
    }

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClientTwo(ApplicationContext ctx, DataRedisProperties redisPropertiesTwo)
        throws Exception {
        Config config = RedissonConfigBuilder.create().build(ctx, redisPropertiesTwo, new RedissonProperties());
        return Redisson.create(config);
    }
}
```

{{% alert title="提示" color="primary" %}}

注意：如果定义多个RedisConnectionFactory，需要标识其中一个为@Primary，否则会报错。你的配置需要保证在RedissonAutoConfiguration配置前，可以使用@AutoConfigureBefore注解。同时要注意bean的方法命名与构造注入时参数名称要一致。

{{% /alert %}}

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>org.redisson</groupId>
        <artifactId>redisson-spring-data-40</artifactId>
    </dependency>

    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-jsr310</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
        <exclusions>
            <exclusion>
                <groupId>redis.clients</groupId>
                <artifactId>jedis</artifactId>
            </exclusion>
            <exclusion>
                <groupId>io.lettuce</groupId>
                <artifactId>lettuce-core</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>
```

## 版权说明

- redisson：https://github.com/redisson/redisson/blob/master/LICENSE.txt
- jackson：https://github.com/FasterXML/jackson-core/blob/master/LICENSE
