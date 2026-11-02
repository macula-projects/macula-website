---
title: "UED规范"
linkTitle: "UED规范"
weight: 3
manual_content: true
source_refs: [{"repository": "https://github.com/macula-projects/macula-samples", "branch": "main", "commit": "5770c37f5ae2c62a7d19ea8dd66a41d37c1ec41e", "paths": ["macula-samples-admin/package.json", "macula-samples-admin/src/views/service1/application/index.vue", "macula-samples-admin/src/views/service1/application/save.vue"]}]
---

## 一致的页面结构

管理后台沿用现有 Vue 3、Element Plus 与项目组件体系。列表页依次呈现标题、筛选条件、操作区、表格与分页；编辑页使用有标签的表单，保持相同字段的名称、顺序和校验提示一致。参考 `src/views/service1/application`，按业务优化，不直接复制其中的 Secret 展示方式。

## 可读与可操作

正文与表单保持清晰字号和足够行距；长字段在自身区域截断或展开，重要名称不挤成逐字换行。窄屏允许表格自身横向滚动，页面整体不横向溢出。状态除颜色外提供文字；图标按钮必须有可访问名称与明确提示。

输入框关联 label，必填和错误信息同时提供文本。键盘可到达筛选、提交、分页及对话框关闭按钮，焦点清晰；弹窗打开时进入弹窗、关闭后返回触发位置。错误提示说明字段与处理方法，保留已填内容。

## 状态与权限

覆盖加载、空数据、请求失败、无权限与提交成功状态。提交期间防止重复操作，删除等动作明确对象并确认。前端隐藏按钮改善体验，后端仍需独立授权；日志、列表和错误提示不展示令牌与密钥。

## 验收

在桌面、窄屏和纯键盘下完成一次搜索、创建、校验失败、编辑与取消；检查长中文名称、空列表和网络错误。自动化断言和实际浏览器检查分别记录，不能以构建成功替代可访问性验收。
