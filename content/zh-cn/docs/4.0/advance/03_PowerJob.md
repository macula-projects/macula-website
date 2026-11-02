---
aliases: ["/docs/98_old/v4.0/advance/03_powerjob/", "/docs/5.x/98_old/v4.0/advance/03_powerjob/", "/docs/6.0.x/98_old/v4.0/advance/03_powerjob/", "/docs/latest/98_old/v4.0/advance/03_powerjob/", "/docs/v4.0/advance/03_powerjob/"]
type: docs
title: "Power Job: 统一调度平台"
linkTitle: "Power Job: 统一调度平台"
weight: 1
description: "Power Job是统一调度平台重要的一个应用任务代理，主要调度 gbss 相关的作业，比如数据同步、消息推送、群组、报表等。统一调度平台，是按应用进行作业分配和负载均衡的。
"
---

### Power Job特性：

1、采用quartz进行定时任务的发起

2、采用rabbitmq进行调度平台与应用方的通信

3、架构图：

![图片](../../imgs/Batch1.png)
### Power Job实现步骤：

1、处理任务的应用通过agent注册进入Power Job平台

2、应用注册进入平台的appId与进行消息沟通rabbitmq的queue一一对应

3、在Power Job平台进行主动或定时任务的创建

4、Power Job平台主动或通过quartz定时任务发起任务处理消息

5、接入应用根据消息进行处理后进行结果应答

### 应用方接入Power Job案例

#### 1、接入Power Job客户端依赖

```plain
<!-- applicationContext-root 配置 batch agent 信息 -->
<!-- Macula Batch Agent -->
<dependency>
     <groupId>org.macula.batch</groupId>
     <artifactId>macula-batch-jobtracker</artifactId>
     <version>2.0.0.RELEASE</version>
</dependency>
```
#### 2、相关配置

```plain
<!-- Batch Agent(DEV) -->
<bean id="agent" class="org.macula.batch.jobtracker.domain.Agent">
     <property name="serverUrl" value="https://batch-test.infinitus.com.cn/admin/macula-batch"></property>
     <property name="appId" value="gbss.po.dev"></property>
     <property name="appKey" value="xxxxx"></property>
     <property name="taskTypes" value="JAVA"></property>
</bean>
<!-- 相关bean注入 -->
<context:component-scan base-package="com.infinitus.xxx.xx.xxx" />
<!-- 任务执行代理 -->
<import resource="classpath*:META-INF/spring/macula-batch-jobtracker.xml" />
<!-- 任务消息扫描频率 -->
<task:scheduled-tasks>
    <task:scheduled ref="agentService" method="listen"  fixed-rate="5000" />
    <task:scheduled ref="agentService" method="ping"   fixed-rate="10000" />
</task:scheduled-tasks>
```
#### 3、任务执行类

```plain
@Component("BatchTestTask")
public class BatchTestTask extends AbstractBeanTask {
  /**
   * 任务核心执行代码
   */
  @Override
  public void execute() throws Exception {
    System.out.println("执行开始:"+ System.currentTimeMillis());
    //...
    System.out.println("执行结束:"+ System.currentTimeMillis());
  }
}
```
**重要！！！**
>请保证应用运行环境为 1.7.0 及以上。( JAVA 1.6环境不支持 )
### Power Job管理配置案例

![图片](../../imgs/Batch2.png)