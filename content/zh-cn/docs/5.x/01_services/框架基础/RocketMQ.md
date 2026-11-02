---
aliases: ["/docs/01_services/框架基础/rocketmq/"]
title: "Macula Boot Starter RocketMQ"
linkTitle: "RocketMQ"
weight: 6
---

## 概述

该模块主要依赖阿里开源的RocketMQ。[RocketMQ](https://github.com/apache/rocketmq-spring/wiki/%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C)支持同步、异步发送消息，半事务消息等，具体可以参考官方文档。



## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-rocketmq</artifactId>
    <version>${macula.version}</version>
</dependency>
```



## 核心功能

### RocketMQ最佳实践

{{% alert title="提示" color="primary" %}}

[最佳实践](https://mp.weixin.qq.com/s/Rxzo584le5XzUuI71S9nJg)

{{% /alert %}}

### 生产者配置建议
```yaml
rocketmq:
  name-server: localhost:9876
  producer:
    namespace: ${spring.profiles.active} # 建议与环境保持一致${spring.profiles.active}
    group: ${spring.application.name}    # 建议采用${spring.application.name}
    sendMessageTimeout: 300000
    enableMsgTrace: true                 # 消息轨迹开启，根据需要来决定

demo:
  rocketmq:
    stringRequestTopic: stringRequestTopic:tagA
```

```java
public class Test {
    @Resource
    private RocketMQTemplate rocketMQTemplate;
    @Value("${demo.rocketmq.stringRequestTopic}")
    private String stringRequestTopic;   // 按照最佳实践，topic一个应用保持一个topic，topic:tag，通过tag区分业务

    SendResult sendResult = rocketMQTemplate.syncSend(stringRequestTopic, "hello world");
}
```
### 消费者配置建议
#### Push模式
Push的namespace、topic等都是配置在@RocketMQMessageListener注解里面的
```yaml
rocketmq:
  name-server: localhost:9876
demo:
  rocketmq:
    stringRequestTopic: stringRequestTopic
    taga: TagA
```

```java

@SpringBootApplication
public class ConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class, args);
    }

    @Slf4j
    @Service
    @RocketMQMessageListener(topic = "${demo.rocketmq.stringRequestTopic}", selectorExpression = "${deom.rocketmq.taga}",
            namespace = "${spring.profiles.active}", consumerGroup = "${spring.application.name}")
    public class MyConsumer1 implements RocketMQListener<String> {
        public void onMessage(String message) {
            log.info("received message: {}", message);
        }
    }

    @Slf4j
    @Service
    @RocketMQMessageListener(topic = "test-topic-2", consumerGroup = "my-consumer_test-topic-2")
    public class MyConsumer2 implements RocketMQListener<OrderPaidEvent> {
        public void onMessage(OrderPaidEvent orderPaidEvent) {
            log.info("received orderPaidEvent: {}", orderPaidEvent);
        }
    }
}
```
#### Pull模式
**从RocketMQ Spring 2.2.0开始，RocketMQ Srping支持Pull模式消费，自己单线程或者多线程获取消息，实时性不高**
```yaml
rocketmq:
  name-server: localhost:9876
  consumer: # 只用于pull模式
    namespace: ${spring.profiles.active} # 建议与环境保持一致${spring.profiles.active}
    group: ${spring.application.name}    # 建议采用${spring.application.name}
    topic: stringRequestTopic
    selectorExpression: tagA
    enableMsgTrace: true                 # 消息轨迹开启，根据需要来决定
```

```java
@SpringBootApplication
public class ConsumerApplication implements CommandLineRunner {

    @Resource
    private RocketMQTemplate rocketMQTemplate;

    @Resource(name = "extRocketMQTemplate")
    private RocketMQTemplate extRocketMQTemplate;

    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        //This is an example of pull consumer using rocketMQTemplate.
        List<String> messages = rocketMQTemplate.receive(String.class);
        System.out.printf("receive from rocketMQTemplate, messages=%s %n", messages);

        //This is an example of pull consumer using extRocketMQTemplate.
        messages = extRocketMQTemplate.receive(String.class);
        System.out.printf("receive from extRocketMQTemplate, messages=%s %n", messages);
    }
}
```
#### 事务消息
```java
@SpringBootApplication
public class ProducerApplication implements CommandLineRunner{
    @Resource
    private RocketMQTemplate rocketMQTemplate;

    public static void main(String[] args){
        SpringApplication.run(ProducerApplication.class, args);
    }

    public void run(String... args) throws Exception {
        try {
            // Build a SpringMessage for sending in transaction
            Message msg = MessageBuilder.withPayload(..)...;
            // In sendMessageInTransaction(), the first parameter transaction name ("test")
            // must be same with the @RocketMQTransactionListener's member field 'transName'
            rocketMQTemplate.sendMessageInTransaction("test-topic", msg, null);
        } catch (MQClientException e) {
            e.printStackTrace(System.out);
        }
    }

    // Define transaction listener with the annotation @RocketMQTransactionListener
    @RocketMQTransactionListener
    class TransactionListenerImpl implements RocketMQLocalTransactionListener {
          @Override
          public RocketMQLocalTransactionState executeLocalTransaction(Message msg, Object arg) {
            // ... local transaction process, return bollback, commit or unknown
            return RocketMQLocalTransactionState.UNKNOWN;
          }

          @Override
          public RocketMQLocalTransactionState checkLocalTransaction(Message msg) {
            // ... check transaction status and return bollback, commit or unknown
            return RocketMQLocalTransactionState.COMMIT;
          }
    }
}
```
默认情况下，@RocketMQTranscationListenner只能有一个，不过可以指定rocketMQTemplateBeanName来定义多个Listener，通过@ExtRocketMQTemplateConfiguration扩展RocketMQTemplate
```java

