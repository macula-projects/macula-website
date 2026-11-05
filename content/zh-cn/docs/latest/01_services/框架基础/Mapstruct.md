---
title: "Macula Boot Starter MapStruct"
linkTitle: "MapStruct"
weight: 2
source_repository: "https://github.com/macula-projects/macula-boot"
source_path: "macula-boot-starters/macula-boot-starter-mapstruct/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-mapstruct/README.md", "macula-boot-parent/pom.xml", "macula-boot-starters/macula-boot-starter-mapstruct/pom.xml", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/DateTimeConverter.java", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/GlobalMapperConfig.java", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/config/DateTimeProperties.java", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/config/MapStructAutoConfiguration.java", "macula-boot-starters/macula-boot-starter-mapstruct/src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports", "macula-boot-starters/macula-boot-starter-mapstruct/src/test/java/dev/macula/boot/mapstruct/DateTimeMappingTest.java"]
source_branch: "main"
source_commit: "6f69e84254b7d1c134d8491c2dbca10dd80de41a"
manual_content: true
---

## 概览

提供 MapStruct / MapStruct Plus 对象映射，以及接口 `Date` 与实体 `LocalDateTime` 的公共双向转换。Mapper 实现由注解处理器在编译期生成；运行时通过 Spring 注入日期转换器，按统一存储时区处理时间。

