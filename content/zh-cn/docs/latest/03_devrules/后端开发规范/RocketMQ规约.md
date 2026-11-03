---
title: "RocketMQ规约"
linkTitle: "RocketMQ规约"
weight: 7
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "cd6e30827c78d267cca2f4e0d7b3a6e3dcb01617", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/阿里规范/Java开发手册(黄山版).pdf", "content/zh-cn/docs/latest/03_devrules/后端开发规范/RocketMQ规约.md"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-starters/macula-boot-starter-rocketmq/README.md", "macula-boot-starters/macula-boot-starter-rocketmq/pom.xml", "macula-boot-starters/macula-boot-starter-sender/README.md"]}]
---

消息规约需要同时覆盖生产、投递、消费、重试和补偿。发出消息或收到 Broker 确认，不等于下游业务已经完成；消费端必须按可能重复交付设计。

## 资源与命名

| 对象 | 建议示例 | 约束 |
| --- | --- | --- |
| Topic | `topic_order_event` | 按领域、消息类型、权限、容量及保留策略划分 |
| Tag | `tag_created`、`tag_cancelled` | 表示可用于订阅过滤的业务事件类别 |
| Producer Group | `pg_order` | 明确生产职责，事务消息按实际客户端规则设置 |
| Consumer Group | `cg_payment_order_event` | 同一消费职责的实例共用，不同业务职责独立 |
| 业务键 | `orderNo` 或 `eventId` | 可追踪且避免敏感原文；业务幂等标识需稳定 |

这些名称是项目建议，新资源保持团队内一致；已有生产资源不为统一前缀强制改名。不同环境通过 namespace、独立资源或独立集群隔离，不能假定启动 profile 会自动完成隔离。

一个领域可按消息语义、吞吐、顺序与生命周期需要使用多个 Topic，不规定“一服务只能一个 Topic”。同一 Consumer Group 的订阅关系和消费语义必须一致，不能让不同实例订阅互不相同的业务集合。

## 消息契约

事件名称描述已发生的业务事实，约定 `eventId`、事件类型、契约版本、业务标识、发生时间和载荷。必要的追踪上下文按组件支持方式传递，禁止将完整登录 Token 或服务端凭据作为消息上下文广播。

消息只包含消费者需要的字段，限制单条大小，避免携带大文件或完整数据库实体。修改字段、枚举及时间/数值表示时验证新旧消费者；生产端与消费端共用某个 Java 类，不等于契约可以无条件兼容。

消息键便于检索，但不能把 Broker 的消息 ID 当作唯一的业务幂等依据：一次业务事件重发时可能产生不同消息 ID，稳定的业务事件标识应由业务设计。

## 生产与本地事务

必须明确发送失败、超时和进程崩溃后的恢复路径。超时可能发生在 Broker 已接收之后，因此重发要与消费幂等一起设计；只在日志中打印异常而无恢复流程，不能满足可靠投递要求。

数据库写入与消息发布需要一致时，选择事务消息、同事务本地消息表或其他可验证的方案。不能简单“先提交数据库再发送”，也不能在发送失败后才临时写消息表并宣称覆盖全部崩溃窗口。

使用 [Sender](/docs/latest/01_services/框架扩展/sender/) 时，待发记录与业务数据在同一本地事务中写入，并提供补偿调度、重试和告警；使用 RocketMQ 事务消息时，实现真实本地事务执行及可重复的事务状态检查，不能在回查中固定返回成功。

日志记录事件 ID、业务键、Topic/Tag、发送结果与耗时，不默认记录完整消息体。单向发送缺少确认能力，只用于已明确接受丢失风险的场景。

## 消费、重试与死信

消费者处理成功后再按实际客户端协议确认。业务失败时触发可控重试，不得捕获异常后直接返回成功；重试次数、退避、不可重试错误与死信处置需要一并设计。

建议以“消费者职责 + eventId”建立持久幂等记录或等价状态约束。幂等判定与业务写入应在可保证原子性的边界内完成，避免先标记已消费、随后业务失败而永久漏处理。唯一约束冲突需区分“该事件已完成”与其他业务错误。

死信队列必须有积压与失败告警、负责人、修复和重放流程。重放保留事件标识并继续走幂等验证；不能通过重置位点或丢弃消息掩盖业务失败。允许舍弃的低价值事件须事先定义业务授权和范围。

## 顺序与并发

顺序要求按订单等业务聚合键定义，确认消息路由、队列及消费模式都支持该顺序范围；单个 Topic 不代表全局有序。失败重试、并行处理和跨 Topic 调用都可能影响观察到的顺序。

消费并发、批量、超时及流控按客户端版本和下游容量配置。增加实例数并不无限增加有效并发，仍受队列和分配方式等条件约束；不能照搬其他 SDK 的参数名。

消费逻辑避免长时间阻塞。慢依赖隔离、处理超时与可恢复的业务任务拆分应有明确边界，不能确认消息后再丢给无持久保障的内存线程池。

## Macula 接入

Starter 的坐标、配置与事务扩展见 [RocketMQ](/docs/latest/01_services/框架基础/rocketmq/)，本章不重复维护一份参数清单。当前灰度配置 `macula.rocketmq.gray.*` 的消息选择规则须先验证，再决定基线与灰度实例是否交叉消费；不要把它当作身份或数据权限隔离。

Macula 的消息转换使用 Jackson 3，第三方 RocketMQ Spring 内部可能仍需要 Jackson 2。升级时核对组件 README 和 POM，不因应用已用 Jackson 3 就随意排除第三方所需依赖。

## 验收与参考

至少验证重复交付、发送超时、业务事务回滚、消费者重启、消费后确认前崩溃、重试耗尽、死信重放和新旧契约并存。积压、最老消息等待时间、失败率、重试及死信数量应可观测。

通用实践参考 [Apache RocketMQ 官方最佳实践](https://rocketmq.apache.org/docs/bestPractice/01bestpractice/)，具体行为仍按所用客户端与 Broker 版本验证。
