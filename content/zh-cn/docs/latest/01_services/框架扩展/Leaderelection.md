---
title: "Macula Boot Starter LeaderElection"
linkTitle: "领导选择"
weight: 7
source_path: "macula-boot-starters/macula-boot-starter-leaderelection/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-leaderelection/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

*通过**redis**的**lock**做领导选举*。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-leaderelection</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml

```yaml
spring:
  application:
    name: ${APP_NAME:business-service}
  data:
    redis:
      host: 127.0.0.1
      port: 6379
```

### 关键配置

必须配置 `spring.application.name`，本模块以 `leader-lock-<应用名>` 为锁键。同一选举组的实例应共用 Redis 和应用名，不同业务组使用不同名称；无独立 `macula.leaderelection.*` 属性。

#### Redis 连接

Redis 连接配置沿用 [Redis Starter](/docs/latest/01_services/框架基础/redis/)。

## 核心功能

可以在应用中实现如下接口，当被选中时，onElected方法被触发，可以做一些标识或者leader应该做的事情。

```java
/**
 * {@code ElectionListener} 选中为领导触发该监听器
 *
 * @author rain
 * @since 2022/12/2 19:07
 */
public interface ElectionListener {

    /**
     * 被选中为领导时触发
     */
    void onElected();
}


@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Component
    public class Service {
        public Service(LeaderElection leaderElection) {
            leaderElection.addElectionListener(() -> System.out.println("master selected"));
        }
    }
}
```

### 验证与排障

| 检查 | 预期与定位方法 |
| --- | --- |
| 同组选举 | 在测试环境用相同应用名与 Redis 启动两个实例，观察领导回调和业务执行；不要只启动单实例判断选举有效。 |
| 故障交接 | 停止当前领导实例，记录另一实例何时接管。Redis 锁、失效时间和网络故障会影响交接，不能据此承诺强一致主节点。 |
| 业务副作用 | 领导变更期间仍按业务要求设计幂等，避免重复任务产生重复写入。 |

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-redis</artifactId>
    </dependency>
</dependencies>
```

## 版权说明

- redisson：https://github.com/redisson/redisson/blob/master/LICENSE.txt
