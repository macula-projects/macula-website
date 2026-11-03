---
title: "Macula Boot Starter Dubbo"
linkTitle: "Dubbo"
weight: 1
source_path: "macula-boot-starters/macula-boot-starter-dubbo/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-dubbo/README.md"]
source_branch: "main"
source_commit: "a0178da198a79cbbf66f7b9354d2c8711703e81e"
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-starters/macula-boot-starter-dubbo/README.md", "macula-boot-starters/macula-boot-starter-dubbo/pom.xml", "macula-boot-parent/pom.xml"]}]
---

## 概览

本模块接入 Dubbo RPC，适用于希望通过 Java 接口调用远程服务的应用。它不替换 Gateway / BFF 的 HTTP 接口，也不自动把 Feign 契约转换为 Dubbo 服务。当前 Parent 管理 Dubbo 3.2.19，接入前按该版本核对配置。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-dubbo</artifactId>
</dependency>
```

## 使用配置

### 本地直连配置

先用两个独立应用完成一次 RPC，再按需接注册中心。下列为不同应用的完整最小配置，不合并到同一 YAML。

提供端 `echo-provider/application.yml`：

```yaml
spring:
  application:
    name: echo-provider
  main:
    web-application-type: none
dubbo:
  application:
    name: echo-provider
    qos-enable: false
  registry:
    address: N/A
  protocol:
    name: dubbo
    port: 20880
```

消费端 `echo-consumer/application.yml`：

```yaml
server:
  port: 8082
spring:
  application:
    name: echo-consumer
dubbo:
  application:
    name: echo-consumer
    qos-enable: false
  registry:
    address: N/A
```

| 配置 | 含义 |
| --- | --- |
| `registry.address: N/A` | 此练习不依赖注册中心，由引用端显式提供目标 URL |
| `protocol.name / port` | 提供端 RPC 协议和监听端口；不是消费端 HTTP 端口 |
| `application.qos-enable` | 本地样例关闭 QoS，避免两个进程争用默认管理端口 |
| `@DubboReference` 的 url | 显式直连提供端；换成服务发现时移除硬编码 URL 并配置注册中心 |
| `timeout / retries` | 下方引用设置 2000 毫秒与 0 次重试，避免将重试误用于写操作 |

服务发现用 `dubbo.registry.address`，与 Spring Cloud 自己的注册配置分别核对。更多属性见 [Dubbo 配置参考](https://dubbo.apache.org/en/docs3-v2/java-sdk/reference-manual/config/properties/)。

## 核心功能

### 最小 RPC 调用

在自己的工程创建 `echo-api`、`echo-provider`、`echo-consumer` 三个模块，并在根 POM 聚合。API 是普通 Java 契约 JAR；提供端与消费端均引用同一业务版本的 API JAR，并引入上面的 Macula Dubbo Starter。消费端还需 [Web Starter](/docs/latest/01_services/框架基础/web/#组件坐标) 暴露验证接口。下面的模块名是接入练习，不是 Boot 或 Samples 已有目录。

`echo-api` 的 `com/example/rpc/api/EchoService.java`：

```java
package com.example.rpc.api;

/** RPC 共享接口。 */
public interface EchoService {
    String echo(String text);
}
```

`echo-provider` 的 `com/example/rpc/provider/EchoServiceImpl.java`：

```java
package com.example.rpc.provider;

import com.example.rpc.api.EchoService;
import org.apache.dubbo.config.annotation.DubboService;

/** 发布 RPC 服务。 */
@DubboService
public class EchoServiceImpl implements EchoService {
    @Override
    public String echo(String text) {
        return "rpc:" + text;
    }
}
```

同模块启动类：

```java
package com.example.rpc.provider;

import org.apache.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** 启动并扫描提供端 Dubbo 服务。 */
@EnableDubbo(scanBasePackages = "com.example.rpc.provider")
@SpringBootApplication
public class ProviderApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProviderApplication.class, args);
    }
}
```

`echo-consumer` 的启动类与本地验证入口：

```java
package com.example.rpc.consumer;

import com.example.rpc.api.EchoService;
import org.apache.dubbo.config.annotation.DubboReference;
import org.apache.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** 经 HTTP 触发一次 RPC 调用。 */
@EnableDubbo(scanBasePackages = "com.example.rpc.consumer")
@SpringBootApplication
@RestController
public class ConsumerApplication {
    @DubboReference(url = "dubbo://127.0.0.1:20880", timeout = 2000, retries = 0)
    private EchoService service;

    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class, args);
    }

    @GetMapping("/rpc/echo")
    public String echo() {
        return service.echo("hello");
    }
}
```

先启动 Provider，再启动 Consumer，执行 `curl http://127.0.0.1:8082/rpc/echo`，预期 Web Result 的业务数据为 `rpc:hello`。停掉 Provider 后调用应失败，而不是继续返回本地常量；恢复提供端后再确认调用恢复。直连机制见 [Dubbo 官方说明](https://dubbo.apache.org/en/overview/mannual/java-sdk/tasks/framework/more/explicit-target/)。

这一步验证契约、扫描、协议和远程调用，不代表已完成注册发现、认证或生产容错。当前 Parent 的 Spring Boot / Dubbo 组合还需在自己的目标环境完成启动与调用验证，不能仅凭依赖解析成功判定兼容。

### 与 Spring Cloud 的边界

本模块提供 Dubbo RPC 依赖，不会自动将 HTTP/Feign 接口转换为 Dubbo 接口。注册中心、协议及服务暴露使用 `dubbo.*`；与 Spring Cloud 共用注册中心时，仍需分别配置两套服务发现与调用方式。

Macula 的 HTTP Feign 请求头透传不能直接当作 Dubbo 上下文传递。若 RPC 也要携带身份、租户或链路，需为该协议确认相应的上下文与验证机制。POM 中可选的 `dubbo-spring-security` 不会因引入本 Starter 就自动成为业务依赖，也不代表 RPC 已具备 Gateway 的全部安全控制。

### 验证与排障

| 现象 | 核对顺序 |
| --- | --- |
| 找不到提供者 | 提供端已启动、20880 监听、接口名称与扫描包；直连时目标地址是否正确 |
| HTTP 能访问但 RPC 失败 | Consumer HTTP 端口与 Provider RPC 端口是否混用；共享契约与协议是否一致 |
| 启动阶段报配置或类兼容错误 | Parent 管理的版本、第三方 Starter 对目标 Boot 的兼容性、是否重复引入另一套 Dubbo |
| 能调用但身份丢失 | 此直连样例没有接入认证；检查真实项目的 RPC 身份及上下文方案 |
| 写操作重复执行 | 检查消费者与上游重试；在业务侧落实幂等，不依赖“重试次数少”保证唯一 |

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-commons</artifactId>
    </dependency>
    <!-- 可选集成，不会自动作为 Starter 的传递依赖引入 -->
    <!--
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-security</artifactId>
    </dependency>
    -->
</dependencies>
```

## 版权说明

- dubbo：https://github.com/apache/dubbo/blob/3.2/LICENSE
