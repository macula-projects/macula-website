---
title: "Macula Boot Starter Wechat"
linkTitle: "微信接入"
weight: 20
source_path: "macula-boot-starters/macula-boot-starter-wechat/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-wechat/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

微信Java开发工具包，支持包括微信支付、开放平台、公众号、企业微信、视频号、小程序等微信功能模块的后端开发。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
   <groupId>dev.macula.boot</groupId>
   <artifactId>macula-boot-starter-wechat</artifactId>
</dependency>

<!-- 以下 SDK 按实际功能选择；企业微信单账号与多账号方案择一 -->
<!-- 开放平台 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-open-spring-boot-starter</artifactId>
</dependency>

<!-- 公众号 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-mp-spring-boot-starter</artifactId>
</dependency>

<!-- 企业微信 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-cp-spring-boot-starter</artifactId>
</dependency>

<!-- 企业微信多账号 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-cp-multi-spring-boot-starter</artifactId>
</dependency>

<!-- 小程序 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-miniapp-spring-boot-starter</artifactId>
</dependency>

<!-- 微信支付 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-pay-spring-boot-starter</artifactId>
</dependency>

<!-- 视频号 -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>wx-java-channel-spring-boot-starter</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。不同应用、文件或替代方案分别标注，请按场景选用。

#### application.yml：开放平台、公众号、小程序、视频号（按需保留）

```yaml
wx:
  open:
    # 公众号配置(必填)
    appId: '@appId'
    secret: '@secret'
    token: '@token'
    aesKey: '@aesKey'
    config-storage:
      # 存储配置redis(可选)
      # 优先注入容器的(JedisPool, RedissonClient), 当配置了wx.open.config-storage.redis.host, 不会使用容器注入redis连接配置
      type: 'redistemplate'            # 配置类型: memory(默认), redis(jedis), jedis, redisson,redistemplate'
      key-prefix: 'wx:open'            # 相关redis前缀配置: wx:open(默认)'
      http-client-type: 'httpclient'   # http客户端类型: httpclient(默认)'
      http-proxy-host: ''              # http客户端配置
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
      max-retry-times: 5               # 最大重试次数，默认：5 次，如果小于 0，则为 0
      retry-sleep-millis: 1000         # 重试时间间隔步进，默认：1000 毫秒，如果小于 0，则为 1000
  mp:
    appId: appId
    secret: '@secret'
    token: '@token'
    aesKey: '@aesKey'
    config-storage:
      type: 'RedisTemplate'            # 配置类型: Memory(默认), Jedis,RedisTemplate,Redisson
      key-prefix: 'wx'                 # 相关redis前缀配置: wx(默认)
      http-client-type: 'httpclient'   # http客户端类型: HttpClient(默认), OkHttp, JoddHttp，用其他的要引入对应jar包
      http-proxy-host: ''
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
  miniapp:
    appid: appId
    secret: '@secret'
    token: '@token'
    aesKey: '@aesKey'
    msgDataFormat: '@msgDataFormat'       # 消息格式，XML或者JSON.
    config-storage:
      type: 'RedisTemplate'               # 配置类型: Memory(默认), Jedis, RedisTemplate, Redisson
      key-prefix: 'wa'                    # 相关redis前缀配置: wa(默认)
      http-client-type: 'HttpClient'      # http客户端类型: HttpClient(默认), OkHttp, JoddHttp
      http-proxy-host: ''
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
  channel:
    appid: appId                          # 设置视频号小店的appid
    secret: '@secret'                     # 设置视频号小店的Secret
    token: '@token'                       # 设置视频号小店消息服务器配置的token.
    aesKey: '@aesKey'                     # 设置视频号小店消息服务器配置的EncodingAESKey
    msgDataFormat: '@msgDataFormat'       # 消息格式，XML或者JSON.
    config-storage:
      type: 'RedisTemplate'               # 配置类型: Memory(默认), Jedis, RedisTemplate, Redisson
      key-prefix: 'wh'                    # 相关redis前缀配置: wh(默认)
      http-client-type: 'HttpClient'      # http客户端类型: HttpClient(默认), OkHttp, JoddHttp
      http-proxy-host: ''
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
```

