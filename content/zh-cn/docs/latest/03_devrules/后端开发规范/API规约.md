---
title: "API规约"
linkTitle: "API规约"
weight: 2
---

> 本章沿用 5.x 的文档内容，尚未按 latest（当前） 分支核对。涉及依赖、配置或 API 时，请以 [main 分支源码](https://github.com/macula-projects/macula-boot/tree/main) 为准。

## 概述

所有软件的UI功能都依赖于后端的API能力输出，规范的API设计以及版本管理对软件功能交付的质量与效率都至关重要。
> 说明：这里的API是指Restful API

## 设计原则

### API根URL

如果预期系统非常庞大，则建议尽量将API部署到独立专用子域名（例如：“api.”）下；如果确定API很简单，不会进一步扩展，则可以考虑放到应用根域名下面（例如，“/api/”）。

      独立子域名：https://api.example.com/api/v1/*
      共享应用根域名：https://example.org/[xxx]/api/v1/* （微服务平台一般都是通过网关的统一域名对外）

### API各模块URL

建议每个领域或者Controller统一一个URL根，一般的形式是：/api/v1/[xxx]，xxx表示某个领域模块名称

### URI末尾不要添加“/”

多一个斜杠，语义完全不同，究竟是目录，还是资源，还是不确定而多做一次301跳转？尽量保持URI结构简洁、语义清晰。

      负面case：http://api.canvas.com/api/v1/shapes/
      正面case：http://api.canvas.com/api/v1/shapes

### 禁止在URL中使用“_”

目的是提高可读性，“_”可能被文本查看器中的下划线特效遮蔽。建议使用连字符“-”替代下划线“_”,使用“-”提高URI的可读性。

      负面case：http://api.example.com/api/v1/blogs/my_first_post
      正面case：http://api.example.com/api/v1/blogs/my-first-post

### 禁止使用大写字母

RFC 3986中规定URI区分大小写，但别用大写字母来为难程序员了，既不美观，又麻烦，同样的原则：建议使用连字符“-”连接不同单词。

      负面case：http://api.example.com/api/v1/My-Folder/My-Doc
      正面case：http://api.example.com/api/v1/my-folder/my-doc

### 不要在URI中包含扩展名

应鼓励REST API客户端使用HTTP提供的格式选择机制Accept request header。

      负面case：http://api.example.com/api/v1/my-doc/hello.json
      正面case：http://api.example.com/api/v1/my-doc/hello

### 建议URI中的名称使用复数

为了保持URI格式简洁统一，资源在URI中应统一使用复数形式，如需访问资源的一个实例，可以通过资源ID定位（@PathVariable）。

      负面case：http://api.college.com/api/v1/student/3248234
      正面case：http://api.college.com/api/v1/students/3248234

如何处理关联关系？

      http://api.college.com/api/v1/students/3248234/courses - 检索学生3248234所学习的所有课程
      http://api.college.com/api/v1/students/3248234/courses/physics - 检索学生3248234的所学习的物理课程

### 建议URI设计时只包含名词

每个URI代表一种资源或者资源集合，因此，建议只包含名词，不包含动词。

      负面case：http://api.example.com/api/v1/get-all-employees
      正面case：http://api.example.com/api/v1/employees

那么，如何告诉服务器端我们需要进行什么样的操作？CRUD？

答案是由HTTP动词表示。

      GET（SELECT）：从服务器取出资源（一项或多项）。
      POST（CREATE）：在服务器新建一个资源。
      PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
      PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
      DELETE（DELETE）：从服务器删除资源。

### 禁止由第三方开发人员任意指定约束条件

非常重要的一点：禁止让第三方开发人员自己任意指定排序过滤器、返回结果集的约束条件。强烈建议服务器端设置默认单页数量，如果无限制，很可能造成服务器资源及网络资源过度消耗，响应缓慢，网络丢包等异常情况。

## 版本管理

### 整体建议

+ 建议通过URI指定服务版本，版本采用字符“v”+数字主版本号，例如，/v1/xxxs

+ 建议版本控制在资源层面，也即Controller维度

  服务后端分包建议规则如下：

      Domain: com.xxx.[user].domain.entity
      Api:
      com.xxx.api.[user].controller.v1
      com.xxx.api.[user].controller.v2

+ API升级建议

  + 尽量做兼容性设计，不要随便升级版本

  + 升级可分步实施，达到最终整个资源整体升级的目的，不同版本相互独立，便于后续拆分独立部署、独立维护等（可能存在代码重复，尽可能抽象通用服务或方法）

  + 先将资源的部分方法升级至高版本，并进行灰度发布，例如，/v1/users/check升级至 /v2/users/check，其他API版本维持v1不变

  + 升级资源的所有方法至高版本，并发布公告，要求客户限期升级API

  + 停止旧版本服务
  
### URL中指定版本

  + URI上添加版本号：例如，https://api.example.org/api/v1/users

  + 参数中添加版本号： 例如，https://api.example.org/api/users?v=1.0

  好处：

  + 直接可以在URI中直观的看到API版本；
  + 可以直接在浏览器中查看各个版本API的结果；

  坏处：

  + 版本号在URI中破坏了REST的HATEOAS（hypermedia as the engine of application state）规则。版本号和资源之间并无直接关系。

## 接口注释

Swagger注释描述，要求使用OpenAPI规范注释接口

## 参考文章

[《汉得开放平台文档》](https://open.hand-china.com/document-center/doc/product/10067/10239?doc_id=34378&doc_code=6208)
