---
title: "Macula Boot Starter Async"
linkTitle: "Async"
weight: 0
source_path: "macula-boot-starters/macula-boot-starter-async/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-async/README.md"]
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
---

## 概览

本模块为异步任务提供线程上下文传播。该分支使用 Alibaba TTL，`@Async` 与显式异步调用的接入方式如下。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-async</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用配置

沿用 Spring 异步线程池配置；TTL 装饰器与显式 Executor 的使用方式见“核心功能”。

## 核心功能

### @Aysnc注解支持TTL

```java
public class AsyncAutoConfiguration {
    @Bean
    public TaskDecorator ttlTaskDecorator() {
        return TtlRunnable::get;
    }
}
```

### CompletableFuture支持TTL

```java
CompletableFuture;CompletableFuture.runAsync(TtlRunnable.get(() -> {
    //... do your business
}));

CompletableFuture.supplyAsync(TtlWrappers.wrapSupplier(() -> {
    //... do your business
}));

// 建议采用下述方式与@Async共享Executor
CompletableFuture.runAsync(()-> {
        //... do your business
}), taskExecutor);
```

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>transmittable-thread-local</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context-support</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
