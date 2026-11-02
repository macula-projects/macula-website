---
title: "RocketMQ规约"
linkTitle: "RocketMQ规约"
weight: 8
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "dcd7fd36ee55ea43e17958264d0c6609455bb114", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/RocketMQ规约.md"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["pom.xml", "macula-samples-parent/pom.xml"]}]
---

以下为消息业务约定，不是当前客户端参数清单。Starter 配置以 [RocketMQ 组件](/docs/latest/01_services/框架基础/rocketmq/)及当前 POM 为准；并发、批量与重试参数须按实际客户端版本选择，不机械照搬旧参数名。消费幂等、失败重试、死信监控与业务补偿需同时设计，敏感消息体不得直接记录日志。

## 命名规范

1、【强制】Topic命名：topic+下划线+业务名，例如：订单领域topic命名为：topic_order。

2、【强制】tag命名：tag+下划线+业务动作，比如：订单创建的tag为：tag_create；订单关闭的tag为：tag_close。

3、【强制】生产者分组命名：pg+下划线+业务名,例如：订单创建生产者发送订单创建消息，那么生产者分组名为：pg_order

4、【强制】消费者分组命名：cg+下划线+业务名+下划线+订阅topic名称+下划线+订阅tag名称。

例如：订单创建消息topic为topic_order，tag为tag_create，消息生产者为订单服务，用户服务和支付服务需要消费这条消息，那么用户服务的消费者分组命名为cg_user_order_create，支付服务的消费者分组命名为cg_payment_order_create。

## 使用规范

### 生产者

2.1【强制】一个领域服务只能有一个topic。

2.2【强制】领域服务发送消息时必须根据业务动作设置tag。

2.3【强制】在Producer发送消息时必须设置keys。

2.4【强制】​消息发送成功或者失败要打印消息日志，务必要打印SendResult和key字段。

2.5【建议】消息发送失败后建议将消息存储到db，然后由定时器类线程进行定时重试，确保消息达到broker。

2.6【建议】对于可靠性要求不高的业务场景可以使用oneway消息。

2.7 【强制】新建生产者时必须指定生产者分组。

### 消费者

2.8【强制】新建消费者时必须指定消费者分组。

2.9【强制】消息消费者无法避免消息重复，所以需要业务服务来保证消息消费幂等。

2.10【建议】为了提高消费并行度，可以在同一个ConsumerGroup下启动多个Consumer实例或者通过修改ConsumeThreadMin和consumeThreadMax来提高单个Consumer的并行消费能力。

2.11【建议】为了增加业务吞吐量，可以通过设置consumer的consumeMessageBatchMaxSize来批量消费消息。

2.12 【建议】发生消息堆积时，如果业务对数据要求不高时，可以选择丢弃不重要的消息。

2.13【建议】如果消息量较少，建议在消费入口打印消息、消费耗时等，方便后续排查问题。

## 申请规范

3.1 【强制】在新建topic时必须进行申请，申请形式为：填写申请表，评审通过方可使用

## 参考

4.1 [RocketMQ最佳实践](https://github.com/apache/rocketmq/blob/master/docs/cn/best_practice.md)
