---
title: "服务治理Sentinel"
linkTitle: "服务治理Sentinel"
weight: 20
manual_content: true
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
source_paths: ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-alibaba/README.md", "macula-boot-starters/macula-boot-starter-cloud/pom.xml"]
---

## 概览

Sentinel 能力由 `macula-boot-starter-cloud-alibaba` 及 Alibaba SCG 组合提供。业务服务、网关和 Nacos 配置导入方式见 [Alibaba 接入](/docs/latest/01_services/微服务/alibaba/)。

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用配置

当前分支的主要配置项为：

| 配置 | 用途 |
| --- | --- |
| `spring.cloud.sentinel.transport.dashboard` | Sentinel 控制台地址 |
| `spring.cloud.sentinel.transport.port` | Sentinel 客户端通信端口 |
| `spring.cloud.sentinel.datasource.<名称>.nacos.*` | 动态规则的 Nacos 地址、Data ID、namespace、data-type 和 rule-type |

配置值应由应用环境提供；完整示例见 [Alibaba README](https://github.com/macula-projects/macula-boot/blob/3fbd28dc74d683055d27b81929971c0e45047878/macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-alibaba/README.md)。

## 核心功能

### 云接入方式

main 的云接入模块包括 Alibaba/Nacos、Tencent/Polaris 和共享 Gateway。Tencent 应用的接入方式见 [Tencent](/docs/latest/01_services/微服务/tencent/)。

平台部署见[部署 Macula 平台](/docs/latest/04_devmanual/部署macula平台/)，历史 TSF 说明保存在 [5.x 文档](/docs/5.x/01_services/微服务/tsf/)。

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-feign</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-loadbalancer</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-web-server</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-cloud-alibaba-gray</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-datasource-nacos</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
