
---
aliases: ["/docs/98_old/v4.0/feature/12_web/", "/docs/5.x/98_old/v4.0/feature/12_web/", "/docs/6.0.x/98_old/v4.0/feature/12_web/", "/docs/latest/98_old/v4.0/feature/12_web/", "/docs/v4.0/feature/12_web/"]
type: docs
title: "WEB"
linkTitle: "WEB"
weight: 1
description: ""
---

#### 使用基类 Controller

在展示层编写的 Controller 实现，需要直接或间接扩展至 BaseController。

```plain
@Controller
public class AppController extends BaseController {
}
```

在 BaseController 中处理了大量的异常处理方式以及数据返回要求的设定。

#### 前端请求重定向

通过 RewriteFilter，过滤后端请求，不属于后端的请求，交由前端路由处理。

默认配置如下，可根据项目修改重定向地址，路由通配符和静态文件通配符。

```plain
@Bean
public FilterRegistrationBean filterRegistration() {
    FilterRegistrationBean<RewriteFilter> registration = new FilterRegistrationBean<>();
    registration.setFilter(new RewriteFilter());
    registration.addUrlPatterns("/static/*");
    registration.addInitParameter(RewriteFilter.REWRITE_TO,"/");
    registration.addInitParameter(RewriteFilter.ROUTER_PATTERNS, "/static/*");
    registration.addInitParameter(RewriteFilter.STATIC_PATTERNS, "/static/js/*;/static/css/*;/static/img/*;/static/assets/*;/static/fonts/*;/static/favicon.ico");
    registration.setName("rewriteFilter");
    registration.setOrder(1);
    return registration;
}
```

#### WEB 配置项

WEB 配置项在 Nacos 中配置

```
macula.web.ignoringRegexPattern

不经过安全拦截的URL正则

默认值：/public.*|/error.*|/static/.*|/favicon.ico.*|/timezone.*

macula.web.maximumSessions

同一个用户登录的最大会话数

默认值：1

macula.web.expiredUrl

会话过期后跳转的URL

默认值：/login

**macula.web.failureUrl

登录发生错误跳转的页面

默认值：/login?error

macula.web.isMenuAsRole

是否把 Menu code 当成自己的一个角色

默认值：false
```