---
title: "统一认证"
linkTitle: "统一认证"
weight: 1
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-cloud", "branch": "main", "commit": "6744045ab560a42af11a913cc59628a65ac9dd1a", "paths": ["macula-cloud-iam/README.md", "macula-cloud-iam/pom.xml", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/ProtocolCasConfiguration.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/ProtocolSaml2Configuration.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/authentication/sms/SmsLoginFilterConfigurer.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/ProtocolOAuth2Configuration.java", "macula-cloud-iam/src/main/java/dev/macula/cloud/iam/config/DefaultSecurityConfiguration.java", "macula-cloud-admin/src/views/system/oauth2Client/index.vue"]}]
---

## 概览

Macula Cloud IAM 是统一身份认证与授权中心，提供 OAuth 2.1 / OpenID Connect 登录、令牌签发、刷新、撤销、内省及公钥发布。用户名、手机号、邮箱、验证码以及第三方身份的接入按 OAuth Client 与 Provider 注册配置管理。

IAM 管理身份与外部令牌；Gateway 负责入口认证、角色/菜单/URL 控制并签发内部 JWT；BFF 和服务通过 Security 实施方法与资源权限。参见[请求链路](/docs/latest/00_introduce/应用架构/)。

## 组件坐标

IAM 为独立部署的 `macula-cloud-iam` 服务，不是业务工程的 Maven 库，没有 IAM Starter 坐标。管理端位于 Macula Cloud 同仓的 `macula-cloud-admin`。

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        opaquetoken:
          introspection-uri: ${IAM_INTROSPECTION_URI:http://127.0.0.1:9010/oauth2/introspect}
          client-id: ${IAM_INTROSPECTION_CLIENT_ID}
          client-secret: ${IAM_INTROSPECTION_CLIENT_SECRET}
```

### 关键配置

#### 首次接入

先启动 Cloud，再登记业务应用及 OAuth Client，区分 AK/SK 和 Client Secret，完成菜单/角色分配。具体字段、兼容 Samples 登录方式及验证命令见[首次接入 Macula Cloud](/docs/latest/04_devmanual/首次接入macula-cloud/)。

#### Gateway 验证外部 Token

内省 Client 在平台登记并配置允许的认证方式，凭据只留服务端。BFF 的 Cloud endpoint 指向 Cloud Gateway，内部服务的 JWK 指向应用 Gateway，不能将这三个地址混用。

#### IAM 服务端

按 Cloud `deploy/README.md` 配置环境与数据库迁移；生产使用稳定的 `IAM_ISSUER_URI`、HTTPS、持久化签名密钥和加密密码。变更 issuer 或签名材料会影响既有令牌，发布前核对回调、密钥和缓存策略。

## 核心功能

### OAuth 与 OIDC

浏览器/移动公共客户端使用授权码和 S256 PKCE；服务身份使用 `client_credentials`。授权方式、scope、租户、回调与精确 Origin 均按 Client 管理。`password`、`sms` 等旧令牌扩展用于兼容现有客户端，新浏览器接入不沿用密码授权或暴露 Secret。

常用端点：

| 路径 | 用途 |
| --- | --- |
| `/login` | 统一登录页 |
| `/oauth2/authorize` | OAuth 2.1 / OIDC 授权入口 |
| `/oauth2/token` | 获取或刷新令牌 |
| `/oauth2/introspect` | 查询令牌状态 |
| `/oauth2/revoke` | 撤销令牌 |
| `/.well-known/openid-configuration` | OIDC Discovery |
| `/oauth2/jwks` | JWT 验签公钥 |
| `/userinfo` | 获取已授权的用户信息 |
| `/connect/logout` | OIDC 退出 |


### 登录与第三方身份

支持本地账号、手机号/邮箱及验证码登录。短信验证码发送入口为 `/api/v1/sms-code`，表单登录处理地址为 `POST /login/sms`。登录链路已有 Sms Filter / Provider / 验证服务实现，不再使用旧文档的 `/login/captcha` TODO。实际短信发送仍需部署方配置供应商和验证存储，不能将接口存在视为真实短信已联通。

GitHub、企业微信、飞书、钉钉、微信等第三方登录需创建对应 Provider 注册并绑定到 Client。浏览器、App SDK、小程序和 WebView 使用的 code 类型与供应商接口不同，按管理端终端与登录方式选择，不互换认证凭据。

当前提交的 `ProtocolCasConfiguration` 与 `ProtocolSaml2Configuration` 仍为空配置类，不构成已可接入的 CAS / SAML 协议实现。本页不沿用 5.x 的 TODO 接口或旧 Spring Authorization Server 0.4.x 配置；需要这些协议时应另行实现并验证。

## 依赖引入

业务 Gateway 按云平台选择 Alibaba SCG 或 Tencent SCG 组合 Starter，见 [Gateway](/docs/latest/01_services/微服务/gateway/)；内层引入 [Security](/docs/latest/01_services/框架基础/security/) 验证内部 JWT，BFF 引入 [System](/docs/latest/01_services/通用平台/system/)获取平台用户与菜单。组合 Starter 已传递引入的依赖不用重复声明。

## 版权说明

Macula Cloud 使用 [Apache License 2.0](https://github.com/macula-projects/macula-cloud/blob/main/LICENSE)。Spring Security 等第三方组件遵循各自许可证。
