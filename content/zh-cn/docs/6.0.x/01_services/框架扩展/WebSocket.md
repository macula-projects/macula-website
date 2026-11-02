---
title: "Macula Boot Starter for WebSocket"
linkTitle: "WebSocket"
weight: 22
source_path: "macula-boot-starters/macula-boot-starter-websocket/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-websocket/README.md"]
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
---

## 概览

该模块基于Spring Boot Websocket搭建，支持基于STOMP协议的Websocket通讯，通过Redis Pub/Sub实现Websocket跨实例通讯。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-websocket</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用配置

该分支 README 未提供独立配置示例；接入时核对该分支的 WebSocket 自动配置、STOMP 端点与 Redis 连接配置。

## 核心功能

支持基于 STOMP 的 WebSocket 通信，并通过 Redis Pub/Sub 在多个应用实例之间传递消息。

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-redis</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-security</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-messaging</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-feign</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