#### application.yml：企业微信单账号

```yaml
wx:
  cp:
    # 企业微信号配置(必填)
    corp-id: '@corp-id'
    corp-secret: '@corp-secret'
    # 选填
    agent-id: '@agent-id'
    token: '@token'
    aes-key: '@aes-key'
    msg-audit-lib-path: '@msg-audit-lib-path'
    msg-audit-priKey: '@msg-audit-priKey'
    config-storage:
      type: 'redistemplate'                # 配置类型: memory(默认), jedis, redisson, redistemplate
      key-prefix: 'wx:cp'                  # 相关redis前缀配置: wx:cp(默认)
      http-proxy-host: ''
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
      max-retry-times: 5
      retry-sleep-millis: 1000
```

#### application.yml：企业微信多账号（与单账号方案择一）

```yaml
wx:
  cp:
    corps:
      tenantId1:
        # 应用 1 配置
        corp-id: '@corp-id'
        corp-secret: '@corp-secret'
        # 选填
        agent-id: '@agent-id'
        token: '@token'
        aes-key: '@aes-key'
        msg-audit-lib-path: '@msg-audit-lib-path'
        msg-audit-priKey: '@msg-audit-priKey'
      tenantId2:
        # 应用 2 配置
        corp-id: '@corp-id'
        corp-secret: '@corp-secret'
        # 选填
        agent-id: '@agent-id'
        token: '@token'
        aes-key: '@aes-key'
        msg-audit-lib-path: '@msg-audit-lib-path'
        msg-audit-priKey: '@msg-audit-priKey'
    # 公共配置
    ## ConfigStorage 配置（选填）
    config-storage:
      type: 'redistemplate'               # 配置类型: memory(默认), jedis, redisson, redistemplate'
      key-prefix: 'wx:cp'                 # 相关redis前缀配置: wx:cp(默认)
      ## http 客户端配置（选填）
      http-proxy-host: ''
      http-proxy-password: ''
      http-proxy-port: ''
      http-proxy-username: ''
      ## 最大重试次数，默认：5 次，如果小于 0，则为 0
      max-retry-times: 5
      ## 重试时间间隔步进，默认：1000 毫秒，如果小于 0，则为 1000
      retry-sleep-millis: 1000
```

#### application.yml：微信支付 V2

```yaml
wx:
  pay:
    appId:
    mchId:
    mchKey:
    keyPath:
```

#### application.yml：微信支付 V3

```yaml
wx:
  pay:
    appId: xxxxxxxxxxx
    mchId: 15xxxxxxxxx #商户id
    apiV3Key: Dc1DBwSc094jACxxxxxxxxxxxxxxx #V3密钥
    certSerialNo: 62C6CEAA360BCxxxxxxxxxxxxxxx
    privateKeyPath: classpath:cert/apiclient_key.pem #apiclient_key.pem证书文件的绝对路径或者以classpath:开头的类路径
    privateCertPath: classpath:cert/apiclient_cert.pem #apiclient_cert.pem证书文件的绝对路径或者以classpath:开头的类路径
```

#### application.yml：微信支付 V3 服务商模式

```yaml
wx:
  pay: #微信服务商支付
    configs:
    - appId: wxe97b2x9c2b3d #spAppId
      mchId: 16486610 #服务商商户
      subAppId: wx118cexxe3c07679 #子appId
      subMchId: 16496705 #子商户
      apiV3Key: Dc1DBwSc094jAKDGR5aqqb7PTHr #apiV3密钥
      privateKeyPath: classpath:cert/apiclient_key.pem #服务商证书文件，apiclient_key.pem证书文件的绝对路径或者以classpath:开头的类路径（可以配置绝对路径）
      privateCertPath: classpath:cert/apiclient_cert.pem #apiclient_cert.pem证书文件的绝对路径或者以classpath:开头的类路径
```

