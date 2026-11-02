---
aliases: ["/docs/98_old/v4.0/advance/02_nacos/", "/docs/5.x/98_old/v4.0/advance/02_nacos/", "/docs/6.0.x/98_old/v4.0/advance/02_nacos/", "/docs/latest/98_old/v4.0/advance/02_nacos/", "/docs/v4.0/advance/02_nacos/"]
type: docs
title: "Nacos :  动态服务发现、配置管理平台"
linkTitle: "Nacos :  动态服务发现、配置管理平台"
weight: 1
description: "一个更易于构建云原生应用的动态服务发现、配置管理和服务管理平台."
---

### 什么是 Nacos ?

>  Nacos 致力于帮助您发现、配置和管理微服务。Nacos 提供了一组简单易用的特性集，帮助您快速实现动态服务发现、服务配置、服务元数据及流量管理
>  Nacos 帮助您更敏捷和容易地构建、交付和管理微服务平台。 Nacos 是构建以“服务”为中心的现代应用架构 (例如微服务范式、云原生范式) 的服务基础设施
* **服务发现和服务健康监测**
>   Nacos 支持基于 DNS 和基于 RPC 的服务发现。服务提供者使用 [原生SDK](https://nacos.io/zh-cn/docs/sdk.html)、[OpenAPI](https://nacos.io/zh-cn/docs/open-api.html)、或一个[独立的Agent TODO](https://nacos.io/zh-cn/docs/other-language.html)注册 Service 后，服务消费者可以使用[DNS TODO](https://nacos.io/zh-cn/docs/xx) 或[HTTP&API](https://nacos.io/zh-cn/docs/open-api.html)查找和发现服务。
>Nacos 提供对服务的实时的健康检查，阻止向不健康的主机或服务实例发送请求。Nacos 支持传输层 (PING 或 TCP)和应用层 (如 HTTP、MySQL、用户自定义）的健康检查。 对于复杂的云环境和网络拓扑环境中（如 VPC、边缘网络等）服务的健康检查，Nacos 提供了 agent 上报模式和服务端主动检测2种健康检查模式。Nacos 还提供了统一的健康检查仪表盘，帮助您根据健康状态管理服务的可用性及流量。
* **动态配置服务**
>   动态配置服务可以让您以中心化、外部化和动态化的方式管理所有环境的应用配置和服务配置。
>动态配置消除了配置变更时重新部署应用和服务的需要，让配置管理变得更加高效和敏捷。
>配置中心化管理让实现无状态服务变得更简单，让服务按需弹性扩展变得更容易。
>   Nacos 提供了一个简洁易用的UI ([控制台样例 Demo](http://console.nacos.io/nacos/index.html)) 帮助您管理所有的服务和应用的配置。Nacos 还提供包括配置版本跟踪、金丝雀发布、一键回滚配置以及客户端配置更新状态跟踪在内的一系列开箱即用的配置管理特性，帮助您更安全地在生产环境中管理配置变更和降低配置变更带来的风险。
* **动态 DNS 服务**
>  动态 DNS 服务支持权重路由，让您更容易地实现中间层负载均衡、更灵活的路由策略、流量控制以及数据中心内网的简单DNS解析服务。动态DNS服务还能让您更容易地实现以 DNS 协议为基础的服务发现，以帮助您消除耦合到厂商私有服务发现 API 上的风险。
>  Nacos 提供了一些简单的 [DNS APIs TODO](https://nacos.io/zh-cn/docs/xx) 帮助您管理服务的关联域名和可用的 IP:PORT 列表.
* **服务及其元数据管理**
>   Nacos 能让您从微服务平台建设的视角管理数据中心的所有服务及元数据，包括管理服务的描述、生命周期、服务的静态依赖分析、服务的健康状态、服务的流量管理、路由及安全策略、服务的 SLA 以及最首要的 metrics 统计数据。

#### Nacos 地图

一图看懂 Nacos.

![图片](../../imgs/Nacos1.png)
* **特性大图**：要从功能特性，非功能特性，全面介绍我们要解的问题域的特性诉求
* **架构大图**：通过清晰架构，让您快速进入 Nacos 世界
* **业务大图**：利用当前特性可以支持的业务场景，及其最佳实践
* **生态大图**：系统梳理 Nacos 和主流技术生态的关系
* **优势大图**：展示 Nacos 核心竞争力
* **战略大图**：要从战略到战术层面讲 Nacos 的宏观优势
#### **Nacos 生态**

![图片](../../imgs/Nacos2.png)

如 Nacos 全景图所示，Nacos 无缝支持一些主流的开源生态，例如

* [Spring Cloud](https://nacos.io/en-us/docs/quick-start-spring-cloud.html)
* [Apache Dubbo and Dubbo Mesh](https://nacos.io/zh-cn/docs/use-nacos-with-dubbo.html)
* [Kubernetes and CNCF](https://nacos.io/zh-cn/docs/use-nacos-with-kubernetes.html)

使用 Nacos 简化服务发现、配置管理、服务治理及管理的解决方案，让微服务的发现、管理、共享、组合更加容易。

关于如何在这些生态中使用 Nacos，请参考以下文档：

* [Nacos与Spring Cloud一起使用](https://nacos.io/zh-cn/docs/use-nacos-with-springcloud.html)
* [Nacos与Kubernetes一起使用](https://nacos.io/zh-cn/docs/use-nacos-with-kubernetes.html)
* [Nacos与Dubbo一起使用](https://nacos.io/zh-cn/docs/use-nacos-with-dubbo.html)
* [Nacos与gRPC一起使用](https://nacos.io/zh-cn/docs/roadmap.html)
* [Nacos与Istio一起使用](https://nacos.io/zh-cn/docs/use-nacos-with-istio.html)
### **Quick Start**

在 Springboot项目中使用 Nacos.

#### **STEP  1.   添加依赖**

在应用 pom.xml 中 加入以下代码即可：

```plain

<parent>
    <groupId>org.maculaframework</groupId>
    <artifactId>macula-parent</artifactId>
    <version>4.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
<!-- nacos 相关依赖 -->
<dependency>
    <groupId>org.maculaframework</groupId>
    <artifactId>macula-cloud-nacos</artifactId>
</dependency>
```

**macula-cloud-nacos 集成了 nacos 配置中心 ， 以及 服务注册/发现等 组件功能， 可根据需要 ，使用 nacos 提供的服务**

#### **STEP  2.  使用案例**

**Nacos 作为 配置中心示例：**

基于 nacos 的 配置中心 应用配置

```yaml
spring:
  # nacos 配置中心相关配置  
  cloud:
    nacos:
      config:
        enabled: true
        # 配置文件 后缀格式， 比如.yaml、 .properties  
        file-extension: yaml 
        # 配置中心地址
        server-addr: ${macula.nacos.url}
        # 配置所在空间 比如 Macula
        namespace: ${macula.nacos.namespace}
        # 配置中心 用户验证 
        username: ${macula.nacos.username}
        password: ${macula.nacos.password}
        # 扩展配置
        extension-configs:
          - data-id: xxxxx.yaml
            refresh: true
---
spring:
  profiles: dev
macula:
  nacos:
    url: https://127.0.0.1
    username: macula
    password: macula123
    namespace: MACULA-DEV
```

**Nacos 配置中心具体**：[请查看前几章 Nacos 配置中心应用配置文件](README.md:216) 

![图片](../../imgs/Nacos3.png)

**Nacos 作为 注册中心**

配置文件中， 配置 Nacos 配置中心地址

```plain
spring:
  application:
    name: pf-recruit // 设置项目名称
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848 // Nacos服务接口(不能加http前缀)，直接访问localhost:8848/nacos可以进入管理页面
```
 
启动类中开启服务发现.

```java
@SpringBootApplication
@EnableDiscoveryClient
public class RecruitApplication {
    public static void main(String[] args) {
        SpringApplication.run(RecruitApplication.class, args);
    }
}
```
 
以上就是 Nacos 全部内容
