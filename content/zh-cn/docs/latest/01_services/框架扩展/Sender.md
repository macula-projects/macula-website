---
title: "Macula Boot Starter Sender"
linkTitle: "消息发送"
weight: 8
source_path: "macula-boot-starters/macula-boot-starter-sender/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-sender/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

该模块实现了通过本地表发送事务消息到RocketMQ的功能。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-sender</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml

```yaml
macula:
  sender:
    message-table: 你的表名 # 默认是MACULA_MSG
```

### 关键配置

唯一的自有属性 `macula.sender.message-table` 默认为 `MACULA_MSG`。应用需配置业务 `DataSource`、事务管理器及 RocketMQ 生产者，并自行建表、安排补偿任务；Starter 不会自动建表或启动定时补偿。RocketMQ 配置参考 [RocketMQ 模块](/docs/latest/01_services/框架基础/rocketmq/)。

## 核心功能

事件消息首先和业务事务一起存储到本地数据库表，然后再发送给 RocketMQ。

业务事务提交后发送消息；发送失败由补偿任务重试。消费端仍需幂等处理，不能将该机制视为消息只投递一次。

使用前，需要在你的业务库中创建如下表（建议定期归档）：

```sql
create table MACULA_MSG
(
    id           bigint auto_increment primary key,
    orderly      tinyint      not null comment '是否为顺序消息',
    topic        varchar(64)  not null comment 'MQ topic',
    sharding_key varchar(128) not null comment 'ShardingKey，用于选择不同的 partition',
    tag          varchar(128) not null comment 'Message Tag 信息',
    msg_id       varchar(64)  not null comment 'Msg ID 只有发送成功后才有数据',
    msg_key      varchar(64)  not null comment 'MSG Key，用于查询数据',
    msg          longtext     not null comment '要发送的消息',
    retry_time   tinyint      not null comment '重试次数',
    status       tinyint      not null comment '发送状态:0-初始化，1-发送成功，2-发送失败',
    create_time  datetime     not null,
    update_time  datetime     not null,
    index        idx_update_time_status(update_time, status)
)
```

可以使用相关API进行消息处理：

- ReliableMessageSender#send 在业务方法中使用，执行可靠消息发送
- ReliableMessageCompensator#compensate 周期性调度，对未发送或发送失败的消息进行补充

```java
import cn.hutool.core.date.DateUtil;
import dev.macula.boot.starter.sender.ReliableMessageSender;
import dev.macula.boot.starter.sender.ReliableMessageCompensator;
import dev.macula.boot.starter.sender.Message;
import cn.hutool.json.JSONUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.Date;

// 在事务方法中，执行完业务逻辑后，调用MessageSender
@Service
@RequiredArgsConstructor
public class OrderService {
    private final ReliableMessageSender sender;

    private final ReliableMessageCompensator compensator;

    @Transactional
    public void createOrder(OrderDTO order) {
        doBusiness();
        sender.send(buildMessage(order));
    }

    private Message buildMessage(OrderDTO order) {
        Message message = Message.builder()
                .msg(JSONUtil.toJsonStr(order))
                .orderly(true)
                .shardingKey("123")         // 用来数据分区的，暂时没有用
                .msgKey(order.getOrderNo()) // 用订单号，发送顺序消息时有用
                .topic("test_topic")
                .tag("tag")
                .build();
        return message;
    }

    // 下面方法应由任务系统定时调度，用于未成功发送消息的补偿
    public void compensator() {
        compensator.compensate(DateUtil.offsetSecond(new Date(), -120), 100);
    }
}
```

### 验证与排障

| 检查 | 预期与定位方法 |
| --- | --- |
| 本地事务 | 业务写入与消息记录在同一本地事务中；制造业务异常后，两者都不应提交。 |
| 补偿闭环 | 模拟发送未完成，确认消息记录可被实际调度的补偿任务找到并重发；仅声明 compensator 方法不会自动调度。 |
| 重复消费 | 同一业务事件重复发送时验证消费幂等；补偿意味着可能重复，不是 exactly-once 保证。 |

## 依赖引入

```xml

<dependencies>
  <dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
  </dependency>

  <dependency>
    <groupId>org.apache.rocketmq</groupId>
    <artifactId>rocketmq-spring-boot-starter</artifactId>
  </dependency>
</dependencies>
```

## 版权说明

- 本模块代码主要来源于 [lego](https://gitee.com/litao851025/lego)。
