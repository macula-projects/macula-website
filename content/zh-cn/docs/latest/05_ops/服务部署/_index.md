---
title: "服务部署"
linkTitle: "服务部署"
weight: 2
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["deploy/scripts/compose.sh", "deploy/docker-compose.yml", "deploy/.env.example", "macula-samples-service1/Dockerfile", "macula-samples-service1/src/main/resources/application.yml"]}]
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

## 一次发布演练

以下以“工作项业务上线到单机预发布”为例串联操作。使用已准备好的测试环境与现有 Samples Compose，不把这份开发编排当作高可用生产模板。实际生产平台可替换编排工具，但制品、配置、迁移和验证的对应关系保持一致。

### 构建并固定镜像

在完成[运行与测试](/docs/latest/04_devmanual/运行与测试/)、提交待发布业务修改并确认工作区干净后，从 Samples 根目录构建。镜像标签采用本次业务源码提交，镜像仓库替换为自己的地址：

```bash
export IMAGE_REGISTRY=registry.example.com/team
export IMAGE_TAG="work-item-$(git rev-parse --short HEAD)"
./deploy/scripts/compose.sh build \
  macula-samples-service1 macula-samples-admin-bff macula-samples-admin
```

这些命令只构建本次涉及的三个应用镜像；Gateway 路由不变时沿用已验证版本。首次安装环境则应先完成整套应用准备。构建使用源码中的 Dockerfile：当前 Java 镜像以 `local` Maven profile 打包，运行时由环境选择配置；不要声称已有 Dockerfile 自动执行了生产 profile 构建或完整测试。

使用具备目标仓库权限的账号推送上述镜像，并记录每条输出的最终 digest：

```bash
docker push "${IMAGE_REGISTRY}/macula-samples-service1:${IMAGE_TAG}"
docker push "${IMAGE_REGISTRY}/macula-samples-admin-bff:${IMAGE_TAG}"
docker push "${IMAGE_REGISTRY}/macula-samples-admin:${IMAGE_TAG}"
```

生产使用同一份已验证制品注入环境配置，镜像构建、推送与运行是三个独立步骤。

### 配置与迁移随版本登记

发布记录至少包括：

| 项目 | 本次演练记录 |
| --- | --- |
| 业务源码与 Boot | Samples 提交、所用 Boot 制品版本 |
| 镜像 | Service1 / BFF / Admin 的 tag 与 digest |
| 配置 | namespace、group、Data ID、配置版本，以及密钥引用 |
| 数据库 | 工作项迁移编号；升级前版本、备份与恢复验证结果 |
| 回退 | 上一镜像与配置版本；新增表保留时旧应用是否仍兼容 |
| 验收 | 测试身份、执行时间、正常与拒绝场景、关联日志 / Trace |

工作项表的创建是向后兼容的新增迁移，先在开发与预发布验证空库、旧库两条路径。生产迁移用受控的单一执行入口，避免多个实例同时承担未确认的升级；新增表不自动意味着所有后续数据变化都可无损回退。

### 在预发布执行与验收

为本次演练准备独立的环境文件（示例为 `/srv/macula/releases/work-item.env`），写入本次镜像 tag、环境地址和受控凭据引用，再检查解析后的配置：

```bash
MACULA_COMPOSE_ENV=/srv/macula/releases/work-item.env \
  ./deploy/scripts/compose.sh config-apps
docker compose --env-file /srv/macula/releases/work-item.env \
  -f deploy/docker-compose.yml --profile apps pull \
  macula-samples-service1 macula-samples-admin-bff macula-samples-admin
docker compose --env-file /srv/macula/releases/work-item.env \
  -f deploy/docker-compose.yml --profile apps up -d --no-build --wait \
  macula-samples-service1 macula-samples-admin-bff macula-samples-admin
MACULA_COMPOSE_ENV=/srv/macula/releases/work-item.env \
  ./deploy/scripts/compose.sh status
```

这里直接调用 Compose 的 `pull` 与 `up --no-build`，使用前一步推送的镜像，避免已有脚本 `up-apps` 的 `--build` 在目标机重新构建。Compose 仍可能启动必要依赖，演练前核对目标项目与数据卷。生产发布平台应引用已批准的 digest，并负责迁移、分批发布与切流。配置解析结果含敏感值时仅在受控终端查看，不作为公开发布附件。

在启用探针的内部管理地址验证 readiness，然后通过实际业务入口登录。创建工作项并刷新列表，再用只读用户验证创建被拒、另一个用户验证查不到原用户数据。核对数据库写入和一条经过 Gateway / BFF / Service1 的请求，按后面的可观测性验收确认指标、链路与日志。

发生错误先暂停继续发布，保留失败请求的时间和关联标识。代码或配置可回退时恢复上一版本，数据库按兼容性判断保留新增表或执行预先演练的恢复方案；不删除数据卷来“回滚”。

## 故障定位顺序

| 现象 | 优先定位 | 下一步证据 |
| --- | --- | --- |
| 启动即失败 | 配置加载、依赖连接、Flyway | 具体实例启动日志、实际 profile 与迁移历史 |
| 登录成功但业务入口被拒 | 应用 Gateway / IAM / URL 角色规则 | 使用的 Client、Token 状态、应用名与原始入口路径 |
| BFF 或 Service 验签失败 | 应用 Gateway JWK、网络与签名材料 | 从该实例能否取得公钥、JWT 的签发者与有效期 |
| 页面有菜单但写入被拒 | 方法角色、PMS 操作权限、资源条件 | 测试身份真实角色、具体拒绝方法及业务状态 |
| 请求超时 | 服务发现、Feign、下游数据库 | Trace 的慢段、实例可达性、连接池与受控 SQL 证据 |
| 接口成功但数据异常 | 事务、查询范围、缓存、迁移 | 数据库结果与返回模型、跨实例缓存失效情况 |
| 日志无法串联 | 上下文传播、采样、OTLP 导出 | 同一请求的 traceId、Collector 接收与后端查询结果 |
