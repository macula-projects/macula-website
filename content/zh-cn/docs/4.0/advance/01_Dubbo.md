---
aliases: ["/docs/98_old/v4.0/advance/01_dubbo/", "/docs/5.x/98_old/v4.0/advance/01_dubbo/", "/docs/6.0.x/98_old/v4.0/advance/01_dubbo/", "/docs/latest/98_old/v4.0/advance/01_dubbo/", "/docs/v4.0/advance/01_dubbo/"]
type: docs
title: "Dubbo：高性能 RPC 分布式服务框架"
linkTitle: "Dubbo：高性能 RPC 分布式服务框架"
weight: 1
description: "Dubbo是阿里巴巴开源的基于 Java 的高性能 RPC（一种远程调用） 分布式服务框架（SOA），致力于提供高性能和透明化的RPC远程服务调用方案，以及SOA服务治理方案。Macula 架构使用 Dubbo Spring Cloud 为组件模块，项目中引入 macula-cloud-dubbo 便可直接用于分布式服务的使用。
"
---
### Dubbo Spring Cloud 主要特性

* 面向接口代理的高性能RPC调用：提供高性能的基于代理的远程调用能力，服务以接口为粒度，屏蔽了远程调用底层细节。
* 智能负载均衡：内置多种负载均衡策略，智能感知下游节点健康状况，显著减少调用延迟，提高系统吞吐量。
* 服务自动注册与发现：支持多种注册中心服务，服务实例上下线实时感知。
* 高度可扩展能力：遵循微内核+插件的设计原则，所有核心能力如Protocol、Transport、Serialization被设计为扩展点，平等对待内置实现和第三方实现。
* 运行期流量调度：内置条件、脚本等路由策略，通过配置不同的路由规则，轻松实现灰度发布，同机房优先等功能。
* 可视化的服务治理与运维：提供丰富服务治理、运维工具：随时查询服务元数据、服务健康状态及调用统计，实时下发路由策略、调整配置参数。
### 

### **Quick Start.**

1. **创建父工程demo-member**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.macula.base</groupId>
  <artifactId>demo-member</artifactId>
  <version>4.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>
  <modules>
    <module>demo-member-infra</module>
    <module>demo-member-admin</module>
    <module>demo-member-esb-api</module>
    <module>demo-member-esb-api-impl</module>
  </modules>
</project>
```
总项目中 modules 说明：
**demo-member-infra** :基础对象公共模块，存放对象实体类, Repostory, 公共服务类等。

**demo-member-admin** :管理端接口，本地服务接口调用。

**demo-member-esb-api** :Dubbo Api 定义。

**demo-member-esb-api-impl** :dubbo与rest服务供应商， Dubbo Api 的实现。

2. **子模块demo-member-esb-api** 

API模块，存放Dubbo服务接口和模型定义，非必要，这里创建仅为更好的代码重用以及接口、模型规格控制管理。

定义抽象接口UserApi.java：

```java
package org.macula.base.api;

import org.macula.base.vo.UserVo;

public interface UserApi {

  /**
   * 根据userName 获取用户
   */
  UserVo get(String userName);
  /**
   * 保存用户信息
   */
  boolean save(UserVo user);

}

```


3. **子模块 demo-member-esb-api-impl  Dubbo服务提供方**

pom.xml 依赖：

```java
<parent>
    <groupId>org.maculaframework</groupId>
    <artifactId>macula-parent</artifactId>
    <version>4.0.0-SNAPSHOT</version>
    <relativePath/>
</parent>
<!-- Dubbo 使用相关依赖 -->
<dependency>
  <groupId>org.maculaframework</groupId>
  <artifactId>macula-cloud-dubbo</artifactId>
</dependency>
<!-- nacos 注册中心相关依赖 -->
<dependency>
    <groupId>org.maculaframework</groupId>
    <artifactId>macula-cloud-nacos</artifactId>
</dependency>
<!--实现 demo-api 模块 -->
<dependency>
  <groupId>org.macula.base</groupId>
  <artifactId>demo-member-esb-api</artifactId>
  <version>${revision}</version>
</dependency>
<!-- 公共模块依赖 -->
<dependency>
  <groupId>org.macula.base</groupId>
  <artifactId>demo-member-infra</artifactId>
  <version>${revision}</version>
  <scope>compile</scope>
</dependency>
```
此处引入公共模块，API模块, 架构dubbo模块 等依赖。
实现Dubbo接口，UserApiImpl.java如下：

```java
package org.macula.base.api;
import org.apache.dubbo.config.annotation.DubboService;
import org.macula.base.member.domain.UserDemoEntity;
import org.macula.base.member.repository.UserDemoRepository;
import org.macula.base.vo.UserVo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.Assert;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import static org.springframework.util.MimeTypeUtils.APPLICATION_JSON_VALUE;

@DubboService(protocol = {"dubbo", "rest"})
@Path("/user")
public class UserApiImpl implements UserApi {

  @Autowired
  private UserDemoRepository userDemoRepository;
  
  @Override
  @Path("get")
  @GET
  @Produces(APPLICATION_JSON_VALUE)
  @Consumes(MediaType.APPLICATION_JSON)
  public UserVo get(@QueryParam("userName") String userName) {
    Assert.hasLength(userName, "macula.get.user.userName.notBlank");
    UserDemoEntity user = userDemoRepository.findByUserName(userName);
    if (user == null) {
      return null;
    }
    return convert(user);
  }
  
