---
title: "Macula Boot Starter Binlog4j"
linkTitle: "Binlog订阅"
weight: 2
source_path: "macula-boot-examples/macula-example-binlog4j/README.md"
source_paths: ["macula-boot-examples/macula-example-binlog4j/README.md", "macula-boot-starters/macula-boot-starter-binlog4j/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
---

## 概览

该模块演示 `macula-boot-starter-binlog4j` 的 MySQL binlog 订阅。`UserEventHandler` 监听 `macula-system.sys_user` 表的新增、修改和删除事件，并将解析后的数据输出到控制台。


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

### 前置条件

- MySQL `127.0.0.1:33306`，开启 binlog，建议使用 `ROW` 格式。
- 订阅账号具有 replication 权限。
- Redis `127.0.0.1:36379`，用于集群模式的状态协调。
- 数据库 `macula-system` 中存在 `sys_user` 表。

### 配置与启动

配置前缀 `binlog4j.client-configs.master` 定义 MySQL 连接，默认用户 `root`、密码为空，必须按实际环境覆盖。

| 属性 | 示例值 | 说明 |
| --- | --- | --- |
| `binlog4j.client-configs.master.host` / `port` | `127.0.0.1` / `33306` | MySQL 地址，端口可用 `MYSQL_PORT` 覆盖 |
| `binlog4j.client-configs.master.username` / `password` | 环境提供 | 复制账号及密码 |
| `binlog4j.client-configs.master.server-id` | `1991` | 复制客户端 ID，避免冲突 |
| `binlog4j.client-configs.master.mode` | `cluster` | 本示例使用 Redis 协调主备 |
| `binlog4j.client-configs.master.persistence` / `gtid-mode` | `true` / `true` | 持久化位点 / 使用 GTID，MySQL 需启用 GTID |
| `spring.data.redis.host` / `port` / `password` | 按环境配置 | Boot 4 Redis 连接属性 |

注意：当前示例文件仍写为旧的 `spring.redis.*`，运行前需在本地配置中改用 `spring.data.redis.*` 或通过启动参数覆盖。连接 Examples Compose 的 Redis 时使用端口 `36379` 和对应密码。完整配置见 [Binlog4j Starter](/docs/latest/01_services/框架扩展/binlog4j/)。

```bash
# 在仓库根目录先安装所需框架依赖，再只启动当前应用
mvn -pl macula-boot-examples/macula-example-binlog4j -am install -DskipTests -Dgpg.skip=true -Pdeploy
mvn -f macula-boot-examples/macula-example-binlog4j/pom.xml spring-boot:run
```

启动后对 `sys_user` 执行 `INSERT`、`UPDATE` 或 `DELETE`，控制台应输出对应事件。如果复制示例监听其他表，同步修改 `@BinlogSubscriber` 的 `database` / `table` 和事件实体字段。




先开启 MySQL ROW 格式 binlog 并授予专用账号必要的复制权限；使用持久化或集群选举时还需可用的 Redis。

```yaml
spring:
  data:
    redis:
      host: 127.0.0.1
      port: 6379
binlog4j:
  client-configs:
    master:
      host: 127.0.0.1
      username: ${BINLOG_USERNAME}
      password: ${BINLOG_PASSWORD}
      server-id: 1990
      persistence: true
```

每个客户端独立配置，前缀为 `binlog4j.client-configs.<名称>`，名称需与 `@BinlogSubscriber.clientName` 一致。

| 属性 | 默认值 | 说明 |
| --- | --- | --- |
| `host` / `username` / `password` | 未设置 | MySQL 地址及账号 |
| `port` | `3306` | MySQL 端口 |
| `server-id` | `0` | 应显式指定复制客户端 ID，避免与其他复制客户端冲突 |
| `mode` | `standalone` | `cluster` 使用集群主备模式 |
| `persistence` | `false` | 将消费位点持久化到 Redis |
| `inaugural` | `false` | 为 `true` 时跳过恢复历史位点，勿作为常规重启配置 |
| `keep-alive` | `true` | 保持连接 |
| `keep-alive-interval` | `60000` | 保活间隔，毫秒 |
| `connect-timeout` | `3000` | 建连超时，毫秒 |
| `heartbeat-interval` | `5000` | 心跳间隔，毫秒 |
| `time-offset` | `0` | Date 类型值的时间偏移，毫秒 |
| `gtid-mode` | `false` | 使用 GTID 复制 |
| `gtid-purged` | `true` | GTID 集为空时读取已清理 GTID 信息 |
| `gtid-set-default` | 未设置 | 无缓存 GTID 位点时的起始集合 |

时间数值不要加 Java 的 `L` 后缀；GTID 模式须与 MySQL 服务端配置匹配。

## 核心功能

### 订阅binlog事件

```java
import tools.jackson.databind.json.JsonMapper;

@BinlogSubscriber(clientName = "master", database = "macula-system", table ="sys_user")
public class UserEventHandler implements IBinlogEventHandler<User> {

    private static final JsonMapper JSON_MAPPER = JsonMapper.builder().build();

    @Override
    public void onInsert(User target) {
        System.out.println("插入数据：" + JSON_MAPPER.writeValueAsString(target));
    }

    @Override
    public void onUpdate(User source, User target) {
        System.out.println("修改数据:" + JSON_MAPPER.writeValueAsString(target));
    }

    @Override
    public void onDelete(User target) {
        System.out.println("删除数据");
    }
}

@Data
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

组件使用独立的 Jackson 3 Mapper，默认将下划线列名映射到驼峰属性，例如 `dept_id → deptId`，无需实体类声明命名策略。没有对应属性的列会忽略；无法转换的字段值会抛出异常。

特殊列名可通过 `com.fasterxml.jackson.annotation.JsonProperty` 显式映射，例如 `@JsonProperty("user_no") private String account;`。原有 fastjson2 的 `@JSONType`、`@JSONField` 和自定义反序列化器不再生效，升级时须迁移为 Jackson 注解或对应实现。日期、枚举等自定义转换应针对业务实体验证。

Redis 位点使用另一个独立 Mapper，保留 `serverId`、`position`、`filename`、`gtidSet` 字段名和原 Redis key，可读取历史位点 JSON。组件不修改应用全局 Mapper；位点 JSON 字段顺序和 null 输出不作为兼容性约定。

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
        <groupId>tools.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid</artifactId>
    </dependency>
    <dependency>
        <groupId>io.debezium</groupId>
        <artifactId>mysql-binlog-connector-java</artifactId>
    </dependency>
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## 版权说明

本代码沿用[binlog4j](https://github.com/dromara/binlog4j)代码，做了适配修改。

- binlog4j：https://github.com/dromara/binlog4j/blob/master/LICENSE
- mysql-binlog-connector-java: https://github.com/osheroff/mysql-binlog-connector-java
