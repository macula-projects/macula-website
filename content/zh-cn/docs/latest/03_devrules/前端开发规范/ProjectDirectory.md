---
title: "工程规约"
linkTitle: "工程规约"
weight: 2
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["macula-samples-admin/package.json", "macula-samples-admin/vite.config.js", "macula-samples-admin/src/config/index.js"]}]
---

## 当前工程

当前 Samples 管理端使用 Vue 3 与 Vite，位于业务单仓的 `macula-samples-admin`；Cloud 管理端位于 Cloud 同仓。两者各自维护 package.json 和锁文件，按各自 README 选择 Node 版本，不混用安装目录。

```text
macula-samples-admin/
├── public/            # 原样复制的静态资源
├── src/
│   ├── api/           # API 模型和请求入口
│   ├── assets/        # 参与构建的资源
│   ├── components/    # 公共组件
│   ├── config/        # 环境配置与模块前缀
│   ├── directives/    # 指令
│   ├── layout/        # 布局
│   ├── locales/       # 国际化
│   ├── router/        # 路由
│   ├── store/         # 状态管理
│   ├── style/         # 全局样式
│   ├── utils/         # 请求、授权等工具
│   ├── views/         # 按业务组织的页面
│   ├── App.vue
│   └── main.js
├── vite.config.js
├── package.json
└── package-lock.json
```

## 开发约定

API 统一放在 `src/api/model` 并复用请求封装，不在每个页面拼接 IAM 或后端地址。组件只处理展示与交互，通用状态、错误和权限沿用现有项目约定。业务页面放在 `src/views/<领域>`，与 Cloud 菜单登记的组件路径保持一致。

Vite 按 mode 读取环境文件，代理规则在 `vite.config.js`；不存在需要维护的 `vue.config.js` 或 Webpack 配置。公开环境变量会打入浏览器代码，不能承载应用 SK、数据库密码等服务端凭据。登录兼容差异见[首次接入](/docs/latest/04_devmanual/首次接入macula-cloud/)。

## 构建与检查

在 Admin 目录执行 `npm ci`、`npm run dev`、`npm run build`。测试、lint 与端到端验证使用 package.json 中已有脚本；含自动修复的 lint 会修改文件，执行后检查差异。

旧工程目录图仍保留供历史对照，不作为 Vite 工程文件清单：

![历史前端工程目录示意](../images/pd.png)
