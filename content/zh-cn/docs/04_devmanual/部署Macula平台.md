---
title: "部署Macula平台"
linkTitle: "部署Macula平台"
weight: 2
---

## (1) github代码clone                

```text
## 后端代码
git clone https://github.com/macula-projects/macula-cloud.git	
## 前端代码
git clone https://github.com/macula-projects/macula-cloud-admin.git
```

## (2) 本地代码配置修改

*（Macula平台本地运行需要修改的配置，都需要明确标注说明，如数据库【包括DDL初始化】、缓存、注册中心、配置中心、消息队列、网关地址、认证中心地址等【文字+截图】）*

- 前端项目

  * 修改 .env.development 文件为如下配置（根据实际情况调整）
  
    ```text
    VITE_APP_PROXY = false
    VITE_APP_TITLE = macula-samples(local)
    VITE_APP_API_BASEURL = http://localhost:9000 # gateway 地址
    VITE_APP_IAM_URL=http://localhost:9010 # IAM 地址
    ```

- 后端项目

    只有macula-cloud-iam、macula-cloud-system和macula-cloud-gateway是必须的。

  * 初始化数据库脚本/macula-cloud/blob/main/macula-cloud-system/docs/macula-system-dump.sql

  * 修改macula-cloud-iam 项目bootstrap.yml配置 

    ```yaml
    server:
      port: 9010

    spring:
      profiles:
        active: dev ## 指定程序以dev环境启动
    application:
      name: macula-cloud-iam
    cloud:
      nacos:
        username: ${nacos.username}
        password: ${nacos.password}
        config:
          server-addr: ${nacos.config.server-addr}
          namespace: ${nacos.config.namespace}
          # group:
          refresh-enabled: true
          file-extension: yml

    ---
    spring:
      config:
        activate:
          on-profile: dev
    nacos:
      username: ## dev环境的nacos用户名
      password: ## dev环境的nacos密码
      config:
        server-addr: ## dev环境的nacos服务地址
        namespace: ## dev环境的nacos命名空间
    ```

  * 修改macula-cloud-iam 项目application.yml配置

    ```yaml
    spring:
      datasource:
        type: com.alibaba.druid.pool.DruidDataSource
        driver-class-name: com.mysql.cj.jdbc.Driver
        url: jdbc:mysql://127.0.0.1:3306/macula-system?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&autoReconnect=true ## mysql数据库地址及数据库名
        username: ## mysql数据库用户名
        password: ## mysql数据库密码
      redis:
        database: 0
        host: ## redis服务器地址
        port: ## redis服务开放端口
      cache:
        # 缓存类型 redis、none(不使用缓存)
        type: redis
      cloud:
        nacos:
          discovery:
            enabled: true
            server-addr: ${nacos.config.server-addr}
            namespace: ${nacos.config.namespace}
            # group:
        sentinel:
          enabled: false
    macula:
      security:
        ignore-urls:
          - /swagger-ui/index.html
          - /v3/api-docs/swagger-config
      cloud:
        iam:
          issuer-uri: http://127.0.0.1:9010

    mybatis-plus:
      configuration:
        # 这个配置会将执行的sql打印出来，在开发或测试的时候可以用
        log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
      type-handlers-package: dev.macula.boot.starter.mp.handler

    feign:
      httpclient:
        enabled: false
        max-connections: 200 # 线程池最大连接数，默认200
        time-to-live: 900 # 线程存活时间，单位秒，默认900
        connection-timeout: 2000  # 新建连接超时时间，单位ms, 默认2000
        follow-redirects: true # 是否允许重定向，默认true
        disable-ssl-validation: false # 是否禁止SSL检查， 默认false
        okhttp:
          read-timeout: 60s # 请求超时时间，Duration配置方式
      okhttp:
        enabled: true

    seata:
      enabled: false

    springdoc:
      api-docs:
        enabled: true  # 默认是true，用于开关API文档
      swagger-ui:
        enabled: true # 默认是true，用于开关API UI

    server:
      servlet:
        encoding:
          force: true

    logging:
      level:
        root: info
        dev.macula.cloud: debug
      file:
        name: ${user.home}/logs/${spring.application.name}/${spring.application.name}.log
    ```

  * 修改macula-cloud-gateway 项目bootstrap.yml配置


    ```yaml
    server:
      port: 9000

    spring:
      profiles:
        active: dev ## 指定程序以dev环境启动
      application:
        name: macula-cloud-gateway
      cloud:
        nacos:
          username: ${nacos.username}
          password: ${nacos.password}
          config:
            server-addr: ${nacos.config.server-addr}
            namespace: ${nacos.config.namespace}
            # group:
            refresh-enabled: true
            file-extension: yml

    ---
    spring:
      config:
        activate:
          on-profile: dev
    nacos:
      username: ## dev环境的nacos用户名
      password: ## dev环境的nacos密码
      config:
        server-addr: ## dev环境的nacos服务地址
        namespace: ## dev环境的nacos命名空间
    ```

  * 修改macula-cloud-gateway 项目application.yml配置

    ```yaml
    spring:
      cloud:
        nacos:
          discovery:
            enabled: true
            server-addr: ${nacos.config.server-addr}
            namespace: ${nacos.config.namespace}
            # group:
        gateway:
          routes:
            - id: macula-cloud-system
              uri: lb://macula-cloud-system
              predicates:
                - Path=/system/**
              filters:
                - StripPrefix=1
      security:
        oauth2:
          resourceserver:
            opaquetoken:
              client-id: ## iam申请的客户端id
              client-secret: ## iam申请指定客户端id的密钥
              introspection-uri: http://127.0.0.1:9010/oauth2/introspect ## iam的提供的token认证introspect接口
      redis:
        database: 0
        host: ## gateway的redis服务器地址
        port: ## system的redis服务开放端口
        system:
          database: 0
          host: ## system的redis服务器地址 
          port: ## system的redis服务开放端口

    macula:
      gateway:
        sign-switch: true                       # 接口签名全局开关，默认true
        force-sign: false                       # 是否强制校验指定URL的接口签名，默认false
        crypto-switch: true                    # 接口加解密全局开关，默认true
        force-crypto: false                    # 是否强制校验指定URL的接口要不要加解密，默认false
        protect-urls: # 需要保护的URL，前端可通过/gateway/protect/urls获取
          crypto: # 加密
            - /system/api/v1/app
          sign: # 签名
            - /system/api/v1/app
        security:
          only-auth-urls: /mallapi/**
          ignore-urls:
            - /system/api/token
            - /system/api/token/introspect

    logging:
      level:
        root: info
        dev.macula.cloud: debug
      file:
        name: ${user.home}/logs/${spring.application.name}/${spring.application.name}.log
    ```

  * 修改macula-cloud-system 项目bootstrap.yml配置

    ```yaml
    server:
      port: 8081

    spring:
      profiles:
        active: dev ## 指定程序以dev环境启动
      application:
        name: macula-cloud-system
      cloud:
        nacos:
          username: ${nacos.username}
          password: ${nacos.password}
          config:
            server-addr: ${nacos.config.server-addr}
            namespace: ${nacos.config.namespace}
            # group:
            refresh-enabled: true
            file-extension: yml

    ---
    spring:
      config:
        activate:
          on-profile: dev
    nacos:
      username: ## dev环境的nacos用户名
      password: ## dev环境的nacos密码
      config:
        server-addr: ## dev环境的nacos服务地址
        namespace: ## dev环境的nacos命名空间
    ```

  * 修改macula-cloud-system 项目application.yml配置

    ```yaml
    spring:
      datasource:
        type: com.alibaba.druid.pool.DruidDataSource
        driver-class-name: com.mysql.cj.jdbc.Driver
        url: jdbc:mysql://127.0.0.1:3306/macula-system?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&autoReconnect=true ## mysql数据库地址及数据库名
        username: ## mysql数据库用户名
        password: ## mysql数据库密码
      redis:
        database: 0
        host: ## redis服务器地址
        port: ## redis服务开放端口
      cache:
        # 缓存类型 redis、none(不使用缓存)
        type: redis
      security:
        oauth2:
          resourceserver:
            jwt:
              jwk-set-uri: http://127.0.0.1:9000/oauth2/jwks ## gateway开放出来的jwks获取路径
      cloud:
        nacos:
          discovery:
            enabled: true
            server-addr: ${nacos.config.server-addr}
            namespace: ${nacos.config.namespace}
            # group:
            metadata:
              version: v1
        sentinel:
          enabled: false
    macula:
      security:
        ignore-urls:
          - /api/token
          - /api/token/**
          - /swagger-ui/index.html
          - /v3/api-docs/swagger-config

    mybatis-plus:
      type-handlers-package: dev.macula.boot.starter.mp.handler

    feign:
      httpclient:
        enabled: false
        max-connections: 200 # 线程池最大连接数，默认200
        time-to-live: 900 # 线程存活时间，单位秒，默认900
        connection-timeout: 2000  # 新建连接超时时间，单位ms, 默认2000
        follow-redirects: true # 是否允许重定向，默认true
        disable-ssl-validation: false # 是否禁止SSL检查， 默认false
        okhttp:
          read-timeout: 60s # 请求超时时间，Duration配置方式
      okhttp:
        enabled: true

    seata:
      enabled: false

    springdoc:
      api-docs:
        enabled: true  # 默认是true，用于开关API文档
      swagger-ui:
        enabled: true # 默认是true，用于开关API UI

    server:
      servlet:
        encoding:
          force: true

    logging:
      level:
        root: info
        dev.macula.cloud: debug
      file:
        name: ${user.home}/logs/${spring.application.name}/${spring.application.name}.log
    ```

## (3) 本地代码构建运行

*（前端项目和后端项目完成构建后，启动运行，需要标注说明构建和运行的命令以及运行效果【文字+截图】）*

* 前端项目

    进行前端项目IDE（如VisualCode），执行命令：

    ```text
    npm install				# 安装npm依赖包
    npm run dev				# 本地运行前端应用
    ```

    打开浏览器，访问前端配置的网址，如`http://localhost:5900/`，成功进入登录页面，即前端启动成功。

    ![image](../images/vue-started.png)

* 后端项目

    打开IDE（如iDEA），启动macula-cloud-iam、macula-cloud-gateway和macula-cloud-system（其它模块按需启动使用）。使用默认账号密码admin/admin登录系统，进入控制台，即平台运行成功。

    ![image](../images/vue-login-success.png)


