---
title: "工程规约"
linkTitle: "工程规约"
weight: 2
---

> 本章沿用 5.x 的文档内容，尚未按 latest（当前） 分支核对。涉及依赖、配置或 API 时，请以 [main 分支源码](https://github.com/macula-projects/macula-boot/tree/main) 为准。

## 概述

建议按以下的前端工程（管理后台类的前端工程）目录组织项目，并进行功能开发。

## 目录

整体目录结构如下图所示：

![image](../images/pd.png)

|  目录名   | 说明  |
|  ----  | ----  |
| public	| 静态资源(不会被Webpack打包)，存放静态资源文件，不会被Webpack打包 | 
| src	| 源代码 |
| src/api	| 统一的API列表管理 |
| src/assets	| 静态资源(会被打包)，存放全局的资源文件 |
| src/components	| 组件目录，所有UI组件代码。每一个组件单独一个目录文件，命名规则采用驼峰式命名法。|
| src/config	| 存放配置文件，包括组件的基础配置信息等 |
| src/directives	| 自定义的一些指令，例如 v-auth |
| src/layout	| 存放框架的布局、视图 |
| src/locales	| 存放关于国际化的资源文件本 |
| src/router	| 存放处理路由表的逻辑 |
| src/store	| 用于缓存状态管理 |
| src/style	| 存放全局样式 |
| src/utils	| 存放全局工具类 |
| src/views	| 存放服务所有视图 |
| src/App.vue	| 入口视图 |
| src/main.js	| 入口文件 |
| package.json	| 包管理 |
| vue.config.js	| vue-cli 配置 |
