---
title: "首次接入"
linkTitle: "首次接入"
weight: 3
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["macula-cloud-iam/README.md", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/OAuth2ClientConfigServiceImpl.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/ProtocolOAuth2Configuration.java", "macula-cloud-admin/src/views/system/application/save.vue", "macula-cloud-admin/src/views/system/oauth2Client/index.vue", "macula-cloud-system/src/main/resources/db/migration/V2__admin_identity_security_settings.sql"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["macula-samples-admin/src/views/common/login/components/passwordForm.vue", "macula-samples-admin/src/config/index.js", "macula-samples-gateway/src/main/resources/application.yml", "macula-samples-admin-bff/src/main/resources/application.yml", "macula-samples-admin-bff/src/main/java/dev/macula/samples/admin/bff/controller/ApplicationController.java"]}]
---

本页以本机启动的 Cloud 与 Samples 为例，说明从平台登记到受保护接口验证。先完成[平台部署](/docs/latest/04_devmanual/部署macula平台/)及[创建示例平台](/docs/latest/04_devmanual/创建应用平台/)。端口如有覆盖，以实际配置为准。

## 1. 登记业务应用

使用有平台管理权限的账号打开 Cloud Admin（默认 `http://127.0.0.1:5900`），进入“应用管理”（页面 `/system/application`），新建应用。

| 字段 | Samples 示例 | 用途 |
| --- | --- | --- |
| 应用名称 | Samples 管理端 | 平台显示名称 |
| 应用编码 | `macula-samples-admin-bff` | 对应 BFF 的 `macula.cloud.app-key` |
| secretKey | 页面生成的值 | 保存到服务端的 `MACULA_CLOUD_APP_SECRET` |
| 主页 | `http://127.0.0.1:5800` | 业务前端入口 |
| 可访问路径 | 按实际开放资源配置 | 应用资源范围，不能用它替代用户角色授权 |
| 负责人、维护人 | 实际管理账号 | 应用维护责任人 |

应用 AK/SK 与 OAuth Client 的 ID/Secret 属于不同凭据。BFF 的应用密钥只放在服务端。不要沿用 `example`，也不要写入 Vite 环境变量。

## 2. 登记 IAM 接入应用

进入“IAM接入应用”（`/system/oauth2-client`）。填写 Client ID、应用名称、所属租户和用户类型；选择终端和登录方式，再配置回调与高级协议字段。

新浏览器应用使用授权码与 S256 PKCE。以下为新建客户端的配置示例，**回调页面需由业务应用实际实现**：

| 字段 | 示例 / 规则 |
| --- | --- |
| Client ID | `samples-web`，与客户端配置一致 |
| 认证方式 | 公共浏览器客户端 `none`，浏览器不保存 Secret |
| 授权方式 | `authorization_code,refresh_token`，以页面最终保存值为准 |
| Scopes | `openid,profile`，按允许的权限选择 |
| 重定向 URI | `http://127.0.0.1:5800/auth/callback`，必须精确登记 |
| 浏览器协议允许 Origin | `http://127.0.0.1:5800`，只填 scheme、host、port，不含路径 |
| 登录方式 | 先选择本地登录；第三方登录另需绑定真实 Provider 配置 |

`localhost` 与 `127.0.0.1` 是不同 Origin，回调也必须与授权请求一致。应用应校验 state，OIDC 客户端还应校验 ID Token；授权码只能使用一次，不能省略 PKCE 校验。协议要求见 [OAuth 安全实践](https://www.rfc-editor.org/rfc/rfc9700.html)。

**当前 Samples 的兼容边界**：已提交的 `passwordForm.vue` 仍使用 `grant_type=password`，配置项为 `VITE_APP_OAUTH_CLIENT_ID`、`VITE_APP_OAUTH_CLIENT_SECRET`、`VITE_APP_OAUTH_SCOPE`；它没有上述 PKCE 回调实现。现有本地示例若继续使用该流程，需为其单独登记允许 `password` 的兼容 Client，认证方式与 IAM 请求保持一致、scope 必须是该 Client 允许值。当前 Cloud 保留此兼容扩展，但不应把浏览器携带 Secret 的示例直接作为生产接入方案。新应用需实现授权码登录，或采用服务端 BFF 管理令牌，不能只改 Client 配置就声称完成迁移。

## 3. 对齐三个连接方向

| 调用方 | 配置 | 地址来源 |
| --- | --- | --- |
| 应用 Gateway → IAM | `spring.security.oauth2.resourceserver.opaquetoken.introspection-uri` 及 client-id / client-secret | 默认 `http://127.0.0.1:9010/oauth2/introspect`；使用有内省权限的服务端 Client |
| BFF → Cloud | `macula.cloud.endpoint` / `app-key` / `secret-key` | Cloud Gateway，默认 `http://127.0.0.1:9000`；填第 1 步的应用凭据 |
| BFF / Service → 应用 Gateway | `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` | Samples Gateway 的 JWK 地址，详见[安全架构](/docs/latest/00_introduce/安全架构/) |

Gateway 的 System Redis 应指向 **Cloud System 实际使用的同一 Redis 与数据库**，应用自身 Redis 则独立配置。Samples 默认 System Redis 端口 `16379`，Cloud 标准 Compose 默认 `6379`，请按部署覆盖 `MACULA_CLOUD_REDIS_PORT`。同样区分本机地址、容器 DNS 与浏览器可访问地址；IDE 不自动加载 `.env`。完整键名见[示例配置](/docs/latest/04_devmanual/模块说明/#示例配置)。

## 4. 配置菜单与用户角色

在 Cloud 的菜单管理登记业务页面、路由组件和按钮权限，归属到对应业务应用；在角色管理授予菜单/按钮权限，再将角色分配给测试用户。对照 Samples 的 `src/views/service1/application/index.vue` 确定组件路径，不能将 Cloud 自身的 `system/application` 页面当作业务页面。

重新登录后，确认 BFF 返回的用户信息包含预期角色、权限，菜单接口包含该应用的菜单；页面、按钮、Gateway URL 权限及后端方法权限分别验证。菜单可见仅代表前端导航权限。

## 5. 验证结果与失败定位

先在浏览器 Network 中完成登录，取得测试用户的 access token；不要把 Token 保存进源码或提交记录。以下在终端临时输入该令牌，调用 Samples 的真实应用列表接口：

```bash
read -s ACCESS_TOKEN
curl --fail-with-body --get \
  'http://127.0.0.1:6000/admin/api/v1/app' \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  --data-urlencode 'pageNum=1' --data-urlencode 'pageSize=10'
unset ACCESS_TOKEN
```

成功时返回统一响应与应用分页数据；空数据可返回空列表，不能只看 HTTP 200。分别验证：有效且获授权用户成功、无 Token 被拒、过期 Token 被拒、缺少必要权限被拒。Samples Gateway 的 `/api/**` 仅认证规则与具体角色 URL 规则需分别核对；方法权限的拒绝测试应选择已声明授权规则的接口，不能假定所有示例接口都已有细粒度注解。

| 现象 | 首先核对 |
| --- | --- |
| `invalid_client` | Client ID、认证方式、Secret 及网关内省 Client，区别于应用 AK/SK |
| 回调或 Origin 被拒 | 精确地址、协议、端口、Client 允许列表 |
| 登录成功，菜单为空 | BFF app-key、Cloud endpoint、应用菜单与用户角色 |
| Gateway 认证失败 | IAM 内省地址、Client 权限、System Redis 地址 |
| 下游 JWT 验签失败 | JWK 是否来自当前应用 Gateway、容器可达性、签名密钥一致性 |

这组步骤是接入验证方法；文档构建通过不代表当前部署已完成认证联调。
