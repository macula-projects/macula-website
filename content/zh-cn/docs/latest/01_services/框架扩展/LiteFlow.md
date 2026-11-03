---
title: "Macula Boot Starter LiteFlow"
linkTitle: "流程引擎"
weight: 10
source_path: "macula-boot-starters/macula-boot-starter-liteflow/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-liteflow/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

该模块基于[LiteFlow](https://liteflow.yomahub.com/)，是一个轻量，快速，稳定可编排的组件式规则引擎。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-liteflow</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。不同应用、文件或替代方案分别标注，请按场景选用。

#### application.yml：基本配置

```yaml
liteflow:
  #规则文件路径
  rule-source: config/flow.el.xml
  #-----------------以下非必须-----------------
  #liteflow是否开启，默认为true
  enable: true
  #liteflow的banner打印是否开启，默认为true
  print-banner: true
  #zkNode的节点，只有使用zk作为配置源的时候才起作用，默认为/lite-flow/flow
  zk-node: /lite-flow/flow
  #上下文的最大数量槽，默认值为1024
  slot-size: 1024
  #FlowExecutor的execute2Future的线程数，默认为64
  main-executor-works: 64
  #FlowExecutor的execute2Future的自定义线程池Builder，LiteFlow提供了默认的Builder
  main-executor-class: com.yomahub.liteflow.thread.LiteFlowDefaultMainExecutorBuilder
  #自定义请求ID的生成类，LiteFlow提供了默认的生成类
  request-id-generator-class: com.yomahub.liteflow.flow.id.DefaultRequestIdGenerator
  #并行节点的线程池Builder，LiteFlow提供了默认的Builder
  thread-executor-class: com.yomahub.liteflow.thread.LiteFlowDefaultWhenExecutorBuilder
  #异步线程最长的等待时间秒(只用于when)，默认值为15
  when-max-wait-seconds: 15
  #when节点全局异步线程池最大线程数，默认为16
  when-max-workers: 16
  #when节点全局异步线程池等待队列数，默认为512
  when-queue-limit: 512
  #是否在启动的时候就解析规则，默认为true
  parse-on-start: true
  #全局重试次数，默认为0
  retry-count: 0
  #是否支持不同类型的加载方式混用，默认为false
  support-multiple-type: false
  #全局默认节点执行器
  node-executor-class: com.yomahub.liteflow.flow.executor.DefaultNodeExecutor
  #是否打印执行中过程中的日志，默认为true
  print-execution-log: true
  #简易监控配置选项
  monitor:
    #监控是否开启，默认不开启
    enable-log: false
    #监控队列存储大小，默认值为200
    queue-limit: 200
    #监控一开始延迟多少执行，默认值为300000毫秒，也就是5分钟
    delay: 300000
    #监控日志打印每过多少时间执行一次，默认值为300000毫秒，也就是5分钟
    period: 300000
```

#### application.yml：Nacos 规则源选项

```yaml
liteflow:
  rule-source-ext-data-map:
    serverAddr: 127.0.0.1:8848
    dataId: demo_rule
    group: DEFAULT_GROUP
    namespace: your namespace id
    username: nacos
    password: nacos
```

### 关键配置

| 配置 | 说明 |
| --- | --- |
| `liteflow.rule-source` | 本地规则文件位置。 |
| `liteflow.rule-source-ext-data-map` | 使用 Nacos 规则源时的连接与数据定位参数。 |
| `liteflow.*executor* / when-*` | 线程池与并行执行选项。 |
| `liteflow.monitor.*` | 简易监控日志开关、队列容量和采样周期。 |

#### Nacos规则源配置

`liteflow-rule-nacos` 为 optional 依赖，使用 Nacos 规则源时应用需显式引入，并提供连接地址和认证信息；仅使用本地规则文件则无需引入。

引入插件后，根据所选规则源核对 `liteflow.rule-source`，不要同时保留无效的本地文件路径。

其他规则源配置可以参考[官方文档](https://liteflow.yomahub.com/pages/6fa87e/)

## 核心功能

示例：https://gitee.com/bryan31/liteflow-example

### 验证与排障

| 检查 | 预期与定位方法 |
| --- | --- |
| 执行结果 | 给一个固定规则链输入确定数据，确认组件执行顺序、上下文输出及失败节点。 |
| 规则变更 | 在测试环境验证修改规则后的实际生效方式，区分配置加载与正在执行链路的行为。 |
| 事务边界 | 跨组件和远程调用不自动成为同一数据库事务，按业务明确补偿、幂等与错误返回。 |

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>com.yomahub</groupId>
        <artifactId>liteflow-spring-boot4-starter</artifactId>
    </dependency>

    <dependency>
        <groupId>com.yomahub</groupId>
        <artifactId>liteflow-rule-nacos</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## 版权说明

- liteflow：https://github.com/dromara/liteflow/blob/master/LICENSE
