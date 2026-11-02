---
title: "Macula Boot Starter Auditing"
linkTitle: "Auditing"
weight: 4

source_path: "macula-boot-starters/macula-boot-starter-auditlog/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-auditlog/README.md", "macula-boot-starters/macula-boot-starter-operationlog/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

本模块通过 `@AuditLog` 采集审计事件，由应用监听 `OperLogEvent` 完成持久化。日志导出可结合 `macula-boot-starter-observability`，本模块不提供日志存储后端。


操作日志功能模块，提供基于注解的操作日志记录功能。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<!-- 日志审计 -->
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-auditlog</artifactId>
</dependency>
```

## 使用配置

无独立 YAML 配置项；记录范围由下文 `@AuditLog` 参数控制。默认保存请求和响应数据，敏感字段应通过 `excludeParamNames` 排除，或关闭对应记录。异步监听示例需启用 `@EnableAsync` 或引入 Async Starter。

### AuditLog

添加macula-boot-starter-auditlog依赖后，在需要审计的方法上加上@AuditLog注解，添加注解后调用方法会触发OperLogEvent事件，可以定义Listener监听事件用于持久化审计日志。

```java
  @Operation(summary = "新增菜单")
  @AuditLog(title = "新增菜单")
  @PostMapping
  @CacheEvict(cacheNames = "system", key = "'routes'")
  public boolean addMenu(@RequestBody SysMenu menu) {
      boolean result = menuService.saveMenu(menu);
      return result;
  }
