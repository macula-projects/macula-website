---
title: "应用架构"
linkTitle: "应用架构"
weight: 3
manual_content: true
source_repository: "https://github.com/macula-projects/macula-website"
source_branch: "master"
source_commit: "cab2f7a737e354a8ba4fd066e7d07ae02fe106d8"
source_paths: ["content/zh-cn/docs/5.x/03_devrules/后端开发规范/应用分层.md", "content/zh-cn/docs/latest/03_devrules/后端开发规范/应用分层.md", "content/zh-cn/docs/latest/03_devrules/后端开发规范/images/layer-model.png", "content/zh-cn/docs/latest/03_devrules/后端开发规范/images/model2.png", "content/zh-cn/docs/latest/01_services/框架基础/Mapstruct.md"]
source_refs: [{"repository": "https://github.com/macula-projects/macula-website", "branch": "master", "commit": "cab2f7a737e354a8ba4fd066e7d07ae02fe106d8", "paths": ["content/zh-cn/docs/5.x/03_devrules/后端开发规范/应用分层.md", "content/zh-cn/docs/latest/03_devrules/后端开发规范/应用分层.md", "content/zh-cn/docs/latest/03_devrules/后端开发规范/images/layer-model.png", "content/zh-cn/docs/latest/03_devrules/后端开发规范/images/model2.png", "content/zh-cn/docs/latest/01_services/框架基础/Mapstruct.md"]}, {"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["macula-samples-api/macula-samples-service1-api/src/main/java/dev/macula/samples/service1/api/ApplicationFeignClient.java", "macula-samples-service1/src/main/java/dev/macula/samples/service1/converter/ApplicationConverter.java", "macula-samples-service1/src/main/java/dev/macula/samples/service1/service/impl/ApplicationServiceImpl.java"]}, {"repository": "https://github.com/macula-projects/macula-boot", "branch": "main", "commit": "a0178da198a79cbbf66f7b9354d2c8711703e81e", "paths": ["macula-boot-archetype/README.md", "macula-boot-archetype/src/main/resources/archetype-resources/pom.xml", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-api/pom.xml", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-service1/src/main/java/service1/controller/ApplicationController.java", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-service1/src/main/java/service1/service/impl/ApplicationServiceImpl.java", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-service1/src/main/java/service1/converter/ApplicationConverter.java", "macula-boot-archetype/src/main/resources/archetype-resources/__rootArtifactId__-service1/src/main/java/service1/mapper/ApplicationMapper.java"]}]
aliases: ["/docs/latest/00_introduce/值对象与分层/"]
---

Macula 建议参考 Archetype，以单仓多模块组织应用：在项目层面区分入口、页面聚合、业务服务与 API 契约，在每个运行模块内部再按 Controller、Service、Mapper、Converter 分工。先明确模块边界，再决定服务内部如何分层，避免把 Maven 模块与 Java 代码层次混为一谈。

## 项目结构

以下以 `demo-app` 为项目名，展示 Archetype 的建议目录；实际业务可将示例 `service1` 替换为领域名称，并按需裁剪模块。

```text
demo-app/
├── pom.xml                         # 后端 Maven 模块聚合
├── demo-app-parent/                # 公共依赖、插件与构建约定
├── demo-app-api/                    # 服务间接口与模型的聚合
│   ├── demo-app-basic-api/          # Basic 的公共契约
│   └── demo-app-service1-api/       # 业务服务的公共契约
├── demo-app-gateway/                # 业务流量入口
├── demo-app-admin-bff/              # 面向管理页面的接口聚合
├── demo-app-service1/               # 领域业务、事务与数据访问
├── demo-app-basic/                  # 按需使用的公共业务服务
├── demo-app-openapi/                # 面向外部调用的接口边界
├── demo-app-thirdparty/             # 第三方协议与模型适配
├── demo-app-admin/                  # 前端工程，独立管理前端依赖
└── deploy/                         # 部署配置与脚本
```

| 模块 | 主要职责 | 边界 |
| --- | --- | --- |
| Parent | 统一依赖版本、插件与构建约定 | 构建模块，不单独运行 |
| API | 发布 Feign 接口、Query / Form / VO 等必要契约 | 不包含持久化实现，不启动服务 |
| Gateway | 路由、入口认证授权、内部 JWT 与接口保护 | 核心业务事务由业务服务负责 |
| Admin BFF | 页面接口聚合，接入 Cloud 用户、菜单与操作权限 | 面向页面组织结果，不维护全部领域逻辑 |
| Service | 领域规则、事务、数据持久化与业务接口 | 维护自己的数据和公开契约 |
| Basic | 可跨业务复用的公共业务能力 | 技术通用能力优先复用 Boot Starter |
| OpenAPI | 面向外部系统组织接口和版本边界 | 与内部业务模型通过契约衔接 |
| Thirdparty | 封装外部 SDK、协议、模型及错误 | 将第三方变化限制在适配边界 |
| Admin / deploy | 页面交互与运行交付配套 | 前端不属于后端 Maven 运行模块 |

Root POM 负责聚合后端模块，Parent 负责公共构建约定；API 是契约制品，Gateway、BFF 与业务服务才是相应的运行边界。前端与 `deploy` 同仓维护，使用各自的构建和部署工具。

**模块按业务需要选用。** 并非每个项目都需要独立的 Basic、OpenAPI、Thirdparty，也不应为了沿用模板而拆出不必要的微服务。Macula Cloud 是独立的公共平台，业务工程通过接口与凭据接入，不将 Cloud 的 IAM、System 实现复制到自己的项目中。

创建与生成步骤见[创建示例平台](/docs/latest/04_devmanual/创建应用平台/)，实际模块配置见[示例模块说明](/docs/latest/04_devmanual/模块说明/)。

## 模块分层

模块边界确定后，再组织模块内部代码。以 Archetype 的业务服务为例，Controller 接收请求，Service 处理业务与事务，Mapper 访问数据，Converter 转换模型；对外共享的表单、查询与返回模型放入该服务的 API 契约模块。

```text
demo-app-service1/
└── src/main/
    ├── java/<基础包>/service1/
    │   ├── controller/              # 请求入口
    │   ├── service/impl/            # 业务接口与实现
    │   ├── mapper/                  # 数据访问
    │   ├── converter/               # 对象转换
    │   └── pojo/
    │       ├── entity/              # 持久化实体
    │       └── bo/                  # 内部业务组合对象
    └── resources/
        ├── mapper/                  # SQL 映射
        └── db/migration/            # 数据库迁移
```

BFF 同样按业务组织接口和服务，但其 Service 以调用和聚合为主，不要求每个模块都具备完整的持久化层。下文结合原有泳道图说明服务内与跨服务的对象传递；这里的 VO 指 **View Object（展示对象）**。

### 各层职责

| 层次 | 负责什么 | 边界 |
| --- | --- | --- |
| Controller | 接收请求、校验输入、调用业务方法并返回结果 | 数据访问通过 Service 组织 |
| Service | 业务规则、授权、事务和操作编排 | 跨服务调用依照对方公开契约 |
| Mapper | 数据查询与持久化 | 按业务要求落实租户和数据范围 |
| Converter | 不同模型的字段映射与结构转换 | 业务规则、授权与事务由业务层处理 |

BFF 面向页面聚合接口，业务服务维护核心业务与持久化；上述职责在各自服务内落实。项目可按复杂度选择基础三层或进一步细分，避免为简单逻辑制造无必要的层次。

下文直接展示服务内泳道图与跨服务原图，结合各层职责解释对象传递；点击图片可放大查看。

### 服务内：对象如何传递

{{< layer-diagram name="layer-model" title="服务内对象传递" original="/docs/latest/03_devrules/后端开发规范/images/layer-model.png" >}}

*泳道从左到右对应 View、Controller、Service、Mapper、DB；橙色为查询链路，绿色为写入链路。*

- **查询入参**：`Query → Controller → Service → Mapper`。同一语义的查询条件可以透传，各层按职责校验、补充查询范围。
- **查询返回**：`DB → Mapper → Entity/BO → Service 转换为 VO → Controller → 调用方`。单表结果通常映射为 Entity，联表或组合结果可映射为 BO。
- **写入入参**：`Form/DTO → Controller → Service → Entity/BO → Mapper → DB`。Controller 校验输入，Service 处理业务规则、授权和事务，并调用 Converter 完成模型转换。
- **写入返回**：按接口契约返回 VO 或结果状态。Controller 返回业务结果，统一响应包装交给 Web Starter。

### 各层命名与职责

以下以应用管理为命名示例，类名采用大驼峰，按业务含义与场景区分对象。

| 对象 | 命名示例 | 用途与传递边界 |
| --- | --- | --- |
| Query | `ApplicationPageQuery` | 查询条件、分页和排序；同一服务内可贯穿 Controller、Service、Mapper |
| Form | `ApplicationCreateForm`、`ApplicationUpdateForm` | 新增或更新的表单入参；按操作声明字段与校验规则 |
| DTO | `ApplicationDTO` | 明确定义的跨层或跨服务传输模型；字段由接口契约决定 |
| VO | `ApplicationVO`、`ApplicationDetailVO` | 面向调用方的返回模型；只暴露接口需要的展示字段 |
| BO | `ApplicationBO` | 联表查询、多实体组合或业务计算的内部对象 |
| Entity | `Application` | 与数据库表映射的持久化实体；留在服务内部 |

Query、Form、DTO、VO 可分别放在 `query/`、`form/`、`dto/`、`vo/`；内部 BO、Entity 沿用 `pojo/bo/`、`pojo/entity/`，转换器放在 `converter/`。对外契约需要共享时，将相应模型与 Feign 接口放入该服务的 `*-api` 模块。

对象以职责区分：Form 描述调用方提交的数据，Entity 描述持久化结构，BO 描述内部业务组合，VO 描述接口返回。相同字段也可能有不同的校验、权限与生命周期，不能直接用 Entity 充当所有输入和输出。

### 跨服务：按接口契约转换

{{< layer-diagram name="cross-service-model" title="跨服务契约与转换" original="/docs/latest/03_devrules/后端开发规范/images/model2.png" >}}

*原跨服务图，点击可放大查看。实线表示请求，虚线表示返回；同一平台内部调用与跨平台 OpenAPI 均遵循契约边界。*

1. **A 调用 B**：A 的 Service / BFF 按 B 的接口契约，将自己的查询或写入模型转换为 B 的 Query、Form 或 DTO，再通过 Feign / HTTP 调用 B 的 Controller。
2. **B 返回 A**：B 在内部将 Entity/BO 转为自己的 VO；A 收到 B 的结果后，按自身页面或业务需要聚合、转换为 A 的 VO。
3. **B 继续调用 C**：同样在调用边界处理 `b-Query → c-Query` 和 `c-VO → b-VO`。第三方协议与模型由 Thirdparty 等适配边界封装。

**跨服务不要求所有对象都改名为 DTO。** Query、Form、VO 也可以成为稳定的 API 契约；现有服务间接口即有这类用法。双方语义、字段和版本完全一致时，可以直接使用 `*-api` 的契约模型；发生聚合、裁剪或语义差异时再转换，不必每经过一层就机械复制对象。

跨服务共享的是接口及其必要模型，调用方不依赖对方的 Entity、Mapper、Service 实现。BO 与 Entity 不作为跨服务的公共返回契约。

### 转换放在哪里

| 转换 | 负责位置 |
| --- | --- |
| Form/DTO → Entity/BO | 业务 Service 调用 Converter，结合业务规则组装持久化或内部模型 |
| Entity/BO → VO | 业务 Service 调用 Converter，控制对外字段与展示结构 |
| 本方模型 ↔ 对方接口模型 | 发起远程调用的 Service / BFF 或适配层，围绕对方契约完成转换 |

转换统一优先使用 MapStruct / MapStruct Plus，由 `XxxConverter` 明确字段映射。Converter 负责结构转换；业务校验、权限、事务和远程调用留在相应业务层。主键、租户、拥有者等字段按服务端可信上下文赋值，不能靠同名字段复制完成授权判断。

同一对象可以在语义一致的层之间复用，模型转换也可以直接得到目标 VO，无需为了补齐后缀强制经过 DTO、BO 等全部类型。

详细约束见[应用分层规范](/docs/latest/03_devrules/后端开发规范/应用分层/)，转换工具见 [MapStruct](/docs/latest/01_services/框架基础/mapstruct/)，完整业务链路见[创建示例服务](/docs/latest/04_devmanual/创建服务模块/)。

## 请求协作

模块如何连接、身份如何传递、权限在哪里检查，继续阅读下级章节[请求链路](/docs/latest/00_introduce/应用架构/请求链路/)。