与数据库交互的 Entity / BO 使用不带时区的日期时间类型；对外 Form、DTO、VO 中表示**具体时刻**的字段使用 `Date` 或 `Instant`。当前公共转换器只内置 `Date ↔ LocalDateTime`，`Instant` 需要显式的业务转换规则，不能假设已自动接入同样的存储时区。类型选择与 JSON 契约见 [Web Starter 的数据库日期约定](/docs/latest/01_services/框架基础/web/#数据库日期)。

## 组件坐标

继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 时由 Parent 管理版本，不重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-mapstruct</artifactId>
</dependency>
```

## 使用配置

### 运行时配置

```yaml
macula:
  mapstruct:
    enabled: true              # 默认启用日期时间转换器的自动配置
  time:
    storage-zone: Asia/Shanghai # 示例值，必须与已有数据库的存储时间约定一致
```

| 配置 / 条件 | 默认与行为 |
| --- | --- |
| `macula.mapstruct.enabled` | 默认 `true`；设为 `false` 不注册默认 DateTimeConverter Bean |
| `macula.time.storage-zone` | 可选；未配置或留空时，固定使用创建转换器时的 JVM 默认时区 |
| 合法时区值 | 去除首尾空白后解析，例如 `Asia/Shanghai`、`UTC` |
| 非法时区值 | 默认转换器初始化失败，不静默回退 |
| 已有 DateTimeConverter Bean | 默认 Bean 退让，由业务自定义实现负责转换 |
| Plus Converter 不在 classpath | 自动配置不生效 |

生产环境建议显式设置存储时区，并在所有实例中保持一致。时区在转换器创建时固定，不代表配置中心发布后会自动热切换。它不是展示时区，也不会修改 JVM、Jackson、JDBC 或数据库会话设置；修改该值不会自动转换历史数据。

### 编译时配置

继承更新后的 Parent 后，MapStruct Plus 默认使用 `GlobalMapperConfig`，业务模型无需重复声明 `uses`。Parent 还维护 Lombok、MapStruct Plus processor、Lombok binding 和 Spring 组件模型参数，IDE 需启用注解处理。

若已有业务 Plus 全局配置，在业务 POM 指定它，替换 Parent 默认类名；这是可选覆盖，不是普通接入的必填项：

```xml
<properties>
    <mapstruct-plus.mapper-config-class>com.example.ApplicationMappingConfig</mapstruct-plus.mapper-config-class>
</properties>
```

仅导入 BOM 不会继承构建插件，需自行配置注解处理器与 `-Amapstruct.plus.mapperConfigClass=dev.macula.boot.mapstruct.GlobalMapperConfig`。自动配置只能注册运行时 Bean，不能修改已编译的映射实现。

## 核心功能

### 日期时间转换边界

以 `storage-zone: Asia/Shanghai` 为例，同一个时刻的转换方向为：

```text
接口 Date：2026-11-05T00:50:30Z
    ↓ DateTimeConverter.toLocalDateTime
Entity / BO：2026-11-05T08:50:30
    ↓ JDBC 按约定读写，不给字段附加时区
数据库 DATETIME：2026-11-05 08:50:30

返回时按同一存储时区反向转换，得到原来的接口时间点。
```

下面是 `DateTimeConverter` 的源码节选，省略类注释与 import，展示公共转换的实际边界：

```java
public class DateTimeConverter {
    private final ZoneId storageZone;

    public DateTimeConverter(String storageZone) {
        this.storageZone = storageZone == null || storageZone.isBlank()
            ? ZoneId.systemDefault() : ZoneId.of(storageZone.trim());
    }

    public LocalDateTime toLocalDateTime(Date value) {
        return value == null ? null : LocalDateTime.ofInstant(value.toInstant(), storageZone);
    }

    public Date toDate(LocalDateTime value) {
        return value == null ? null : Date.from(value.atZone(storageZone).toInstant());
    }
}
```

- 双向转换共用一个 `ZoneId`；两端为 null 时返回 null。
- `LocalDateTime` 没有时区，必须按数据库约定解释，不能在不同实例上使用不同的默认时区。
- `Date` 表示毫秒精度的时间点，不保存时区 ID；数据库小数秒精度也需与接口精度约定一致。
- 若使用存在夏令时切换的存储时区，某些本地时间会重复或不存在，不能承诺所有值都无歧义往返；需要这类时区的系统应单独明确处理规则。

完整实现见 [DateTimeConverter 源码](https://github.com/macula-projects/macula-boot/blob/6f69e84254b7d1c134d8491c2dbca10dd80de41a/macula-boot-starters/macula-boot-starter-mapstruct/src/main/java/dev/macula/boot/mapstruct/DateTimeConverter.java)。

### MapStruct Plus：默认接入公共转换器

继承更新后的 Parent 并引入本 Starter 后，模型使用 `@AutoMapper` 即可。以下模型分别放在自己的 Java 文件中，示例省略 getter / setter：

```java
import io.github.linpeilie.annotations.AutoMapper;
import java.time.LocalDateTime;
import java.util.Date;

@AutoMapper(target = UserEntity.class)
public class UserForm {
    private String username;
    private Date createTime;
    // getter / setter
}

public class UserEntity {
    private String username;
    private LocalDateTime createTime;
    // getter / setter
}
```

在 Spring 业务 Bean 中注入 `io.github.linpeilie.Converter` 后调用：

```java
@Autowired
private Converter converter;

UserEntity entity = converter.convert(form, UserEntity.class);
UserForm result = converter.convert(entity, UserForm.class);
```

编译与运行是两步，不要混淆：

1. Parent 将共享配置类传给 Plus processor，Plus 把 `DateTimeConverter` 合并到自己生成的 Config，再生成 Mapper。
2. Boot 从 `AutoConfiguration.imports` 发现 `MapStructAutoConfiguration`，注册可覆盖的转换器；生成的 Spring Mapper 注入并调用它。

不需要额外扫描 Starter 包或手工 `@Import`。依赖 Spring 配置的映射使用注入的 Converter，不以 `new Converter()` 绕过容器。

### 普通 MapStruct：显式引用共享配置

普通 MapStruct 需要在每个 Mapper 上显式设置 `config`：

```java
import dev.macula.boot.mapstruct.GlobalMapperConfig;
import org.mapstruct.Mapper;

@Mapper(config = GlobalMapperConfig.class)
public interface UserMapper {
    UserEntity toEntity(UserForm form);
    UserForm toForm(UserEntity entity);
}
```

在 Spring 业务 Bean 中注入生成的 `UserMapper` 后调用。模型不必再标 `@AutoMapper`；上面的类型示例若用于此方案，可去掉该注解。

共享配置同时面向普通 MapStruct 和 Plus，源码节选如下：

```java
@io.github.linpeilie.annotations.MapperConfig(uses = DateTimeConverter.class)
@org.mapstruct.MapperConfig(
    componentModel = MappingConstants.ComponentModel.SPRING,
    uses = DateTimeConverter.class
)
public interface GlobalMapperConfig {
}
```

仅引入 Starter 或设置 `componentModel = "spring"`，不等于普通 Mapper 已接入公共日期规则。省略 `config` 时仍使用 MapStruct 自身的转换规则，不能期待 `storage-zone` 自动影响它。运行时注册 Bean 不能代替编译期引用。

### 字段名称不同的映射

普通字段转换仍使用 MapStruct / Plus 原有能力。例如普通 Mapper 将 `username` 映射为目标对象的 `user`：

```java
@Mapper(config = GlobalMapperConfig.class)
public interface SourceTargetMapper {
    @Mapping(source = "username", target = "user")
    TargetDto toTarget(SourceDto source);
}
```

Spring 组件模型下优先注入生成的 Mapper。只有显式采用无 Spring 依赖的默认组件模型时，才考虑 `Mappers.getMapper()`；它不适用于依赖本公共转换器 Bean 的映射。

### 自定义配置与禁用

- 提供自己的 `DateTimeConverter` Bean 时，默认 Bean 自动退让。
- 设置前面集中配置中的 `macula.mapstruct.enabled=false`，只禁用默认转换器自动配置，不会改写已生成 Mapper；这些 Mapper 仍依赖转换器时，须自行提供 Bean 或调整编译配置。
- 业务 Plus 配置使用 `io.github.linpeilie.annotations.MapperConfig`。要保留公共日期转换，将 `DateTimeConverter.class` 合并到 `uses`；每个业务编译模块只定义一份 Plus 配置。
- Parent 的配置类编译参数优先于模块源码中的 Plus 配置；已有自定义类时同时覆盖前述 POM 属性，避免被 Parent 默认值替代。

接口使用 `Instant` 时，本提交没有增加 `Instant ↔ LocalDateTime` 方法。可按同一存储时区提供业务转换并接入 Mapper 的 `uses`；如借道 `Date.from(instant)`，需明确纳秒会收敛到毫秒，不能声称无损转换。

### 验证与排查

| 现象 | 检查方向 |
| --- | --- |
| 转换后差几个小时 | 实际存储时区、JVM 默认值、Mapper 是否使用共享配置；不要靠 Jackson 格式修补对象映射 |
| Mapper 找不到转换器 Bean | 是否启用自动配置、是否误用 `new Converter()` / `Mappers.getMapper()`、禁用后是否提供自定义 Bean |
| 代码未生成或仍用旧规则 | 注解处理是否生效、Parent 与 Starter 是否都已更新、是否残留旧编译产物 |
| 非法时区导致启动失败 | 修正实际配置值，业务覆盖 Bean 时检查自己的时区策略 |

框架源码中的验证命令如下，测试不连接数据库：

```bash
mvn -pl macula-boot-starters/macula-boot-starter-mapstruct -am test
```

已有用例覆盖合法 / 缺省时区、双向往返、null、非法配置、禁用、用户覆盖和自动配置发现，并实际生成普通 MapStruct 与 Plus Mapper。跨 JSON、JDBC 和真实数据库的整条链路仍需应用集成测试。

## 依赖引入

以下为组件引入的主要依赖，不需要业务模块再重复添加。版本与注解处理器由 Parent 统一管理。

```xml
<dependencies>
    <dependency>
        <groupId>io.github.linpeilie</groupId>
        <artifactId>mapstruct-plus-spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>cn.hutool</groupId>
        <artifactId>hutool-all</artifactId>
    </dependency>
</dependencies>
```

更多映射能力见 [MapStruct](https://mapstruct.org/documentation/stable/reference/html/) 与 [MapStruct Plus](https://mapstruct.plus/)。

## 版权说明

- [MapStruct](https://github.com/mapstruct/mapstruct/blob/main/LICENSE.txt)
- [MapStruct Plus](https://github.com/linpeilie/mapstruct-plus/blob/main/LICENSE)
