---
title: "服务配置"
linkTitle: "服务配置"
weight: 3
manual_content: true
---

## 发布前配置

配置组织与属性前缀以[应用配置](/docs/latest/04_devmanual/应用配置/)为准。环境注入采用配置中心、受控环境变量或挂载配置，制品中不携带生产密码。

| 配置组 | 发布前核对 |
| --- | --- |
| Profile 与 Nacos | 实际激活 profile、namespace、group、Data ID；禁止与开发环境串用 |
| 数据库 | 独立业务库、迁移账号与运行账号、连接池与备份 |
| Redis | 应用 Redis 与 Cloud System Redis 的地址、库号、认证和序列化边界 |
| IAM 与应用凭据 | issuer、内省 Client、Cloud endpoint、AK/SK；浏览器不得保存服务端 Secret |
| 内部 JWT | 应用 Gateway JWK、签名材料持久化、各实例一致性 |
| 外部访问 | HTTPS、域名、回调 URI、Origin、反向代理转发头 |
| Observability | Collector 可达性、三信号导出开关、采样率、服务名和环境标签 |

Compose 会读取自己的 `.env`，Java/IDE 不会自动读取；Vite 的公开变量会进入浏览器资源。不要把数据库、应用 SK 或 Client Secret 写进前端变量。Nacos 的 `optional:` 只表示配置导入可选，生产应明确缺失配置时是否允许启动。

## 配置变更验证

先在预发布环境加载生产同构配置，验证注册发现、数据库、缓存与认证。记录每个配置版本及变更时间，密钥只记录引用与轮换编号。修改共享配置可能同时影响多个实例，按发布批次生效并保留旧配置版本供回滚；不在工单或日志粘贴完整敏感配置。
