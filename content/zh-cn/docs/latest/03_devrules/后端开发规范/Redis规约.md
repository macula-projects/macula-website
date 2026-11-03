---
title: "Redis规约"
linkTitle: "Redis规约"
weight: 6
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "cd6e30827c78d267cca2f4e0d7b3a6e3dcb01617", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/阿里规范/Java开发手册(黄山版).pdf", "content/zh-cn/docs/latest/03_devrules/后端开发规范/Redis规约.md"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-starters/macula-boot-starter-redis/README.md", "macula-boot-starters/macula-boot-starter-cache/README.md", "macula-boot-starters/macula-boot-starter-lock4j/README.md", "macula-boot-starters/macula-boot-starter-idempotent/README.md"]}]
---

Redis 用于缓存、短期状态、协调及平台运行数据。先确定数据的所有权、丢失后果和故障策略，再选择存储结构；不能因为访问快，就将需要持久保证的业务事实只保存在缓存中。

## 键与数据模型

键使用可识别的应用、领域、用途和标识组成，例如 `order-service:order:detail:12345`。有租户语义时，将已验证的租户标识纳入隔离设计；共享部署的环境也需隔离。避免将密码、完整手机号、Token 或其他敏感原文作为可直接观察的键名。

| 内容 | 规约 |
| --- | --- |
| 命名 | 项目内使用统一大小写与分隔方式，限制长度，避免控制字符及难以运维的转义形式 |
| 数据类型 | 按访问模式选择 String、Hash、Set、List、ZSet；不为节省键数创建无界集合 |
| 序列化 | 明确编码、字段与版本兼容性，新旧应用并存时都能处理已有数据 |
| 生命周期 | 临时数据设置 TTL；永久数据明确容量和清理责任 |
| Redis Cluster | 多键原子操作按要求位于同一 slot，hash tag 不得造成热点集中 |

新增缓存键的前缀、TTL、大小上限与删除方式应写入模块说明。调整序列化或键结构时设计版本前缀、兼容读取或迁移策略，不靠全库清空处理升级。

## 容量与命令

必须监测键数量、内存、热键、单键大小、集合基数和访问延迟。旧文中的“10 KB、5000 个元素”等数值可作为某些场景的评估起点，不能当作适用于所有实例、命令和数据结构的硬边界。

生产业务路径不得执行全库清空或不受控的 `KEYS`、全量集合读取。确需枚举时用 SCAN 系列分批处理，限制扫描速率并处理重复元素；扫描过程不是一致性快照，单次 COUNT 也不是严格返回条数。

批量操作与 Pipeline 必须控制元素数和总字节数。Pipeline 主要减少网络往返，不提供事务原子性；多键命令及 Lua 的原子语义分别按实际命令和部署模式判断。

大键删除优先评估当前服务器与客户端支持的异步释放方式，并在受控任务中分批处理；同步删除、批量过期和重建均需评估 CPU、内存、复制与网络影响。排障期间限制 MONITOR 等高成本观测操作的范围和时长。

## TTL 与一致性

写入临时值时尽量原子设置 TTL，避免写值成功但设置过期失败。允许时对到期时间增加随机偏移，避免批量同时失效；随机范围不能突破业务允许的最长陈旧时间。

数据库为事实来源时，缓存更新与失效要围绕提交时机设计，防止事务回滚却提前发布缓存、并发回填旧值或删除失败。短期最终一致不适合所有业务，余额、库存及权限等场景需单独评估。

对不存在对象的请求，可结合短 TTL 空值缓存、请求限制或其他机制防止持续穿透；空值必须与正常结果可区分。热点重建应限制并发，防止一次缓存故障压垮数据库。

## 锁与幂等

分布式锁必须明确锁名、拥有者、等待时间、租约及释放方式，使用成熟组件的正确用法。不能以“先 GET、再 SET”实现互斥，也不能由非持有者无条件删除锁。

锁过期后旧持有者可能仍在执行，关键写入仍要由数据库条件、版本或其他隔离机制保护。接口防重、业务幂等和互斥是不同问题；仅拿到 Redis 锁不能证明业务只执行一次。

使用 [Lock4j](/docs/latest/01_services/框架扩展/lock4j/)、[Idempotent](/docs/latest/01_services/框架扩展/idempotent/) 时核对超时、异常与解锁规则。租约长度不能凭固定经验值代替最长执行时间评估。

## 连接与故障

连接、命令、连接池等待均需有边界，按业务延迟预算设置。缓存读取失败、缓存写入失败、锁失败与平台身份数据不可用应分别决定拒绝、降级或补偿，不能统一吞掉 Redis 异常。

Macula 两级缓存可在部分 Redis 连接和超时故障下 fail-open，但其他实例可能暂时持有旧值；其行为不代表 System Redis、业务 Redis 和分布式锁都可无条件降级。

普通服务使用 `spring.data.redis.*`，显式 Redisson YAML 使用其对应命名空间；Samples Gateway 的自定义连接与 System Redis 按绑定代码配置。多数据库编号不是资源或权限隔离，Cluster 也不能当作可随意切换数据库的单机实例。

## 验收与参考

验证正常读写、TTL、并发回填、连接超时、Redis 重启、键结构升级与多实例失效传播；容量检查使用接近实际的键数和载荷。

连接配置见 [Redis](/docs/latest/01_services/框架基础/redis/)，缓存行为见 [Cache](/docs/latest/01_services/框架基础/cache/)。命令语义以 [Redis SCAN 文档](https://redis.io/docs/latest/commands/scan/)及所用服务器版本为准，历史开发建议可参见[阿里云 Redis 开发规范](https://developer.aliyun.com/article/531067)。
