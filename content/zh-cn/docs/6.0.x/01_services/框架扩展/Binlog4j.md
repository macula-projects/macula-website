---
title: "Macula Boot Starter Binlog4j"
linkTitle: "Binlog订阅"
weight: 2
source_path: "macula-boot-examples/macula-example-binlog4j/README.md"
source_paths: ["macula-boot-examples/macula-example-binlog4j/README.md", "macula-boot-starters/macula-boot-starter-binlog4j/README.md"]
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
---

# Binlog4j 示例

该模块演示 `macula-boot-starter-binlog4j` 的 MySQL binlog 订阅。`UserEventHandler` 监听 `macula-system.sys_user` 表的新增、修改和删除事件，并将解析后的数据输出到控制台。

## 前置条件

- MySQL `127.0.0.1:3306`，开启 binlog，建议使用 `ROW` 格式。
- 订阅账号具有 replication 权限。
- Redis `127.0.0.1:6379`，用于集群模式的状态协调。
- 数据库 `macula-system` 中存在 `sys_user` 表。

## 配置与启动

`application.yml` 中的 `binlog4j.client-configs.master` 定义 MySQL 连接。本地默认用户是 `root`、密码为空，请按实际环境覆盖。

```bash
mvn -pl macula-boot-examples/macula-example-binlog4j -am spring-boot:run
```

启动后对 `sys_user` 执行 `INSERT`、`UPDATE` 或 `DELETE`，控制台应输出对应事件。如果复制示例监听其他表，同步修改 `@BinlogSubscriber` 的 `database` / `table` 和事件实体字段。


---

## 概述

binlog4j是一个读取MySQL binlog的组件，以slave的方式接入mysql，将binlog转为事件。

## 组件坐标

```xml

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-binlog4j</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用配置

```yaml
spring:
  redis:
    host: 127.0.0.1
    port: 6379

binlog4j:
  client-configs:
    master: # clientID
      username: root            # mysql的用户
      password:                 # mysql的密码
      host: 127.0.0.1           # mysql的host
      port: 3306                # mysql的port
      serverId: 1990            # 本实例的serverId，不同应用不能重复
      persistence: true         # 是否将binlog位置持久化，默认false
      inaugural: false          # 是否是首次启动，默认false
      mode: cluster             # 启动模式，集群模式一个实例启动连接到mysql，其他standby，默认standalone
      keepAlive: true           # 是否保持连接，默认是true
      KeepAliveInterval: 60000L # 保持连接间隔，默认1分钟，单位毫秒
      connectTimeout: 3000L     # 连接超时时间，默认3秒，单位毫秒
      heartbeatInterval: 6000L  # 发送心跳间隔，默认6秒，单位毫秒  
      gtidMode: true            # 开启GTID模式，默认为false
      gtidPurged: true          # 当GTID SET为“”时，是否获取最近的purged的GTID SET，默认为true
      gtidSetDefault: "xxx"     # 设置开始消费的GTID位置
```

## 核心功能

### 订阅binlog事件

```java
@BinlogSubscriber(clientName = "master", database = "macula-system", table ="sys_user")
public class UserEventHandler implements IBinlogEventHandler<User> {

    @Override
    public void onInsert(User target) {
        System.out.println("插入数据：" + JSON.toJSONString(target));
    }

    @Override
    public void onUpdate(User source, User target) {
        System.out.println("修改数据:" + JSON.toJSONString(target));
    }

    @Override
    public void onDelete(User target) {
        System.out.println("删除数据");
    }
}

@Data
@JSONType(naming = PropertyNamingStrategy.SnakeCase)
public class User {
    private Long id;
    private String username;
    private String nickname;
    private String mobile;
    private Integer gender;
    private String avatar;
    private String password;
    private String email;
    private Integer status;
    private Long deptId;
}
```

> 注意Entity要使用SnakeCase策略

### 集群模式说明

同一个应用多个实例时要启用集群模式，serverId同一个应用保持一致，不同应用千万不要重复。否则前面的应用会被踢出。同一时刻同一个serverId只能有一个实例与MySQL连接。

本模块的高可用原理是通过redis锁，集群中某个实例先连上mysql后，后hold
redis锁，其他实例会单独一个线程等待锁，如果前面的实力出现异常宕机，redis锁释放，则其他实例会自动重连，并且从redis恢复binlog的postion，从而实现高可用。

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-redis</artifactId>
    </dependency>
    <dependency>
        <groupId>cn.hutool</groupId>
        <artifactId>hutool-all</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba.fastjson2</groupId>
        <artifactId>fastjson2</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid</artifactId>
    </dependency>
    <dependency>
        <groupId>com.zendesk</groupId>
        <artifactId>mysql-binlog-connector-java</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## 版权说明

本代码沿用[binlog4j](https://github.com/dromara/binlog4j)代码，做了适配修改。

- binlog4j：https://github.com/dromara/binlog4j/blob/master/LICENSE
- mysql-binlog-connector-java: https://github.com/osheroff/mysql-binlog-connector-java
