---
title: "Macula Boot Starter SpringDoc"
linkTitle: "Swagger"
weight: 14
source_path: "macula-boot-starters/macula-boot-starter-springdoc/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-springdoc/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

该模块是基于 [SpringDoc](https://springdoc.org/) 3.x 的 OpenAPI V3 规范 API 接口文档生成工具，兼容 Spring Boot 4。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-springdoc</artifactId>
</dependency>
```

## 使用配置

### 配置示例

以下集中列出本页涉及的配置。可选能力按需保留，环境值按实际部署填写。

#### application.yml

```yaml
springdoc:
  # packages-to-scan: com.example.business.controller
  # paths-to-match: /api/**
  api-docs:
    path: /v3/api-docs
    enabled: true  # 默认是true，用于开关API文档
  swagger-ui:
    path: /swagger-ui.html
    enabled: false # 默认是true，用于开关API UI
```

### 关键配置

无自有配置前缀；生产环境按需关闭文档入口或限制访问。

| 属性 | 默认值 | 说明 |
| --- | --- | --- |
| `springdoc.api-docs.enabled` | `true` | 生成 OpenAPI 文档 |
| `springdoc.api-docs.path` | `/v3/api-docs` | JSON 文档路径 |
| `springdoc.swagger-ui.enabled` | `true` | 启用 Swagger UI |
| `springdoc.swagger-ui.path` | `/swagger-ui.html` | UI 入口路径 |
| `springdoc.packages-to-scan` | 未设置 | 限定扫描包 |
| `springdoc.paths-to-match` | 未设置 | 限定文档接口路径 |

## 核心功能

### 示例

```java
/**
 * 部门控制器
 *
 * @author haoxr
 * @since 2020/11/6
 */
@Tag(name = "部门接口", description = "部门接口")
@RestController
@RequestMapping("/api/v1/dept")
@RequiredArgsConstructor
public class SysDeptController {

    private final SysDeptService deptService;

    @Operation(summary = "获取部门列表")
    @GetMapping
    public List<DeptVO> listDepartments(DeptQuery queryParams) {
        List<DeptVO> list = deptService.listDepartments(queryParams);
        return list;
    }

    @Operation(summary = "获取部门下拉选项")
    @GetMapping("/options")
    public List<Option> listDeptOptions() {
        List<Option> list = deptService.listDeptOptions();
        return list;
    }

    @Operation(summary = "获取部门详情")
    @Parameter(name = "部门ID")
    @GetMapping("/{deptId}/form")
    public DeptForm getDeptForm(@PathVariable Long deptId) {
        DeptForm deptForm = deptService.getDeptForm(deptId);
        return deptForm;
    }

    @Operation(summary = "新增部门")
    @AuditLog(title = "新增部门")
    @PostMapping
    public Long saveDept(@Valid @RequestBody DeptForm formData) {
        Long id = deptService.saveDept(formData);
        return id;
    }

    @Operation(summary = "修改部门")
    @AuditLog(title = "修改部门")
    @PutMapping(value = "/{deptId}")
    public Long updateDept(@PathVariable Long deptId, @Valid @RequestBody DeptForm formData) {
        deptId = deptService.updateDept(deptId, formData);
        return deptId;
    }

    @Operation(summary = "删除部门")
    @AuditLog(title = "删除部门")
    @Parameter(name = "部门ID，多个以英文逗号(,)分割")
    @DeleteMapping("/{ids}")
    public boolean deleteDepartments(@PathVariable("ids") String ids) {
        boolean result = deptService.deleteByIds(ids);
        return result;
    }
}


@Schema(description = "部门表单对象")
@Data
public class DeptForm {

    @Schema(description = "部门名称")
    private String name;

    @Schema(description = "父部门ID")
    @NotNull(message = "父部门ID不能为空")
    private Long parentId;

    @Schema(description = "状态")
    private Integer status;

    @Schema(description = "排序")
    private Integer sort;
}
```

### 官方文档

- Swagger UI： http://xxx/context-path/swagger-ui/index.html

- API Docs： http://xxx/context-path/v3/api-docs

## 依赖引入

```xml
<dependencies>
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

## 版权说明

- springdoc：https://github.com/springdoc/springdoc-openapi/blob/master/LICENSE
