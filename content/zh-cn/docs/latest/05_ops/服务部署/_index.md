---
title: "服务部署"
linkTitle: "服务部署"
weight: 2
manual_content: true
---

## 生产发布顺序

本页提供交付检查路径，具体编排由部署环境决定。本地 Compose 演示见[打包部署](/docs/latest/04_devmanual/打包部署/)，不能直接当作高可用生产方案。

1. 按[服务创建](/docs/latest/05_ops/服务创建/)生成可追溯制品，在预发布验证；记录旧镜像 digest、配置版本和数据库版本。
2. 按[服务配置](/docs/latest/05_ops/服务配置/)准备凭据、配置中心、HTTPS、回调和可观测性连接；先备份数据库并验证恢复方案。
3. 数据库迁移在明确的单一执行入口运行。Samples Service1 维护自己的 Flyway 脚本；Cloud 共享库由 System 维护。追加迁移不修改已执行脚本，先验证空库初始化和旧库升级。多副本启动前确认迁移完成。
4. 先部署业务服务，再 BFF、应用 Gateway 和 Admin；按实际依赖核对 readiness、注册发现和路由，分批切流。
5. 使用真实测试身份执行登录、菜单获取、业务读写及无权限拒绝测试。检查返回业务状态，不能以进程存在或 HTTP 200 代替功能验证。
6. 检查日志、指标和一条跨 Gateway/BFF/Service 的 Trace，再观察错误率、延迟与资源使用，按事先定义的发布阈值决定扩大流量。

## 健康与就绪

启用 Actuator 探针并仅在内部管理网络暴露必要端点，例如：

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
  endpoints:
    web:
      exposure:
        include: health,info
```

在部署系统探测实际管理端口的 `/actuator/health/liveness` 和 `/actuator/health/readiness`。liveness 关注进程是否需重启，readiness 决定是否接流；按业务补充关键依赖的健康检查，避免把短暂外部故障导致的全体重启作为恢复策略。端点需受访问控制，不能公开暴露完整环境和 Bean 信息。

## 可观测性验收

参照 [Observability](/docs/latest/01_services/生产准备/observability/#验证三类信号)，确认 Collector 收到 metrics/traces/logs、后端可查询，并通过 traceId 将请求与日志关联。记录一次正常请求、一次受控错误以及一次授权拒绝；检查敏感字段未进入日志。应用启动但遥测全丢失应作为发布问题处理。

## 回滚

先停止扩大流量，按发布阈值切回上一镜像及配置版本，保留故障日志和 Trace。代码回滚不会自动回滚数据库；迁移采用向前兼容的扩展/收缩策略，删除字段等破坏性迁移另设窗口。确需恢复备份时评估新写入数据并执行事先演练的恢复方案。回滚后重跑健康、认证及关键业务验证，不删除数据卷或修改 Flyway 历史表“修复”发布。