```

@AuditLog注解定义如下：

```java
@Target({ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface AuditLog {
    /**
     * 模块
     */
    String title() default "";

    /**
     * 功能
     */
    BusinessType businessType() default BusinessType.OTHER;

    /**
     * 操作人类别
     */
    OperatorType operatorType() default OperatorType.MANAGE;

    /**
     * 是否保存请求的参数
     */
    boolean isSaveRequestData() default true;

    /**
     * 是否保存响应的参数
     */
    boolean isSaveResponseData() default true;

    /**
     * 排除指定的请求参数
     */
    String[] excludeParamNames() default {};

}
```

Listenter定义参考：

```java
@Component
@RequiredArgsConstructor
public class AuditLogEventListener {

    private final SysLogService sysLogService;

    /**
     * 保存系统日志记录
     */
    @Async
    @EventListener
    public void saveLog(OperLogEvent operLogEvent) {
        SysLog log = new SysLog();
        log.setOpIp(operLogEvent.getOperIp());
        log.setErrorMsg(operLogEvent.getErrorMsg());
        log.setJsonResult(operLogEvent.getJsonResult());
        log.setOpName(operLogEvent.getOperName());
        log.setOpParam(operLogEvent.getOperParam());
        log.setOpMethod(operLogEvent.getMethod());
        log.setOpStatus(operLogEvent.getStatus());
        log.setOpUrl(operLogEvent.getOperUrl());
        log.setOpRequestMethod(operLogEvent.getRequestMethod());
        log.setOpTitle(operLogEvent.getTitle());
        log.setCreateBy(operLogEvent.getOperName());
        if (operLogEvent.getOperTime() != null) {
            log.setCreateTime(LocalDateTime.ofInstant(operLogEvent.getOperTime().toInstant(), ZoneId.systemDefault()));
        } else {
            log.setCreateTime(LocalDateTime.now());
        }
        sysLogService.save(log);
    }
}
```

## 核心功能

- **注解驱动**：通过 `@OperationLog` 注解标记需要记录日志的方法
- **分层记录**：支持 Controller、Service、Domain、Repository 等不同层级
- **参数记录**：可选择是否记录方法入参和出参
- **执行时间统计**：自动计算方法执行耗时
- **异常处理**：自动捕获和记录异常信息
- **HTTP 请求信息**：在 Controller 层自动记录请求 IP、URI、HTTP 方法等
- **事件驱动**：基于 Spring Event 机制，支持异步处理
- **自动配置**：基于 Spring Boot AutoConfiguration，开箱即用

### 与 AuditLog 的区别

- **OperationLog**：专注于操作过程记录，追踪业务方法的调用过程和执行结果
- **AuditLog**：专注于审计日志，记录关键业务操作的安全和合规信息

### 使用方法

#### 1. 添加依赖

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-operationlog</artifactId>
</dependency>
```

#### 2. 使用注解

仅在 Web 应用中自动配置，无独立 YAML 开关；记录内容由注解参数控制。`spring.application.name` 用作应用名，未设置时为 `unknown-app`。避免两个日志注解重复记录同一方法，并对参数和结果中的敏感信息脱敏。

##### Controller 层使用示例

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @OperationLog(
        module = "用户管理",
        description = "创建用户",
        operation = "ADD",     // 自定义类型
        layer = "CONTROLLER",       // 自定义层级
        logParameters = true,
        logResult = false
    )

    // 查询方法见下方常量写法；同一方法只添加一个 @OperationLog
    @PostMapping
    public Result<UserVO> createUser(@RequestBody UserCreateDTO dto) {
        // 业务逻辑
        return Result.success(userVO);
    }

    @OperationLog(
        module = "用户管理",
        description = "查询用户详情",
        operation = OperationLogConstant.OPERATION_TYPE_SELECT,
        layer = OperationLogConstant.LAYER_CONTROLLER
    )
    @GetMapping("/{id}")
    public Result<UserVO> getUser(@PathVariable Long id) {
        // 业务逻辑
        return Result.success(userVO);
    }
}
```

##### Service 层使用示例

```java
@Service
public class UserService {

    @OperationLog(
        module = "用户服务",
        description = "删除用户",
        operation = OperationLogConstant.OPERATION_TYPE_DELETE,
        layer = OperationLogConstant.LAYER_SERVICE
    )
    public void deleteUser(Long userId) {
        // 业务逻辑
    }

    @OperationLog(
        module = "用户服务",
        description = "更新用户信息",
        operation = OperationLogConstant.OPERATION_TYPE_UPDATE,
        layer = OperationLogConstant.LAYER_SERVICE,
        logParameters = true,
        logResult = true
    )
    public UserVO updateUser(UserUpdateDTO dto) {
        // 业务逻辑
        return userVO;
    }
}
```

##### Domain 层使用示例

```java
@Component
public class UserDomainService {

    @OperationLog(
        module = "用户领域服务",
        description = "用户状态变更",
        operation = OperationLogConstant.OPERATION_TYPE_UPDATE,
        layer = OperationLogConstant.LAYER_DOMAIN
    )
    public void changeUserStatus(Long userId, UserStatus status) {
        // 业务逻辑
    }
}
```

##### 自定义操作类型

```java
@OperationLog(
    module = "认证服务",
    description = "用户登录",
    operation = "LOGIN",            // 自定义类型
    layer = "CONTROLLER"             // 自定义层级
)
```

### 注解参数说明

`@OperationLog` 注解支持以下参数：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `module` | String | - | **必填**，模块名称 |
| `description` | String | - | **必填**，操作描述 |
| `operation` | String | "SELECT" | 操作类型：支持自定义字符串或使用常量 |
| `layer` | String | "CONTROLLER" | 业务层级：支持自定义字符串或使用常量 |
| `logParameters` | boolean | true | 是否记录方法入参 |
| `logResult` | boolean | false | 是否记录方法返回值 |

### 常量使用

#### 操作类型常量

- `OperationLogConstant.OPERATION_TYPE_ADD` - 增加
- `OperationLogConstant.OPERATION_TYPE_DELETE` - 删除
- `OperationLogConstant.OPERATION_TYPE_UPDATE` - 更新
- `OperationLogConstant.OPERATION_TYPE_SAVE_OR_UPDATE` - 新增或者修改
- `OperationLogConstant.OPERATION_TYPE_SELECT` - 查询

#### 业务层级常量

- `OperationLogConstant.LAYER_CONTROLLER` - 控制器层
- `OperationLogConstant.LAYER_SERVICE` - 业务层
- `OperationLogConstant.LAYER_DOMAIN` - 领域层
- `OperationLogConstant.LAYER_REPOSITORY` - 仓储层级

#### 使用方式

```java
// 方式一：直接写字符串（推荐，最灵活）
@OperationLog(
    operationType = "LOGIN",     // 自定义类型
    layer = "CONTROLLER"         // 自定义层级
)

// 方式二：使用常量类
@OperationLog(
    operationType = OperationLogConstant.OPERATION_TYPE_ADD,
    layer = OperationLogConstant.LAYER_CONTROLLER
)
```

### 日志输出

日志会通过 SLF4J 输出，格式如下：

```
[OperationLog] UserController.createUser ->
{
  "serviceId": "your-app-name",
  "logType": {"type":1,"description":"正常日志"},
  "operation": "ADD",
  "layer": "CONTROLLER",
  "module": "用户管理",
  "description": "创建用户",
  "clientIp": "127.0.0.1",
  "requestMode": "POST",
  "requestUri": "/api/users",
  "method": "UserController.createUser",
  "param": {"dto": {...}},
  "result": {...},
  "startTime": "2023-12-01T10:30:00",
  "endTime": "2023-12-01T10:30:05",
  "costTime": 5000,
  "traceId": "...",
  "requestId": "..."
}
```

### 自定义扩展

#### 自定义日志监听器

如果需要将日志写入数据库或其他存储，可以实现自定义监听器：

```java
@Component
public class CustomOperationLogListener {

    @EventListener(OperationLogEvent.class)
    @Async
    public void handleOperationLog(OperationLogEvent event) {
        OperationLogDTO logDTO = event.getOperationLog();
        // 将日志写入数据库或其他存储
        operationLogService.save(logDTO);
    }
}
```

#### 禁用自动配置

如果不需要自动配置，可以通过以下方式禁用：

```yaml
spring:
  autoconfigure:
    exclude:
      - dev.macula.boot.starter.operationlog.config.OperationLogAutoConfiguration
```

### 最佳实践

#### 1. 合理使用分层

- **Controller 层**：适合记录外部接口调用，包含完整的 HTTP 请求信息
- **Service 层**：适合记录业务逻辑操作，重点关注业务参数和结果
- **Domain 层**：适合记录领域核心操作，关注业务规则执行
- **Repository 层**：一般不建议使用，避免日志过于冗余

#### 2. 参数控制

- 生产环境中建议关闭 `isShowResult`，避免敏感信息泄露
- 对于大数据量的操作，建议关闭 `isShowParam`，避免日志过大
- 异常情况下会自动记录异常信息，无需额外处理

#### 3. 模块划分

建议按照业务模块来划分 `moduleName`：
- 用户管理、订单管理、商品管理等业务模块
- 支付服务、消息服务等基础服务模块

### 注意事项

1. 该 Starter 仅在 Web 应用环境中生效
2. 日志监听器默认使用异步处理，避免影响主业务流程
3. 在 Controller 层会自动记录 HTTP 请求相关信息
4. 异常情况下会自动记录异常信息并设置日志类型为 ERROR
5. 与 `auditlog` 模块配合使用可以实现完整的日志体系

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-security</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

## 版权说明

上述部分代码来源于[RuoYi](https://plus-doc.dromara.org)
并适当修改。基于MIT协议：https://gitee.com/dromara/RuoYi-Cloud-Plus/blob/master/LICENSE
