---
title: "Macula Boot Starter Web"
linkTitle: "WEB"
weight: 1
source_path: "macula-boot-starters/macula-boot-starter-web/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-web/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-starters/macula-boot-starter-web/README.md", "macula-boot-starters/macula-boot-starter-security/README.md"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "5ff9b5c8e6166449ced7512cd3bf74a672aa922e", "paths": ["macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/filter/TenantFilter.java", "macula-boot-commons/src/main/java/dev/macula/boot/context/TenantContextHolder.java", "macula-boot-starters/macula-boot-starter-mybatis-plus/src/main/java/dev/macula/boot/starter/mp/config/MyBatisPlusAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-security/src/main/java/dev/macula/boot/starter/security/utils/SecurityUtils.java"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "6f69e84254b7d1c134d8491c2dbca10dd80de41a", "paths": ["macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/DateTimeConverter.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/config/JacksonConfiguration.java", "macula-boot-starters/macula-boot-starter-web/src/main/java/dev/macula/boot/starter/web/config/MaculaWebMvcConfigurer.java"]}]
---

## 概览

该模块为 Web 开发所需的基本依赖包，是对 `spring-boot-starter-web` 的扩展。Macula Boot 6.1 随 Spring Boot 4 使用其默认的 Tomcat Web 服务器；Spring Boot 4 不再提供 Undertow Starter。有兴趣可以阅读[优雅的写Controller](https://mp.weixin.qq.com/s/i1iCiwhTxQRMqIQj6QzbiQ)。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml

<dependency>
   <groupId>dev.macula.boot</groupId>
   <artifactId>macula-boot-starter-web</artifactId>
</dependency> 
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml

```yaml
macula:
  jackson:
    long-to-string: true
    null-to-empty: false
    # 以下为可选格式示例，不配置时使用组件默认行为
    # local-date-time-format: yyyy-MM-dd HH:mm:ss
    # local-date-format: yyyy-MM-dd
    # local-time-format: HH:mm:ss
  web:
    exception-advice: true  # 统一异常处理器，默认true
    response-advice: true   # 统一响应处理器，默认true
spring:
  jackson:
    date-format: "yyyy-MM-dd'T'HH:mm:ss.SSSXXX" # Date 的示例格式，保留时区偏移
    time-zone: UTC                           # 接口输出时区，不是数据库存储时区
```

### 关键配置

| 属性 | 默认值 | 说明 |
| --- | --- | --- |
| `macula.web.exception-advice` | `true` | 启用统一异常处理 |
| `macula.web.response-advice` | `true` | 启用统一响应包装 |
| `macula.jackson.long-to-string` | `true` | 将 Long、BigInteger、BigDecimal 序列化为字符串 |
| `macula.jackson.null-to-empty` | `false` | 按字段类型将 null 输出为空值 |
| `macula.jackson.local-date-time-format` | 未设置 | 自定义 LocalDateTime 格式 |
| `macula.jackson.local-date-format` | 未设置 | 自定义 LocalDate 格式 |
| `macula.jackson.local-time-format` | 未设置 | 自定义 LocalTime 格式 |

通用 Jackson 开关使用 `spring.jackson.*`。`spring.jackson.date-format` 不能替代 JSR-310 类型的格式配置；上述 LocalDateTime 格式项用于兼容存量字段，不应据此将它选为接口中表示具体时刻的类型。

## 核心功能

### 全局异常处理

如果在Controller每个方法都catch异常，非常不方便，所以默认通过ControllerExceptionAdvice类处理，包括：

- BindException（使用form data方式调用接口，校验异常抛出 BindException）
- ConstraintViolationException（单个参数校验异常抛出ConstraintViolationException）
- MethodArgumentNotValidException (使用 json 请求体调用接口，校验异常抛出 MethodArgumentNotValidException)
- BizException（业务异常，一般业务可以继承这个异常类）
- NullPointerException
- Exception（兜底）

通常返回 HTTP 500；`BizCheckException` 返回 HTTP 510。失败结果的结构如下：

```json
{
  "success": false,
  "code": "10001",
  "msg": "异常说明",
  "cause": "具体的异常信息",
  "data": null
}
```

BizException 异常的 message 通过 `cause` 字段返回，支持国际化 code。其定义如下：

```java
public class BizException extends MaculaException {

   private String code;
   private String msg;

   public BizException(ResultCode resultCode, String exceptionMessage) {
      this(resultCode.getCode(), resultCode.getMsg(), exceptionMessage);
   }

   public BizException(String code, String msg, String exceptionMessage) {
      // message用于用户设置抛出错误详情，例如：当前价格-5，小于0
      super(exceptionMessage);
      this.code = code;
      this.msg = msg;
   }

   public BizException(String exceptionMessage) {
      this(ApiResultCode.BIZ_ERROR, exceptionMessage);
   }

   public String getCode() {
      return this.code;
   }

   public String getMsg() {
      return this.msg;
   }
}
```

> 大家在开发应用时，在service层可以讲底层异常使用BizException封装为业务异常抛出。在Controller层一般情况下无需catch任何异常，交由上述全局异常处理器统一处理。

### 全局返回结构处理

默认情况下所有Controller都按照Result结构体返回，Controller返回值无需自己转换为Result类，保持原始返回类即可。

***如果不需要包装可以添加@NotControllerResponseAdvice注解。***

Result类由macula-boot-commons模块定义。具体如下：

```java

@Data
public class Result<T> implements Serializable {
   private boolean success;
   private String code;
   private String msg;
   private String cause;
   private T data;
}
```

并且为了code属性的规范一致，提供了ResultCode接口

```java
public interface ResultCode {
   /**
    * 返回码
    */
   String getCode();

   /**
    * 返回消息
    */
   String getMsg();
}
```

macula默认提供了ApiResultCode实现，定义了用户类异常、业务类异常以及第三方调用异常。

建一个各项目自行定义自己的ResultCode，code的编码规则建议如下：

- 长度为5位
- 第一位字母，表示一类异常，macula保留A用户类异常、B业务类异常、C第三方调用异常等三个字母。
- 后四位用数字表示，同类型的异常尽量保持前两位一致

#### Controller示例

```java

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/consumer")
public class ConsumerController {

   @Autowired
   private Provider1Service provider1Service;

   @Autowired
   private GapiService gapiService;

   @Autowired
   private IpaasService ipaasService;

   @GetMapping("/echo")
   @NotControllerResponseAdvice
   // 该接口直接返回String
   public String echo() {
      return provider1Service.echo("consumer");
   }

   @PostMapping("/user")
   // 该接口返回的JSON是{sucess:true, code:xxx, msg: xxx, data: {UserResult}}
   public UserResult getUser() {
      return provider1Service.getUser();
   }
}
```

#### 授权列表的资源凭证扩展

响应签发依赖 Commons 的 `PasskeyResource` 与 `PasskeyIssuer` 契约，Web 无需依赖具体 Security 实现。处理规则：

- **支持包装**：Collection、PageVO、成功 Result 中的列表，以及 ResponseEntity 的相应正文。
- **资源元素**：实现接口的元素调用签发器，混合列表中的普通元素保持不变；单对象不自动签发。
- **字段输出**：辅助 resourceId 不输出 JSON，实际业务编号与 passkey 正常输出。不同 DTO 可引用同一全局唯一资源编号。

**返回接口实现元素即表示业务已按当前用户过滤资源访问范围。**

- 不需要签发注解，不能把此类 DTO 用于未经授权的列表。
- 每次响应覆盖旧凭证，不把缓存凭证当作授权依据。
- `macula.security.passkey.enabled=false`（默认）时，跳过遍历与签发，已有自定义签发器也不调用。
- 启用后，存在候选元素却缺少有效签发器时拒绝；默认 Security 服务要求有效签名配置。

签发在包装判定前执行：Result、ResponseEntity、Feign 或 `@NotControllerResponseAdvice` 的包装跳过不能绕过签发，但保持原响应外壳。原两参 Advice 构造入口仍保留，无签发提供者时仍可处理普通响应。关闭 `macula.web.response-advice` 或提供自定义 Advice 后，自动签发需自行接入，资源前置验证不会因此放行。

现有 ControllerExceptionAdvice 将实现公共 `ResourceAccessDenied` 标记的异常映射为 HTTP 403 / A0312，其他异常沿用原处理。完整配置和 Controller 参数验证见 [Security Starter](/docs/latest/01_services/框架基础/security/)。

列表签发后的资源请求，在 MVC Controller 参数上使用 `@Passkey` 验证；操作权限与返回值归属分别使用 `@PreAuthorize`、`@PostAuthorize`。凭证不从 JSON / 表单字段读取，完整示例见 [Security 资源凭证](/docs/latest/01_services/框架基础/security/#passkeycontroller-参数资源凭证)。

<span id="租户id"></span>

### 临时租户参数

Servlet 应用中的 `TenantFilter` 从 `tenantId` 请求头读取临时租户；请求头为空时再读同名请求参数，随后写入 `TenantContextHolder`。它解析的是临时切换值，不是重新登录，不改变 JWT 认证租户，也不校验调用者是否有目标租户权限。

业务开放切换前须校验目标租户权限，禁止切换的接口应拒绝外部覆盖。临时值对数据访问的影响、作用域恢复与默认值选择见 [MyBatisPlus 租户插件](/docs/latest/01_services/框架基础/mybatisplus/#租户插件)。

### 国际化

客户端透过请求头的Accept-Language设定对应的国际化资源，其他参考Spring标准。

### 时间格式

#### 日期传入

http请求传入日期格式的字符串

##### 表单请求

当GET请求或者POST请求的x-www-form-urlencoded时，前端的时间格式都是通过Converter转为日期格式，系统默认已经设置为ISO日期格式。

```java
@Override public void addFormatters(FormatterRegistry registry){
        // 默认String没有办法转为java.util.Date类型
        registry.addConverter(new Converter<String, Date>(){
@Override public Date convert(String source){
        return DateUtil.parse(source.trim()).toJdkDate();
        }
        });

        DateTimeFormatterRegistrar registrar=new DateTimeFormatterRegistrar();
        registrar.setUseIsoFormat(true);
        registrar.registerFormatters(registry);
        }

enum ISO {
   /**
    * The most common ISO Date Format {@code yyyy-MM-dd} &mdash; for example,
    * "2000-10-31".
    */
   DATE,

   /**
    * The most common ISO Time Format {@code HH:mm:ss.SSSXXX} &mdash; for example,
    * "01:30:00.000-05:00".
    */
   TIME,

   /**
    * The most common ISO Date Time Format {@code yyyy-MM-dd'T'HH:mm:ss.SSSXXX}
    * &mdash; for example, "2000-10-31T01:30:00.000-05:00".
    */
   DATE_TIME
}
```

{{% alert title="提示" color="primary" %}}

如果请求的日期字符串对应的类型是java.util.Date类型，我们使用了hutool的DateUtil.parse，他会自适应一些日期格式，具体参考[hutool](https://doc.hutool.cn/pages/DateUtil/#%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E6%97%A5%E6%9C%9F)。

如果请求的日期字符串对应的类型是jsr310的，需要注意按照ISO要求。

如果某些字段或者参数需要个性化设置，可以使用注解@DateTimeFormat

{{% /alert %}}

##### JSON请求

如果是POST请求的application/json时，则由jackson的配置来完成

配置见本页[配置示例](#配置示例)。

{{% alert title="提示" color="primary" %}}

`spring.jackson.date-format` 不控制 LocalDate / LocalDateTime 的格式。纯日期字段可按契约使用属性注解；表示具体时刻的接口字段应选择 Date / Instant，见下文“数据库日期”。

{{% /alert %}}

```java
@JsonFormat(pattern = "yyyy-MM-dd") private LocalDate businessDate;
```

#### 日期返回

##### 普通响应

响应如果是text/html时，由生成html的模板引擎配置

##### JSON响应

响应如果是json格式也是由jackson的配置

#### 数据库日期

**数据库与接口使用两种时间语义：Entity / BO 按存储约定保留无时区日期时间；对外 POJO 用 `Date` 或 `Instant` 表示具体时刻，在转换边界显式关联存储时区。** 不直接把 Entity 的 `LocalDateTime` 字段复制到接口模型中作为发生时刻。

{{< process-diagram name="web-datetime-boundary" title="日期时间双向流转：前端 JSON、接口 Date 或 Instant、Converter、实体 LocalDateTime 与数据库无时区字段" >}}

| 边界 | 推荐类型 / 表达 | 约束 |
| --- | --- | --- |
| 数据库日期时间列 | MySQL `DATETIME(3)` / `DATETIME(6)` 等无时区字段 | 小数秒精度按业务选择；统一约定这些值按哪个存储时区解释 |
| 与数据库交互的 Entity / BO | `LocalDateTime`；纯日期用 `LocalDate`，日内时刻用 `LocalTime` | 不在字段里附加时区；查询范围参数也按同一存储语义转换 |
| 对外 Form / DTO / VO 中的发生、创建、更新时间等 | `Date` 或 `Instant` | 表示确定时刻，不使用 `LocalDateTime` 承担此语义 |
| 前端 JSON 中的具体时刻 | 含 `Z` / 明确偏移量的 ISO 字符串，或契约明确单位的时间戳 | 不传含义不明的裸日期时间字符串；前端展示时再按用户时区格式化 |

`Date` 和 `Instant` 表示时间线上的点，**并不保存用户的时区 ID**；`LocalDateTime` 则没有足够信息独立确定一个时刻。接口若表达生日、账期日期等纯日期，仍可使用 `LocalDate`；这类字段不是发生时刻，不应强行补成零点。

##### 写入与返回的职责

1. **JSON → 接口 POJO：** Web / Jackson 按契约解析时间点。接口 JSON、GET 参数和表单绑定不是同一条解析链，需分别验证。
2. **接口 POJO → Entity / BO：** Converter 按统一存储时区，将时间点转换成 `LocalDateTime`。不是直接去掉偏移量或时区后缀。
3. **Entity / BO → 数据库：** JDBC 按数据库列类型读写无时区值。数据库、连接和驱动设置应与存储约定一致，避免隐式二次换算。
4. **返回响应：** 数据库值经 Entity / BO 取出，由 Converter 按同一存储时区还原 `Date` / `Instant`，再由 Jackson 输出接口 JSON。

以 `Asia/Shanghai` 为存储约定：接口 `2026-11-05T00:50:30Z` 对应实体 `2026-11-05T08:50:30`、数据库 `2026-11-05 08:50:30`。返回时应还原同一个时刻，而不是把 `08:50:30` 直接加 `Z`。

##### 公共转换器与 Instant

最新 [MapStruct Starter](/docs/latest/01_services/框架基础/mapstruct/#使用配置) 提供 `macula.time.storage-zone` 与 `DateTimeConverter`。当前内置的是 `Date ↔ LocalDateTime`，普通 MapStruct 与 Plus 的接入方式不同，详见该组件文档。

接口选择 `Instant` 时，需提供同一存储时区的显式转换。下面是业务转换方法的写法节选，`storageZone` 应与应用的数据库存储约定一致；不是 Starter 已新增的公共 API：

```java
LocalDateTime toStorageTime(Instant value, ZoneId storageZone) {
    return value == null ? null : LocalDateTime.ofInstant(value, storageZone);
}

Instant toApiTime(LocalDateTime value, ZoneId storageZone) {
    return value == null ? null : value.atZone(storageZone).toInstant();
}
```

通过 Mapper 的 `uses` 等方式接入应用自己的适配器，不依赖隐式转换。经 `Date` 中转时只有毫秒精度；直接使用 `Instant` 也仍须遵守数据库列的小数秒精度。

##### 配置和已有数据

- Jackson 的时区 / 格式配置只控制接口解析与输出；MapStruct 的 `storage-zone` 控制对象映射；JDBC / 数据库会话设置属于持久化边界。一个设置不能代替其他边界。
- 未配置 `storage-zone` 时，当前公共转换器使用创建 Bean 时的 JVM 默认时区；多实例环境应显式统一，不能让不同容器按不同默认值解释同一列。
- MySQL `TIMESTAMP` 存在按会话时区转换的语义，不应简单写成“对应 ZonedDateTime”。本指南推荐的无时区存储采用 `DATETIME`；已有 `TIMESTAMP` 字段须按实际驱动和数据库行为评估迁移。
- MySQL `TIME` 还可表达超过一天的时长，只有“日内时刻”语义才适合直接对应 `LocalTime`。
- 改时区配置不会重写历史值。先核对已有数据的存储约定，再决定配置和迁移，不能只改 JVM 或 JSON 格式后认定问题解决。

验收应覆盖：JSON 输入 → 对象转换 → 实际数据库写入 → 重新读取 → JSON 返回，检查时间点和精度是否一致；至少比较不同 JVM 默认时区的实例，避免只测试格式字符串看起来相同。

类型语义见 [LocalDateTime](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/LocalDateTime.html)、[Instant](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Instant.html)；数据库行为见 [MySQL 日期时间类型](https://dev.mysql.com/doc/refman/8.4/en/datetime.html)。

### Validator校验

默认引入了spring-boot-starter-validation，可以在这里继续扩展自定义的validator，比如身份证、电话、邮件等等。

```java
public class UserVO {
   @NotNull(message = "age 不能为空")
   private Integer age;
}
```

然后在`controller`方法中添加`@Validated`：

```java
// 注意这里的BindingResult参数可以不添加，如果不添加则validator有问题会抛出异常，由全局异常拦截器统一处理
public String add1(@Validated UserVO userVO,BindingResult result){
        List<FieldError> fieldErrors=result.getFieldErrors();
        if(!fieldErrors.isEmpty()){
        return fieldErrors.get(0).getDefaultMessage();
        }
        return"OK";
        }
```

内置的校验注解有很多，罗列如下：

| 注解               | 校验功能                |
|------------------|---------------------|
| @AssertFalse     | 必须是false            |
| @AssertTrue      | 必须是true             |
| @DecimalMax      | 小于等于给定的值            |
| @DecimalMin      | 大于等于给定的值            |
| @Digits          | 可设定最大整数位数和最大小数位数    |
| @Email           | 校验是否符合Email格式       |
| @Future          | 必须是将来的时间            |
| @FutureOrPresent | 当前或将来时间             |
| @Max             | 最大值                 |
| @Min             | 最小值                 |
| @Negative        | 负数（不包括0）            |
| @NegativeOrZero  | 负数或0                |
| @NotBlank        | 不为null并且包含至少一个非空白字符 |
| @NotEmpty        | 不为null并且不为空         |
| @NotNull         | 不为null              |
| @Null            | 为null               |
| @Past            | 必须是过去的时间            |
| @PastOrPresent   | 必须是过去的时间，包含现在       |
| @Pattern         | 必须满足正则表达式           |
| @PositiveOrZero  | 正数或0                |
| @Size            | 校验容器的元素个数           |

#### 分组校验

如果同一个参数，需要在不同场景下应用不同的校验规则，就需要用到分组校验了。比如：新注册用户还没起名字，我们允许`name`
字段为空，但是不允许将名字更新为空字符。

分组校验有三个步骤：

1. 定义一个分组类（或接口）
2. 在校验注解上添加`groups`属性指定分组
3. `Controller`方法的`@Validated`注解添加分组类

```java
public interface Update extends Default{
}
public class UserVO {
    @NotBlank(message = "name 不能为空",groups = Update.class)
    private String name;
    // 省略其他代码...
}
@PostMapping("update")
public ResultInfo update(@Validated({Update.class}) UserVO userVO) {
    return new ResultInfo().success(userVO);
}
```

细心的同学可能已经注意到，自定义的`Update`分组接口继承了`Default`接口。校验注解(如：` @NotBlank`)和`@validated`
默认都属于`Default.class`分组，这一点在`jakarta.validation.groups.Default`注释中有说明

```java
/**
 * Default Jakarta Bean Validation group.
 * <p>
 * Unless a list of groups is explicitly defined:
 * <ul>
 *     <li>constraints belong to the {@code Default} group</li>
 *     <li>validation applies to the {@code Default} group</li>
 * </ul>
 * Most structural constraints should belong to the default group.
 *
 * @author Emmanuel Bernard
 */
public interface Default {
}
```

在编写`Update`分组接口时，如果继承了`Default`，下面两个写法就是等效的：

```
@Validated({Update.class})
@Validated({Update.class,Default.class})
```

请求一下`/update`接口可以看到，不仅校验了`name`字段，也校验了其他默认属于`Default.class`分组的字段

```json
{
    "status": 400,
    "message": "客户端请求参数错误",
    "response": [
        "name 不能为空",
        "age 不能为空",
        "email 不能为空"
    ]
}
```

如果`Update`不继承`Default`，`@Validated({Update.class})`就只会校验属于`Update.class`分组的参数字段，修改后再次请求该接口得到如下结果，可以看到，
其他字段没有参与校验：

```json
{
    "status": 400,
    "message": "客户端请求参数错误",
    "response": [
        "name 不能为空"
    ]
}
```

#### 递归校验

如果 UserVO 类中增加一个 OrderVO 类的属性，而 OrderVO 中的属性也需要校验，就用到递归校验了，只要在相应属性上增加`@Valid`
注解即可实现（对于集合同样适用）

OrderVO类如下

```java
public class OrderVO {
   @NotNull
   private Long id;
   @NotBlank(message = "itemName 不能为空")
   private String itemName;
   // 省略其他代码...
}
```

在 UserVO 类中增加一个 OrderVO 类型的属性

```java
public class UserVO {
   @NotBlank(message = "name 不能为空", groups = Update.class)
   private String name;
   //需要递归校验的OrderVO
   @Valid
   private OrderVO orderVO;
   // 省略其他代码...
}   
```

#### 自定义校验

Spring 的 validation 为我们提供了这么多特性，几乎可以满足日常开发中绝大多数参数校验场景了。但是，一个好的框架一定是方便扩展的。有了扩展能力，就能应对更多复杂的业务场景，毕竟在开发过程中，
**唯一不变的就是变化本身**。

Spring Validation允许用户自定义校验，实现很简单，分两步：

1. 自定义校验注解
2. 编写校验者类

代码也很简单，结合注释你一看就能懂

```java
@Target({METHOD, FIELD, ANNOTATION_TYPE, CONSTRUCTOR, PARAMETER})
@Retention(RUNTIME)
@Documented
@Constraint(validatedBy = {HaveNoBlankValidator.class})// 标明由哪个类执行校验逻辑
public @interface HaveNoBlank {
    
    // 校验出错时默认返回的消息
    String message() default "字符串中不能含有空格";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };

    /**
     * 同一个元素上指定多个该注解时使用
     */
    @Target({ METHOD, FIELD, ANNOTATION_TYPE, CONSTRUCTOR, PARAMETER, TYPE_USE })
    @Retention(RUNTIME)
    @Documented
    public @interface List {
        NotBlank[] value();
    }
}
public class HaveNoBlankValidator implements ConstraintValidator<HaveNoBlank, String> {
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // null 不做检验
        if (value == null) {
            return true;
        }
        if (value.contains(" ")) {
            // 校验失败
            return false;
        }
        // 校验成功
        return true;
    }
}
```

自定义校验注解使用起来和内置注解无异，在需要的字段上添加相应注解即可，同学们可以自行验证

### 字段脱敏

通过使用@Sensitive注解可以令某个字段属性在序列化为JSON时按照一定的规则脱敏，并且预置了如下规则：

* MOBILE：手机号，如：138****2359
* CHINESE_NAME：中文名 ，如：黄**
* ID_CARD：身份证号，如：511623********0537
* FIXED_PHONE：座机号，如：****1234
* ADDRESS：地址，如：广东省广州市天河区****
* EMAIL：电子邮件，如：g**@163.com
* BANK_CARD：银行卡，如：622848*********5579
* CUSTOM_HIDE：自定义，有多少个字符替换成多少个*
* CUSTOM_RETAIN_HIDE：保留方式隐藏
* CUSTOM_OVERLAY：自定义,只替换成指定个*
  例如：

```java
@Data
public class DemoDto {

   @NotEmpty
   private String password;

   @Length(min = 5, max = 25, message = "{key.length}")
   private String key;

   @Pattern(regexp = "[012]", message = "无效的状态标志")
   private String state;

   @Sensitive(value = Sensitive.Type.MOBILE)
   private String mobile;

}
```

@Sensitive注解定义：

```java
/**
 * {@code Sensitvie} 脱敏的JSON注解
 *
 * @author rain
 * @since 2022/7/28 23:48
 */
@Target({ElementType.FIELD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@JacksonAnnotationsInside
@JsonSerialize(using = SensitiveSerializer.class)
public @interface Sensitive {

   /**
    * 脱敏的类型,默认手机号
    *
    * @return 返回脱敏类型
    */
   Type value();

   /**
    * CUSTOM_HIDE/CUSTOM_OVERLAY 时生效
    *
    * @return 开始位置（包含）
    */
   int startInclude() default 0;

   /**
    * CUSTOM_HIDE/CUSTOM_OVERLAY 时生效
    *
    * @return 结束位置（不包含）
    */
   int endExclude() default 0;

   /**
    * CUSTOM_OVERLAY 时生效
    *
    * @return *重复的次数
    */
   int overlayRepeat() default 4;

		...
}
```

### Jackson配置

默认对Jackson做了如下配置

```java
@Bean
@ConditionalOnMissingBean
public JsonMapperBuilderCustomizer customizer() {
    return builder -> {
        builder.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
        builder.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        SimpleModule module = new SimpleModule("customJacksonModule");
        module.addSerializer(Long.class, ToStringSerializer.instance);
        builder.addModule(module);
    };
}
```

Macula Boot 6.1 使用 Jackson 3：`JsonMapperBuilderCustomizer` 位于
`org.springframework.boot.jackson.autoconfigure`，Jackson 数据绑定类型位于 `tools.jackson.databind`。
Boot 3 的 `Jackson2ObjectMapperBuilderCustomizer` 与 `com.fasterxml.jackson.databind` 扩展不能直接用于该配置链。

### 升级与消息转换器兼容

JSON 转换器显式设置默认字符集为 UTF-8，自动生成的 JSON 响应头包含 `charset=UTF-8`；SSE 专用 PrettyPrinter 在构造时初始化并复用。

Jackson 3 请求反序列化保留基本类型字段接收 `null` 的历史行为，例如 `int` 转为 `0`、`boolean` 转为 `false`。开启 JSON 缩进时，SSE 响应的后续行仍使用 `data:` 前缀。

消息转换器通过 Spring 7 的 `configureMessageConverters(HttpMessageConverters.ServerBuilder builder)` 配置：字符串使用 UTF-8，JSON 使用 `MappingApiJacksonHttpMessageConverter`。通过 `withStringConverter` / `withJsonConverter` 替换对应默认转换器，其他格式保留框架默认注册行为。

升级自定义扩展时，将 `AbstractReadWriteJackson2HttpMessageConverter`、`MappingApiJackson2HttpMessageConverter` 分别替换为去掉名称中 `2` 的新类。Jackson API 使用 `tools.jackson.*`；共享注解仍使用 `com.fasterxml.jackson.annotation.*`。

## 依赖引入

```xml

<dependencies>
   <dependency>
      <groupId>dev.macula.boot</groupId>
      <artifactId>macula-boot-commons</artifactId>
   </dependency>
   <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
   </dependency>
   <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-validation</artifactId>
   </dependency>
</dependencies>
```

## 版权说明

- Spring：https://github.com/spring-projects/spring-boot/blob/main/LICENSE.txt
