---
title: "Redis规约"
linkTitle: "Redis规约"
weight: 7
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "dcd7fd36ee55ea43e17958264d0c6609455bb114", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/Redis规约.md"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["pom.xml", "macula-samples-parent/pom.xml"]}]
---

以下为 Redis 使用约定，体积与批量数值作为容量评估起点，应按延迟、内存与实例规格验证。当前普通服务使用 `spring.data.redis.*`；Samples Gateway 的自定义 Redis 前缀与 System Redis 另见[示例配置](/docs/latest/04_devmanual/模块说明/#示例配置)。缓存命名、TTL 和序列化契约需保持跨版本兼容；大 key 清理应优先采用服务器与客户端支持的异步释放机制并分批验证，不在生产执行全库清空。

## 概述

Redis目前已经是应对高并发、高性能场景系统设计的标配了，以下主要从键值设计、命令使用两方面对Redis的开发规范进行说明。

## 键值设计

### key名设计

  (1)【建议】: 可读性和可管理性

    以业务名(或数据库名)为前缀(防止key冲突)，用冒号分隔，例如：
    
    业务名:表名:id
    ugc:video:1

  (2)【建议】：简洁性

    保证语义的前提下，控制key的长度，当key较多时，内存占用也不容忽视，例如：
    
    user:{uid}:friends:messages:{mid}简化为u:{uid}:fr:m:{mid}

  (3)【强制】：不要包含特殊字符

    反例：包含空格、换行、单双引号以及其他转义字符

### value值设计

   (1)【强制】：拒绝bigkey(防止网卡流量、慢查询)

    string类型控制在10KB以内，hash、list、set、zset元素个数不要超过5000。
    
    反例：一个包含200万个元素的list。
    
    非字符串的bigkey，不要使用del删除，使用hscan、sscan、zscan方式渐进式删除，同时要注意防止bigkey过期时间自动删除问题(例如一个200万的zset设置1小时过期，会触发del操作，造成阻塞，而且该操作不会不出现在慢查询中(latency可查))，查找方法和删除方法

   (2)【推荐】：选择适合的数据类型

    例如：实体类型(要合理控制和使用数据结构内存编码优化配置,例如ziplist，但也要注意节省内存和性能之间的平衡)
    
    反例：
      set user:1:name tom
      set user:1:age 19
      set user:1:favor football
      
    正例:
      hmset user:1 name tom age 19 favor football

   (3)【推荐】：控制key的生命周期，redis不是垃圾桶

      建议使用expire设置过期时间(条件允许可以打散过期时间，防止集中过期)，不过期的数据重点关注idletime

## 命令使用

1.【推荐】 O(N)命令关注N的数量

    例如hgetall、lrange、smembers、zrange、sinter等并非不能使用，但是需要明确N的值。有遍历的需求可以使用hscan、sscan、zscan代替。

2.【推荐】：禁用命令

    禁止线上使用keys、flushall、flushdb等，通过redis的rename机制禁掉命令，或者使用scan的方式渐进式处理。

3.【推荐】合理使用select

    redis的多数据库较弱，使用数字进行区分，很多客户端支持较差，同时多业务用多数据库实际还是单线程处理，会有干扰。

4.【推荐】使用批量操作提高效率

    原生命令：例如mget、mset。
    
    非原生命令：可以使用pipeline提高效率。
    
    但要注意控制一次批量操作的元素个数(例如500以内，实际也和元素字节数有关)。
    
    注意两者不同：
    
      (1) 原生是原子操作，pipeline是非原子操作。
      (2)pipeline可以打包不同的命令，原生做不到
      (3) pipeline需要客户端和服务端同时支持。

5.【建议】Redis事务功能较弱，不建议过多使用

    Redis的事务功能较弱(不支持回滚)，而且集群版本(自研和官方)要求一次事务操作的key必须在一个slot上(可以使用hashtag功能解决)

6.【建议】Redis集群版本在使用Lua上有特殊要求：

    (1)所有key都应该由 KEYS 数组来传递，redis.call/pcall 里面调用的redis命令，key的位置，必须是KEYS array, 否则直接返回error，"-ERR bad lua script for redis cluster, all the keys that the script uses should be passed using the KEYS array"
      
    (2)所有key，必须在1个slot上，否则直接返回error, "-ERR eval/evalsha command keys must in same slot"

7.【建议】必要情况下使用monitor命令时，要注意不要长时间使用。

## 参考文章

+ [《阿里云Redis开发规范》](https://developer.aliyun.com/article/531067)