### 关键配置

| 配置 | 说明 |
| --- | --- |
| `wx.open / wx.mp / wx.miniapp / wx.channel` | 按所用微信产品分别提供应用身份与回调凭据。 |
| `wx.cp / wx.cp.corps` | 企业微信单账号与多账号方案按需择一。 |
| `wx.pay` | 按实际支付协议选择 V2、V3 或服务商方案。 |
| `config-storage` | 各 SDK 的存储、HTTP 客户端及重试选项，具体字段以对应示例为准。 |

配置使用上方各 SDK 的 `wx.*` 前缀，无统一 `macula.wechat.*` 开关。应用需显式引入所用能力的 Starter；Secret、Token、AES Key 和支付证书应由环境注入。集群部署需选择共享配置存储，不应沿用单机内存存储。

#### 开放平台

自动注入的类型：

- WxOpenService
- WxOpenMessageRouter
- WxOpenComponentService

#### 公众号

自动注入的类型：

- WxMpService
- WxMpConfigStorage

#### 企业微信

自动注入的类型：

- WxCpService
- WxCpConfigStorage

自定义同类型 Bean 可覆盖默认配置：

- WxCpService
- WxCpConfigStorage

#### 企业微信多账号

企业微信多账号配置

- 实现多 WxCpService 初始化。
- 未实现 WxCpTpService 初始化，可参考多 WxCpService 配置的实现。
- 未实现 WxCpCgService 初始化，可参考多 WxCpService 配置的实现。

自动注入的类型：

- WxCpMultiServices

使用示例：

```java
@Service
public class DemoService {
  @Autowired
  private WxCpMultiServices wxCpMultiServices;

  public void test() {
    // 应用 1 的 WxCpService
    WxCpService wxCpService1 = wxCpMultiServices.getWxCpService("tenantId1");
    WxCpUserService userService1 = wxCpService1.getUserService();
    userService1.getUserId("xxx");
    // todo ...

    // 应用 2 的 WxCpService
    WxCpService wxCpService2 = wxCpMultiServices.getWxCpService("tenantId2");
    WxCpUserService userService2 = wxCpService2.getUserService();
    userService2.getUserId("xxx");
    // todo ...

    // 应用 3 的 WxCpService
    WxCpService wxCpService3 = wxCpMultiServices.getWxCpService("tenantId3");
    // 判断是否为空
    if (wxCpService3 == null) {
      // todo wxCpService3 为空，请先配置 tenantId3 企业微信应用参数
      return;
    }
    WxCpUserService userService3 = wxCpService3.getUserService();
    userService3.getUserId("xxx");
    // todo ...
  }
}
```

#### 小程序

自动注入的类型：

- WxMaService
- WxMaConfig

#### 微信支付

支付示例分为 V2、V3 和 V3 服务商模式，按实际接入协议选择对应配置。

#### 视频号

自动注入的类型：

- WxChannelService

## 核心功能

请参考[官方网站](https://github.com/Wechat-Group/WxJava/wiki)

## 依赖引入

```xml
<dependencies>
    <dependency>
        <groupId>dev.macula.boot</groupId>
        <artifactId>macula-boot-starter-redis</artifactId>
    </dependency>
    <!-- 微信开放平台 -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-open-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <!-- 微信公众号(服务号/订阅号) -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-mp-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <!-- 企业号/企业微信 -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-cp-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-cp-multi-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <!-- 微信小程序 -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-miniapp-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <!-- 微信支付 -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-pay-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
    <!-- 微信视频号 -->
    <dependency>
        <groupId>com.github.binarywang</groupId>
        <artifactId>wx-java-channel-spring-boot-starter</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## 版权说明

- WxJava: https://github.com/Wechat-Group/WxJava/blob/develop/LICENSE
