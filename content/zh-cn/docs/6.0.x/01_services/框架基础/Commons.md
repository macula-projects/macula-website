---
title: "Macula Boot Commons"
linkTitle: "Commons"
weight: -1
source_path: "macula-boot-commons/README.md"
source_paths: ["macula-boot-commons/README.md"]
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
---

## 概览

主要引入所有模块都需要使用到的工具类，基础类

## 组件坐标

```xml
<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-commons</artifactId>
    <version>${macula.version}</version>
</dependency>
```

## 使用配置

Commons 提供公共数据结构与工具契约，无独立 YAML 配置项；按下文接口在业务代码中使用。

## 核心功能

### 统一的返回结构

```java
@Data
public class Result<T> implements Serializable {
    private boolean success;

    private String code;

    private String msg;

    private T data;

    public static <T> Result<T> success() {
        return success(null);
    }

    public static <T> Result<T> success(T data) {
        Result<T> result = new Result<>();
        result.setSuccess(true);
        result.setCode(ApiResultCode.SUCCESS.getCode());
        result.setMsg(ApiResultCode.SUCCESS.getMsg());
        result.setData(data);
        return result;
    }

    public static <T> Result<T> failed() {
        return failed(ApiResultCode.FAILED);
    }

    public static <T> Result<T> failed(ResultCode resultCode) {
        return failed(resultCode, null);
    }

    public static <T> Result<T> failed(ResultCode resultCode, T data) {
        // data是错误原因
        Result<T> result = new Result<>();
        result.setSuccess(false);
        result.setCode(resultCode.getCode());
        result.setMsg(resultCode.getMsg());
        result.setData(data);
        return result;
    }

    public static <T> Result<T> judge(boolean status) {
        if (status) {
            return success();
        } else {
            return failed();
        }
    }
}
```

### 全局常量

### Hutool工具类

### 全局异常类

```java
// 框架异常基类
public class MaculaException extends RuntimeException {

    public MaculaException() {
        super();
    }

    public MaculaException(String message) {
        super(message);
    }

    public MaculaException(String message, Throwable cause) {
        super(message, cause);
    }

    public MaculaException(Throwable cause) {
        super(cause);
    }
}

// REST服务层异常
public class ApiException extends MaculaException {
    private ResultCode resultCode;

    public ApiException(ResultCode resultCode, String exceptionMessage) {
        // message用于用户设置抛出错误详情，例如：当前价格-5，小于0
        super(exceptionMessage);
        this.resultCode = resultCode;
    }

    public ApiException(String exceptionMessage) {
        super(exceptionMessage);
        this.resultCode = ApiResultCode.API_ERROR;
    }

    public ResultCode getResultCode() {
        return this.resultCode;
    }
}
```

## 依赖引入

以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>io.swagger.core.v3</groupId>
    <artifactId>swagger-annotations</artifactId>
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
    <groupId>com.alibaba</groupId>
    <artifactId>transmittable-thread-local</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk18on</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>jakarta.validation</groupId>
    <artifactId>jakarta.validation-api</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-annotation</artifactId>
</dependency>
```

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

## 版权说明

Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。
