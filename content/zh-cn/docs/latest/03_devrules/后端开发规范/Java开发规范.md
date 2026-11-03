---
title: "Java开发规范"
linkTitle: "Java开发规范"
weight: 1
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "cd6e30827c78d267cca2f4e0d7b3a6e3dcb01617", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/阿里规范/Java开发手册(黄山版).pdf"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["AGENTS.md", "README.md", ".editorconfig", ".idea/codeStyles/Project.xml"]}]
---

本章参考阿里《Java 开发手册》的工程实践，结合 Macula 的 Java 17、Spring 和组件约定编写。文中的“必须”“建议”表示本项目的要求，不代表逐条引用阿里原文。格式化与框架贡献要求见[贡献规范](/docs/latest/11_about/贡献规范/)。

## 命名与结构

| 对象 | 约定 | 示例 |
| --- | --- | --- |
| 包 | 小写，按业务与职责组织；Boot 源码沿用 `dev.macula...` | `com.example.order.service` |
| 类型 | 大驼峰，名称描述职责，避免无意义缩写 | `OrderService`、`OrderConverter` |
| 方法与变量 | 小驼峰；方法体现操作，布尔值避免双重否定 | `cancelOrder`、`enabled` |
| 常量与枚举项 | 大写、下划线分词；业务状态使用明确类型 | `MAX_PAGE_SIZE`、`PAID` |
| 模型 | 按用途使用 Query、Form、DTO、VO、BO、Entity | `OrderPageQuery`、`OrderCreateForm` |

必须把业务规则放在所属业务层，避免出现包揽查询、转换、远程调用和权限处理的通用“大工具类”。公开接口上的模型、枚举值、配置键和错误码均是契约，修改前核对调用方。

## 类型与对象

- 必须为可空数据选择明确的空值约定。包装类型参与计算、比较或拆箱前检查空值；集合返回空集合还是允许 `null` 要在接口上说明。
- 金额计算使用 `BigDecimal`，明确币种、精度和舍入规则；从十进制字符串或可靠的数值转换方法构造，避免从二进制浮点近似值直接构造金额。
- 业务标识、数据库列和 Java 属性的类型必须匹配。对外大整数的 JSON 表示按 API 契约固定，不在相邻接口中随意切换字符串与数字。
- 优先使用 `java.time`。绝对时间、日期和本地时间分别建模，接口时区与数据库存储策略一致；不共享可变且非线程安全的日期格式器。
- 覆盖 `equals` 时同时处理 `hashCode`；作为 Map 键或 Set 元素的对象，在参与相等性判断的字段变化后不能继续按原键使用。
- 输入 Form 与 Entity 分开。客户端不得通过批量属性复制覆盖主键、租户、拥有者、审计字段和业务状态；Converter 显式映射，可信字段在服务端赋值。

## 集合与控制流程

必须避免循环中逐条查询数据库或远程服务，优先批量查询再按键组织结果；同时限制批量规模，避免一次加载全部数据。

遍历时修改集合应使用适合的迭代器、过滤方法或独立结果集。Stream 操作保持可读，避免在 `map`、`filter` 中隐藏数据库写入或依赖执行顺序的副作用；需要短路和异常分支时可直接使用普通循环。

复杂条件拆分为有业务名称的判断；控制语句保留大括号。状态值和阈值集中定义，避免同一含义在多处散落为数字或字符串。

## 异常与日志

- 必须区分输入错误、业务拒绝和基础设施故障；业务异常使用项目错误码，不将所有失败转换为成功或空集合。
- 保留原始异常原因。捕获异常时要处理、转换或向上抛出；避免在每层重复打印同一堆栈。
- 日志使用 SLF4J 参数化方式，记录业务 ID、操作、结果和 traceId；不拼接输出整份凭据、Token、用户敏感字段或完整请求体。
- 资源使用 try-with-resources 或明确的生命周期管理。收到线程中断后正确退出或恢复中断标记，不将中断当作可无限重试的普通错误。

```java
try {
    paymentClient.confirm(orderNo);
} catch (PaymentException ex) {
    // 保留原因；由业务边界统一记录或转换，不在每层重复打印。
    throw new IllegalStateException("确认支付失败，orderNo=" + orderNo, ex);
}
```

示例只说明异常链保留方式；面向调用方的业务错误使用所属模块定义的错误码与异常类型，内部详情由统一异常处理控制。

## 并发与事务

Spring 单例 Bean 不保存单次请求的可变状态。共享状态、集合和缓存需要明确线程安全策略，不能因为使用了 Spring 就假定并发安全。

异步任务优先使用 Spring 管理的执行器，并配置容量、线程名、拒绝策略和关闭行为；不得无上限创建线程或提交任务。`CompletableFuture` 显式传入受管执行器，涉及 Trace、MDC、租户或灰度信息时按 [Async](/docs/latest/01_services/框架基础/async/) 接入上下文传播。业务手动设置的 ThreadLocal 在 `finally` 中清理。

事务放在需要原子性的业务边界，明确异常回滚策略；同类内部调用不应被当作已经经过 Spring 代理。数据库事务不跨越用户交互，避免把慢速远程调用包进长事务。外部调用成功与本地提交成功不能仅靠 `@Transactional` 保证一致，需按场景采用可靠消息、补偿或分布式事务方案。

## 注释与验证

类型 Javadoc 说明职责与重要约束；公开 API 说明参数、返回值、异常和副作用。Boot 源码的版权头、`@author`、`@since` 及 Formatter 以贡献规范为准，不用格式化后的外观代替功能测试。

提交前至少检查正常路径、边界、空值、失败、重复请求与权限拒绝。复杂 SQL、缓存、消息和外部系统协作需要相应集成验证；仅 Mock 成功不能证明真实基础设施行为正确。

## 相关资料

- [阿里规范参考资料](../阿里规范/)：手册原文与章节入口。
- [应用分层](../应用分层/)与 [API规约](../api规约/)：模型与接口边界。
- [贡献规范](/docs/latest/11_about/贡献规范/)：Boot 的编辑器格式化、Checkstyle 与验证要求。
