---
title: "首次接入"
linkTitle: "首次接入"
weight: 3
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["macula-cloud-iam/README.md", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/OAuth2ClientConfigServiceImpl.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/ProtocolOAuth2Configuration.java", "macula-cloud-admin/src/views/system/application/save.vue", "macula-cloud-admin/src/views/system/oauth2Client/index.vue", "macula-cloud-system/src/main/resources/db/migration/V2__admin_identity_security_settings.sql"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["macula-samples-admin/src/views/common/login/components/passwordForm.vue", "macula-samples-admin/src/config/index.js", "macula-samples-gateway/src/main/resources/application.yml", "macula-samples-admin-bff/src/main/resources/application.yml", "macula-samples-admin-bff/src/main/java/dev/macula/samples/admin/bff/controller/ApplicationController.java", "macula-samples-admin/src/api/model/common/auth.js", "deploy/.env.example"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["deploy/.env.example", "deploy/docker-compose.yml", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/OAuth2ClientConfigServiceImpl.java"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/README.md", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/utils/KongApiUtils.java", "macula-boot-starters/macula-boot-starter-cloud/macula-boot-starter-cloud-gateway/src/main/java/dev/macula/boot/starter/cloud/gateway/filter/AddJwtGlobalFilter.java"]}, {"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "291e80dc296587cc1ec4f4979aa6fdb3bd087054", "paths": ["macula-cloud-system/README.md", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/SysApplicationServiceImpl.java", "macula-cloud-system/src/main/java/dev/macula/cloud/system/service/impl/SysTenantServiceImpl.java", "macula-cloud-system/src/main/resources/db/migration/V12__application_auth_tenant.sql", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/service/userdetails/SysUserDetailsServiceImpl.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/protocol/oauth2/CustomOAuth2TokenCustomizer.java", "macula-cloud-system/src/main/java/dev/macula/cloud/system/form/OAuth2ClientForm.java", "macula-cloud-admin/src/views/system/application/save.vue"]}]
---

本页以本机启动的 Cloud 与 Samples 为例，说明从平台登记到受保护接口验证。先完成[平台部署](/docs/latest/04_devmanual/部署macula平台/)及[创建示例平台](/docs/latest/04_devmanual/创建应用平台/)。端口如有覆盖，以实际配置为准。

## 1. 登记业务应用

使用有平台管理权限的账号打开 Cloud Admin（默认 `http://127.0.0.1:5900`），进入“应用管理”（页面 `/system/application`），新建应用。

| 字段 | Samples 示例 | 用途 |
| --- | --- | --- |
| 应用名称 | Samples 管理端 | 平台显示名称 |
| 应用编码 | `macula-samples-admin-bff` | 对应 BFF 的 `macula.cloud.app-key` |
| secretKey | 页面生成的值 | 保存到服务端的 `MACULA_CLOUD_APP_SECRET` |
| 归属租户 `tenantId` | 应用实际所属租户 | 管理与 AK/SK 接入隔离，须与目标网关归属一致 |
| 认证租户 `authTenantId` | 通常留空 | AK/SK 认证后的默认业务租户；留空沿用归属租户 |
| 主页 | `http://127.0.0.1:5800` | 业务前端入口 |
| 可访问路径 | 按实际开放资源配置 | 应用资源范围，不能用它替代用户角色授权 |
| 负责人、维护人 | 实际管理账号 | 应用维护责任人 |

应用 AK/SK 与 OAuth Client 的 ID/Secret 属于不同凭据。BFF 的应用密钥只放在服务端。不要沿用 `example`，也不要写入 Vite 环境变量。

### 对齐归属租户与认证租户

应用归属租户用于隔离应用接入，认证租户用于决定认证后的业务数据租户。两者通常一致；只有平台 ROOT 可设置不同的认证租户，且目标租户必须存在。不能通过把 `authTenantId` 改成目标网关的租户来绕过应用归属隔离。

目标网关按 `spring.application.name` 与平台租户编码做最长前缀匹配。例如 `macula-samples-gateway` 应匹配实际存在的 `macula-samples` 租户编码；该租户 ID 必须与当前 AK/SK 应用的归属租户一致。Cloud Gateway 同样按其自身应用名确定归属。BFF 访问 Cloud 时，这组应用凭据的归属租户须匹配 Cloud Gateway，而认证租户按需要设置为业务租户；它与 BFF 所在业务网关的归属不是同一个配置入口。System Redis 中的租户映射未就绪时，网关会拒绝接入；不使用手工 `macula.gateway.tenant-id`。

已有环境升级时，先通过正常数据库迁移流程应用 `V12__application_auth_tenant.sql`，新增可空的 `auth_tenant_id`，再运行新版 System 并确认租户映射缓存正常；在新版网关就绪后再配置不同的认证租户。历史应用不需回填，空值沿用归属租户。回滚旧网关前，先恢复认证租户与归属租户一致。

## 2. 登记 IAM 接入应用

进入“IAM接入应用”（`/system/oauth2-client`）。填写 Client ID、应用名称、所属租户和用户类型；选择终端和登录方式，再配置回调与高级协议字段。这里的“所属租户”字段 `tenantId` 表示登录认证关联的租户，IAM 在该租户及用户类型下查找用户，并把租户随认证身份带入令牌。它不等于 AK/SK 应用的归属接入规则，也不由请求中的临时租户值替代。

### 先跑通当前 Samples

本章运行主线使用当前 Samples 的本地兼容登录。其 `src/views/common/login/components/passwordForm.vue` 将 Client ID、Secret 和 scope 放在表单中，向 IAM 请求 `grant_type=password`；应登记与这个实际请求一致的本地测试 Client。

| 登记字段 | 本地 Samples 的要求 |
| --- | --- |
| Client ID | 与 `VITE_APP_OAUTH_CLIENT_ID` 一致，例如自建 `samples-local-web` |
| 认证方式 | `client_secret_post`，匹配前端表单中的 client_secret |
| 授权方式 | `password`；需要刷新时另允许 `refresh_token` |
| Secret | 与 `VITE_APP_OAUTH_CLIENT_SECRET` 一致、至少 16 字符的本地测试值；不要使用生产凭据 |
| Scopes | 与 `VITE_APP_OAUTH_SCOPE` 一致；多个 scope 在请求中以空格分隔 |
| 用户类型与租户 | 与测试用户所属类型、租户一致；选择平台中实际存在的值 |
| 浏览器允许 Origin | 本地使用 `http://127.0.0.1:5800`，与浏览器实际打开的地址一致 |

同步修改 Samples 的 `deploy/.env`。完整容器模式重建 / 重启 Admin 使运行配置生效；IDE + Vite 模式按[示例配置](/docs/latest/04_devmanual/模块说明/#env-与前端配置的边界)加载对应前端变量，并重启开发服务器。先从浏览器 Network 确认 `/oauth2/token` 返回 `access_token`，再检查用户与菜单接口。

这条兼容流程仅用于运行现有本地示例。新应用应采用授权码 + S256 PKCE 或由服务端 BFF 管理令牌；OAuth 安全实践已不允许以密码模式作为新接入方案，见 [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.4)。

### 新应用使用授权码与 PKCE

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

当前 Samples 尚未提供上述 PKCE 回调页面。采用这条新应用方案时，需要实际实现发起授权、保存并验证 state / code_verifier、处理回调、换取及管理令牌、退出等逻辑；请求 OIDC 时还需验证 ID Token。不能只修改 Client 登记字段就宣称已完成迁移。若由服务端 BFF 管理令牌，浏览器使用会话，服务端持有机密材料。

完成这条方案的验证后，再使用对应的访问令牌执行下方第 5 步；不要把本地兼容 Client 的 Secret 复制到新浏览器应用。

## 3. 对齐三个连接方向

| 调用方 | 配置 | 地址来源 |
| --- | --- | --- |
| 应用 Gateway → IAM | `spring.security.oauth2.resourceserver.opaquetoken.introspection-uri` 及 client-id / client-secret | 默认 `http://127.0.0.1:9010/oauth2/introspect`；使用有内省权限的服务端 Client |
| BFF → Cloud | `macula.cloud.endpoint` / `app-key` / `secret-key` | Cloud Gateway，默认 `http://127.0.0.1:9000`；填第 1 步的应用凭据 |
| BFF / Service → 应用 Gateway | `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` | Samples Gateway 的 JWK 地址，详见[请求链路](/docs/latest/00_introduce/请求链路/) |

Gateway 的 System Redis 应指向 **Cloud System 实际使用的同一 Redis 与数据库**，应用自身 Redis 则独立配置。当前 Samples 与 Cloud 的 `deploy/.env.example` 均使用宿主机 Redis 端口 `16379`；如果自己的部署改了端口或库号，同步覆盖 `MACULA_CLOUD_REDIS_PORT` 及相关连接配置。同样区分本机地址、容器 DNS 与浏览器可访问地址；IDE 不自动加载 `.env`。完整键名见[示例配置](/docs/latest/04_devmanual/模块说明/#示例配置)。

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
| AK/SK 提示归属租户不允许接入 | 应用 tenantId、目标网关应用名与租户编码前缀、System Redis 租户映射；不能用 authTenantId 绕过 |
| 认证成功但业务租户不符 | OAuth Client 的 tenantId / AK/SK 应用的 authTenantId，再核对临时 Holder 是否覆盖了认证租户 |
| Gateway 认证失败 | IAM 内省地址、Client 权限、System Redis 地址 |
| 下游 JWT 验签失败 | JWK 是否来自当前应用 Gateway、容器可达性、签名密钥一致性 |

这组步骤是接入验证方法；文档构建通过不代表当前部署已完成认证联调。
