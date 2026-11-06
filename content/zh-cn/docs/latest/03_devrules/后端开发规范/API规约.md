---
title: "API规约"
linkTitle: "API规约"
weight: 2
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "cd6e30827c78d267cca2f4e0d7b3a6e3dcb01617", "paths": ["content/zh-cn/docs/latest/03_devrules/后端开发规范/阿里规范/Java开发手册(黄山版).pdf", "content/zh-cn/docs/latest/03_devrules/后端开发规范/API规约.md"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-starters/macula-boot-starter-web/README.md", "macula-boot-commons/README.md"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "6f69e84254b7d1c134d8491c2dbca10dd80de41a", "paths": ["macula-boot-starters/macula-boot-starter-mapstruct/README.md", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/DateTimeConverter.java"]}]
---

本章约束新建和演进中的 HTTP API。REST 设计原则用于提高接口一致性，既有契约兼容性优先；例如 Samples 的 `/api/v1/app` 不因复数命名建议而强制改名。调用流程见开发指引，本章侧重接口必须满足的约束。

## 时间字段

对外 POJO 中表示具体时刻的字段使用 `Date` 或 `Instant`，JSON 使用带 `Z` / 偏移量的明确表达，或约定好单位的时间戳。不要用 `LocalDateTime` 传递创建、发生、更新时间等时间点；纯日期可按业务使用 `LocalDate`。与 Entity / BO 的转换遵循 [Web 日期时间边界](/docs/latest/01_services/框架基础/web/#各层类型与转换原理)，格式化不等于时区转换。

## 路径与方法

新接口建议使用小写、连字符和稳定的业务资源名，资源集合优先用复数；避免尾部斜杠和无必要的文件扩展名。业务动作不适合表达为普通字段更新时，可以设计明确的资源动作，但不得用 GET 触发状态变更。

| 方法 | 典型用途 | 设计要求 |
| --- | --- | --- |
| GET | 查询列表或详情 | 无业务写入副作用，限制结果规模 |
| POST | 创建资源或执行业务动作 | 明确重复提交、并发与幂等处理 |
| PUT | 按约定替换资源 | 明确完整字段范围，设计幂等语义 |
| PATCH | 部分修改 | 区分未提供字段、显式空值和实际修改 |
| DELETE | 删除或使资源失效 | 明确不存在、重复删除及关联数据的处理 |

```text
GET    /api/v1/orders
GET    /api/v1/orders/{orderId}
POST   /api/v1/orders
PATCH  /api/v1/orders/{orderId}
POST   /api/v1/orders/{orderId}/cancellation
```

上例是通用设计示意。前端代理路径、网关入口前缀和服务内部路径需分别记录，不能把去除前缀前后的 URL 混为同一个地址；实际 Samples 路由见[示例模块说明](/docs/latest/04_devmanual/模块说明/)。

## 请求与模型

必须通过 Query/Form 等专用模型声明输入，使用 Bean Validation 做结构与字段校验，嵌套对象按需启用递归校验。业务状态、资源归属和跨字段规则由业务层验证；“字段合法”不等于“有权操作”。

| 场景 | 约束 |
| --- | --- |
| 分页 | 定义页码、页大小与上限；超限拒绝或按公开约定处理 |
| 排序 | 客户端只能选择服务端允许的字段及方向，不能提交任意 SQL |
| 模糊与批量查询 | 限制关键字长度、ID 数量与时间范围；大导出采用独立流程 |
| 时间与金额 | 明确格式、时区、精度、单位和舍入方式 |
| 更新 | 采用允许字段映射，不将 Form 整体覆盖持久化实体 |
| 身份与租户 | 来自已验证身份与服务端授权，不能信任请求中的同名字段 |

不要在 URL 查询串中放置长期凭据。上传、下载和流式响应有独立的媒体类型与资源限制，不机械套用普通 JSON 接口。

## 响应与错误

在 Web Starter 管理的普通业务接口中，Controller 优先返回业务对象，由响应 Advice 按规则封装 `Result`；确需自行返回 Result 时核对已有处理逻辑，避免双重包装。下载、SSE、原始字节等响应按实际契约处理。

成功与失败都需要稳定的响应约定。参数错误、未认证、无权限、资源不存在、并发冲突、限流和服务故障应可区分，不能统一包装为无法判断的 HTTP 200“成功”。旧接口已有业务码与 HTTP 状态约定时，先验证客户端兼容，再逐步治理。

错误码表达可程序判断的原因，错误消息面向使用者；响应不暴露数据库 SQL、内部堆栈、密钥或系统路径。统一返回结构、异常处理和 Jackson 行为见 [Web](/docs/latest/01_services/框架基础/web/) 与 [Commons](/docs/latest/01_services/框架基础/commons/)。

## 权限与幂等

必须在服务端检查操作权限及数据边界。Gateway 的入口规则、BFF/Service 的方法授权和业务查询的数据范围分别生效；菜单或按钮可见性不能作为接口授权证据。

创建、支付、扣减等写操作需定义业务幂等键，使用唯一约束、状态机或原子条件更新保护最终状态。接口防重注解可辅助减少重复请求，但不能替代数据库一致性。并发更新使用版本或业务条件并核对受影响行数，不能只执行更新而忽略结果。

## 契约与版本

同一主版本内优先兼容演进。新增可选字段通常比删除字段、改变类型或枚举语义更易兼容；枚举增加值仍需评估旧客户端的兜底逻辑。破坏性修改应提供并行版本、迁移期和明确下线计划。

跨服务共享 `*-api` 中的接口及必要模型，不传递 Entity、Mapper 或 Service 实现。修改契约时验证调用方、服务端、序列化和滚动发布期间的新旧组合；API 制品版本与 HTTP 路径版本分别管理。

## 文档与验收

OpenAPI 文档应描述用途、鉴权、输入约束、分页排序、响应模型、错误码及幂等行为，并提供脱敏示例。不能只给方法添加一个标题就视为文档完整。

上线前验证成功、空结果、参数越界、无身份、权限不足、资源归属不匹配、重复提交和并发冲突。接口路径或字段改变时同步更新 API 契约、调用方和测试，详细安全机制见[请求链路](/docs/latest/00_introduce/请求链路/)。