@ExtRocketMQTemplateConfiguration
public class ExtRocketMQTemplate extends RocketMQTemplate {

}
```
{{% alert title="提示" color="primary" %}}

可以参考[rocketmq-samples](https://github.com/apache/rocketmq-spring/blob/master/rocketmq-spring-boot-samples/rocketmq-produce-demo/src/main/java/org/apache/rocketmq/samples/springboot/ProducerApplication.java)

{{% /alert %}}

#### Macula 额外扩展

- 引入TxMqMessage，通过发送TxMqMessage执行业务方法和检查方法
- 引入@TxMqExecute和@TxMqCheck标识业务方法和检查方法
```java
    private RocketMQTemplate rocketMQTemplate;

    private final String BIZ_NAME_ORDER = "BIZ_ORDER";

    private final String TOPIC_ORDER = "TOPIC_ORDER_TX";

    public OrderServiceImpl(RocketMQTemplate template) {
        this.rocketMQTemplate = template;
    }

    public void createOrderWithMq(OrderVo order) {
        TxMqMessage txMsg = new TxMqMessage(order, this.getClass(), BIZ_NAME_ORDER, order.getOrderNo());
        rocketMQTemplate.sendMessageInTransaction(TOPIC_ORDER, txMsg, new Object[] { order });
    }

    @Transactional
    @TxMqExecute(BIZ_NAME_ORDER)
    public void createOrder(OrderVo order) {
        System.out.println("=============" + order.getOrderNo());
    }

    @TxMqCheck(BIZ_NAME_ORDER)
    public boolean checkOrder(String orderNo) {
        System.out.println("order_no=" + orderNo);
        return true;
    }
```



### 环境隔离

本模块支持通过PostProcessor自动设置@RocketMQTransactionListener的namespace。当该注解没有配置namespace而配置文件中配置了rocketmq.consumer.namespace时，会自动设置namespace。

```yaml
macula:
	rocketmq:
		namespace:
			enabled: true
rocketmq:
	producer:
		namespace: macula-${spring.profiles.active}
		...
	consumer:
		namespace: macula-${spring.profiles.active}  
    ...
```

### 灰度隔离

通过在消息中添加user-property，消费时过滤来实现灰度环境的消息隔离。灰度标识一般情况下可以利用spring cloud注册中心的metadata配置。

```yaml
spring:
  cloud:
    nacos:
      discovery:
        enabled: true
        server-addr: ${nacos.config.server-addr}
        namespace: ${nacos.config.namespace}
        # group:
        metadata:
          grayversion: version1        # 灰度标识，这个标识会被写入rocketmq的user property
```

灰度配置如下：

```yaml
macula:
	rocketmq:
		gray:
			enabled: true							# 是否开启灰度隔离
			gray-consume-main: false  # 灰度环境消费者是否可以消费基线消息
			main-consume-gray: false  # 基线环境消费者是否可以消费灰度环境消息
```

### 连接多个集群

默认情况下只能连接一个RocketMQ集群，如果要发送消息给多个集群，可以使用ExtRocketMQTemplateConfiguration注解生成新的RocketMQTemplate

```java
@ExtRocketMQTemplateConfiguration(nameServer = "${demo.rocketmq.extNameServer}")
public class ExtRocketMQTemplate extends RocketMQTemplate {
}

public class ProductApp {
    @Resource(name = "extRocketMQTemplate")
    private RocketMQTemplate extRocketMQTemplate;
  	...
}
```

PULL消费模式类似

```java
@ExtRocketMQConsumerConfiguration(nameServer = "${demo.rocketmq.extNameServer}")
public class ExtRocketMQTemplate extends RocketMQTemplate {
}

public class ConsumerApplication implements CommandLineRunner {

    @Resource(name = "extRocketMQTemplate")
    private RocketMQTemplate extRocketMQTemplate;

    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        //This is an example of pull consumer using extRocketMQTemplate.
        messages = extRocketMQTemplate.receive(String.class);
        System.out.printf("receive from extRocketMQTemplate, messages=%s %n", messages);
    }
}
```

RocketMQMessageListener注解本身就支持设置不同服务器地址

```java
@RocketMQMessageListener(nameServer = "${demo.rocketmq.myNameServer}", topic = "${demo.rocketmq.topic}", consumerGroup = "string_consumer_newns")
public class StringConsumerNewNS implements RocketMQListener<String> {
    @Override
    public void onMessage(String message) {
        System.out.printf("------- StringConsumerNewNS received: %s \n", message);
    }
}
```

RocketMQTransactionListener默认使用rocketMQTemplate这个bean，可以使用该注解rocketMQTemplateBeanName属性配置不同的RocketMQTemplate

```java
@RocketMQTransactionListener(rocketMQTemplateBeanName = "extRocketMQTemplate")
public class ExtTransactionListenerImpl implements RocketMQLocalTransactionListener {
      @Override
      public RocketMQLocalTransactionState executeLocalTransaction(Message msg, Object arg) {
          System.out.printf("ExtTransactionListenerImpl executeLocalTransaction and return UNKNOWN. \n");
          return RocketMQLocalTransactionState.UNKNOWN;
      }

      @Override
      public RocketMQLocalTransactionState checkLocalTransaction(Message msg) {
          System.out.printf("ExtTransactionListenerImpl checkLocalTransaction and return COMMIT. \n");
          return RocketMQLocalTransactionState.COMMIT;
      }
}
```



## 依赖引入

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.rocketmq</groupId>
        <artifactId>rocketmq-spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-commons</artifactId>
    </dependency>
</dependencies>
```



## 版权说明

- rocketmq：https://github.com/apache/rocketmq/blob/develop/LICENSE
