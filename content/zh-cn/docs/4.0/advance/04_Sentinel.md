---
aliases: ["/docs/98_old/v4.0/advance/04_sentinel/", "/docs/5.x/98_old/v4.0/advance/04_sentinel/", "/docs/6.0.x/98_old/v4.0/advance/04_sentinel/", "/docs/latest/98_old/v4.0/advance/04_sentinel/", "/docs/v4.0/advance/04_sentinel/"]
type: docs
title: "Sentinel ：分布式系统的流量防卫兵"
linkTitle: "Sentinel ：分布式系统的流量防卫兵"
weight: 1
description: ""
---

### Sentinel 是什么？

随着微服务的流行，服务和服务之间的稳定性变得越来越重要。Sentinel 以流量为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。

#### Sentinel 具有以下特征:

**丰富的应用场景**：Sentinel 承接了阿里巴巴近 10 年的双十一大促流量的核心场景，例如秒杀（即突发流量控制在系统容量可以承受的范围）、消息削峰填谷、集群流量控制、实时熔断下游不可用应用等。

**完备的实时监控**：Sentinel 同时提供实时的监控功能。您可以在控制台中看到接入应用的单台机器秒级数据，甚至 500 台以下规模的集群的汇总运行情况。

**广泛的开源生态**：Sentinel 提供开箱即用的与其它开源框架/库的整合模块，例如与 Spring Cloud、Apache Dubbo、gRPC、Quarkus 的整合。您只需要引入相应的依赖并进行简单的配置即可快速地接入 Sentinel。同时 Sentinel 提供 Java/Go/C++ 等多语言的原生实现。

**完善的 SPI 扩展机制**：Sentinel 提供简单易用、完善的 SPI 扩展接口。您可以通过实现扩展接口来快速地定制逻辑。例如定制规则管理、适配动态数据源等。

#### **Sentinel 主要特性：**

![图片](../../imgs/Sentinel1.png)

#### **Sentinel 开源生态:**

![图片](../../imgs/Sentinel2.png)


### **Quick Start.**

#### **STEP 1.  添加依赖**

在应用 pom.xml 中 加入以下代码即可：

```java
<dependency>
    <groupId>org.macula.plugins</groupId>
    <artifactId>macula-plugins-sgs</artifactId>
    <version>3.1.3.RELEASE</version>
</dependency>
```

如果未使用依赖管理工具，请自行去公司 **Maven Center Repository** 下载 JAR 包   

**已知问题**  macula-plugins-sgs  中引入了  nacos-client 版本与公司部署的Nacos 兼容有问题

```java
check-update] get changed dataId error, code: 403
```
建议 排除掉 macula-plugins-sgs中的 nacos-client ， 手动引入  nacos-client 1.4.0 以上版本 
```plain
<dependency>
    <groupId>com.alibaba.nacos</groupId>
    <artifactId>nacos-client</artifactId>
    <version>1.4.0</version>
</dependency>
<dependency>
    <groupId>org.macula.plugins</groupId>
    <artifactId>macula-plugins-sgs</artifactId>
    <version>3.1.3.RELEASE</version>
    <exclusions>
        <exclusion>
            <groupId>com.alibaba.nacos</groupId>
            <artifactId>nacos-client</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

#### **STEP 2.  添加配置**

  目前sentinel 已集成 nacos 存储流控规则，实现流控规则双向推拉

**构建 NacosSubscriber** 

* **TransportConfig.CONSOLE_SERVER**  配置 sentinel 控制台地址,  注册客户端信息
* **NacosSubscriber**  构造方法,  配置Nacos地址信息， 用于订阅 ，存储Sentinel 流控规则,  项目启动时自动注册规则信息
* 构造参数信息
    * **serverAddr**    Nacos 配置中心地址
    * **namespace**   Nacos 配置中心空间名 ， 默认 ： SENTINEL
    * **username**      Nacos 配置中心登陆账号
    * **password**      Nacos 配置中心登陆密码
    * **groupId**         Nacos 配置分组  ， 默认 SENTINEL_GROUP
    * **appName**      应用Name,  框架内部基于 appName + 指定后缀名 构建 唯一流控规则配置名. 

```java
@Bean
public NacosSubscriber nacosSubscriber() {
  // 配置 Sentinel Dashboard 控制台地址, 注意:无需HTTP协议前缀
  System.setProperty(TransportConfig.CONSOLE_SERVER, "ss-dev.infinitus.com.cn");
  // nacos 配置需 IP：port 或 domain:port 
  // example should like ip:port or domain:port
  return new NacosSubscriber("nacos-dev.infinitsu.com.cn:80", "SENTIENL", "nacos", "nacosxxxx123", "SENTINEL_GROUP", "esb-demo" );
}
```

以上就是 流控系统接入 的内容 ， 实测 **Dubbo** 系统 接入 ok .
**Web端  需额外添加配置 过滤web请求**

```java
@Bean
@ConditionalOnBean(NacosSubscriber.class)
public FilterRegistrationBean sentinelFilterRegistration() {
    FilterRegistrationBean<Filter> registration = new FilterRegistrationBean<>();
    registration.setFilter(new CommonFilter());
    registration.addUrlPatterns("/*");
    registration.setName("sentinelFilter");
    registration.setOrder(1);
    return registration;
}
```


#### **STEP 3.  启动项目**

**应用启动以后， 请求接口， 将在控制台显示请求数据**

**Sentinel 控制台**：https://sgs-dev.infinitus.com.cn

![Sentinel3.png](../../imgs/Sentinel3.png)


**通过配置流控规则 ，自动同步到Nacos 配置中心， 实现规则持久化，修改配置中心规则同样将反向推送到Sentinel**

![图片](../../imgs/Sentinel4.png)

![图片](../../imgs/Sentinel5.png)