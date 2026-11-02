# Macula 官方文档

基于[Hugo](https://gohugo.io)和[Docsy](https://docsy.dev)的Macula官方文档


## 安装Hugo

请[参考官网](https://gohugo.io/installation/)

## 运行

```bash
git clone --depth 1 https://github.com/macula-projects/macula-website.git

## If you want to do SCSS edits and want to publish these, you need to install `PostCSS`

npm install

## Running the website locally

hugo server

```

## 文档版本

首页、博客等页面共用一套内容。文档顶部提供版本切换，侧栏只展示当前版本；同一章节存在时保留章节，否则进入目标版本首页。

| 文档入口 | Macula Boot 分支 | 内容来源 |
| --- | --- | --- |
| `/docs/latest/` | `main` | 按 5.x 栏目组织当前分支的 README、模块文档及迁移指南 |
| `/docs/6.0.x/` | `6.0.x` | 按 5.x 栏目组织 6.0.x 分支的 README 和模块文档 |
| `/docs/5.x/` | `5.x` | 官网已有的 5.x 文档 |
| `/docs/4.0/` | 历史归档 | 从 `98_old/v4.0` 独立出的完整文档 |
| `/docs/3.1/` | 历史归档 | 从 `98_old/v3.1` 独立出的完整文档 |

`/docs/` 默认跳转到 latest。原有 `/docs/<章节>/` 地址跳转到 5.x 的对应页面，避免旧链接指向其他版本。

版本与分支映射统一维护于 `data/doc_versions.json`。更新 6.0.x 和 latest 文档时，先在相邻的 `macula-boot` 仓库更新对应本地分支，再执行：

```bash
python3 scripts/sync-boot-docs.py
# 或指定 Boot 仓库位置
python3 scripts/sync-boot-docs.py --boot-repo /path/to/macula-boot
hugo --minify
```

5.x、6.0.x、latest 三个版本的目录和章节文件路径完全一致，均以 `content/zh-cn/docs/5.x/` 为基准，包括平台简介、平台能力、开发规范、开发指引、运维指引和关于。源码模块路径只用于内容映射，不会生成另一套文档目录。

3.1、4.0 分别独立维护在 `content/zh-cn/docs/3.1/`、`content/zh-cn/docs/4.0/`，保留各自历史目录结构，直接从顶部版本菜单进入，不再嵌套或复制到其他版本中。它们在版本配置中标记为 `archived: true`，同步工具会跳过历史版本。原始 `/docs/98_old/<版本>/` 及曾使用的 `/docs/<5.x|6.0.x|latest>/98_old/<版本>/` 章节地址均跳转到独立历史文档；旧图片地址通过 Hugo 静态挂载保留。原有“历史文档”目录入口跳转到 4.0 首页。

同步工具只读取 Git 已提交内容，不切换或修改 Boot 工作区。`scripts/sync-boot-docs.py` 中的 `MAPPING` 将分支 README 映射到已有章节；生成章节保留 5.x 的标题、导航名和排序，并记录来源分支、提交和文件路径。编辑链接指向对应 Boot 分支。

暂无对应分支资料的章节沿用 5.x 内容并明确标注尚未核对，历史归档保持原文。执行同步会重新生成 6.0.x 和 latest 文档；人工修订应同步维护生成规则。生成器会检查文件路径与 5.x 完全一致，且不会为新模块自动添加新的栏目。文档快照随官网保存，构建及部署无需再次访问 Boot 仓库。

人工编写的版本专属章节可在 Front Matter 中设置 `manual_content: true`，同步工具会完整保留该页面。6.0.x 与 latest 的“运维指引 → 升级指南”分别记录从 5.x、6.0.x 升级的步骤、分支对照提交和参考源码；它们不是某一份 README 的直接副本。latest 概述同步时会移除 README 中“从 6.0 升级到 6.1”的详细迁移章节，仅保留指向统一升级指南的入口。后续分支升级说明变化时，应同步维护对应指南及此提取规则。

历史版本名称与正式路径统一不带 `v` 前缀，原 `/docs/v3.1/`、`/docs/v4.0/` 及其章节地址保留跳转，图片等资源地址继续可用。