  @Override
  @Path("save")
  @POST
  @Produces(APPLICATION_JSON_VALUE)
  public boolean save(UserVo user) {
    Assert.notNull(user, "macula.sync.user.notNull");
    UserDemoEntity currentUser = userDemoRepository.findByUserName(user.getUserName());
    UserDemoEntity newUser = convert(user);
    if (currentUser != null) {
      BeanUtils.copyProperties(newUser, currentUser, "id");
      return userDemoRepository.save(currentUser).getId() != null;
    } else {
      return userDemoRepository.save(newUser).getId() != null;
    }
  }
  
  private UserVo convert(UserDemoEntity userEntity) {
    UserVo userVO = new UserVo();
    BeanUtils.copyProperties(userEntity, userVO);
    return userVO;
  }
  private UserDemoEntity convert(UserVo userVO) {
    UserDemoEntity userEntity = new UserDemoEntity();
    BeanUtils.copyProperties(userVO, userEntity);
    return userEntity;
  }
}
```
@DubboService 声明了Dubbo请求 与Rest请求 两种模式， @Path("/user") 为 rest 请求路径地址，结合方法路径上的 @Path("get") 发送 http 使用。
配置文件 application.yml 需要将Java服务（本地）配置为 Dubbo 服务（远程）如下：

```yaml
## 服务发现与注册配置
spring:
  cloud:
    nacos:
      discovery:
        server-addr: ${macula.nacos.url}
        namespace: ${macula.nacos.namespace}
        username: ${macula.nacos.username}
        password: ${macula.nacos.password}
###########dubbo配置###############
dubbo:
  application:
    name: ${spring.application.name}
  scan:
    # dubbo 服务扫描基准包
    base-packages: org.macula.base.api
  protocols:
    dubbo:
      # dubbo 协议
      name: dubbo
      # dubbo 协议端口（ -1 表示自增端口，从 20880 开始）
      port: -1
      threads: 500
    rest:
      # http rest 请求 
      name: rest
      port: 9090
      server: netty
  registries:
    macula:
      default: true
      timeout: 60000
      # 挂载到 Spring Cloud 注册中心
      address: nacos://${macula.nacos.registry.url}?namespace=${macula.nacos.namespace}&username=${macula.nacos.username}&password=${macula.nacos.password}
```
* `dubbo.scan.base-packages`：指定 Dubbo 服务实现类的扫描基准包
* `dubbo.protocols`：
    * name: dubbo 为 Dubbo服务暴露的协议配置，其中子属性name为协议名称，port为协议端口（-1 表示自增端口，从 20880 开始）
    * name: rest 为http协议，server：netty 为应用启动容器服务
* `dubbo.registries`：
    * macula: default  true 为 Dubbo 服务默认注册中心配置，其中子属性address 的值 "nacos://${macula.nacos.registry.url}"，说明挂载到 Nacos 注册中心。
* `dubbo.application.name`：dubbo服务名称
*  `spring.cloud.nacos.discovery`：Nacos 服务发现与注册配置，其中子属性 server-addr 指定 Nacos 服务器主机和端口。

创建服务启动类

```java
@DubboComponentScan
@SpringBootApplication
@EnableDiscoveryClient
public class MemberEsbDubboApplication {
  public static void main(String[] args) {
    SpringApplication.run(MemberEsbDubboApplication.class, args);
  }
}
```

4. **子模块 demo-member-admin 服务调用方**

 工程依赖 pom.xml 

```xml
<dependency>
  <groupId>org.macula.base</groupId>
  <artifactId>demo-member-esb-api</artifactId>
  <version>${revision}</version>
</dependency>
```

配置文件 application.yml

```yaml
## 服务发现与注册配置
spring:
  cloud:
    nacos:
      discovery:
        server-addr: ${macula.nacos.url}
        namespace: ${macula.nacos.namespace}
        username: ${macula.nacos.username}
        password: ${macula.nacos.password}
dubbo:
  scan:
      # dubbo 服务扫描基准包
      base-packages: org.macula.base.api
  cloud:
    # The subscribed services in consumer side
    subscribed-services: ${provider.application.name}
  protocols:
    dubbo:
      port: -1
  consumer:
    timeout: 60000
  registries:
    macula:
      default: true
      address: nacos://${macula.nacos.registry.url}?namespace=${macula.nacos.namespace}&username=${macula.nacos.username}&password=${macula.nacos.password}
      timeout: 60000
```

测试接口HelloController.java

```java
@RestController
public class HelloController {

    @DubboReference
    private UserApi userApi;
    
    private static final String BASE_URL = "http://localhost:9090";
    
    // 通过Dubbo协议请求
    @GetMapping("/testDubbo")
    public String testDubbo() {
        return userApi.get("admin");
    }
    
    // 通过Http Rest 请求
    @GetMapping("/testRest")
    private static void testRest() {
    String uri = "/user/get?userName=admin";
    // 发起请求
    OkHttpClient client = new OkHttpClient();
    Request request = new Request.Builder()
        .url(BASE_URL + uri)
        .get()
        .build();
    try (Response response = client.newCall(request).execute()) {
      System.out.println("请求结果: " + response.body().string());
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
```