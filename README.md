# Macula 官方文档

基于[Hugo](https://gohugo.io)和[Docsy](https://docsy.dev)的Macula官方文档


## 构建环境与运行

使用 Hugo Extended **0.169.0**、Docsy **0.18.1**、Node.js **24 LTS** 和 Go **1.24+**。主题通过 Hugo Modules 获取；Bootstrap **5.3.8**、Font Awesome **7.3.1** 与 Sass Embedded **1.107.1** 由 npm 锁文件固定。样式直接使用 Dart Sass，不再需要 PostCSS 或单独安装全局 Sass。

```bash
git clone --depth 1 https://github.com/macula-projects/macula-website.git
cd macula-website
nvm use
npm ci
npm run dev
# 完整构建，警告会使构建失败
npm run build
```

Hugo 安装请参考[官方说明](https://gohugo.io/installation/)。直接使用 Hugo 命令时，需将 node_modules/.bin 加入 PATH；推荐使用上述 npm 命令。GitHub Pages 与 Netlify 使用相同的 Hugo、Node 和锁文件。Docsy 0.18 使用 _partials、_shortcodes、_markup 目录和 Bootstrap 5。自定义模板保留本站版本导航与阅读布局，图片预览使用浏览器原生弹窗。

## 页面与样式维护

首页内容位于 `content/zh-cn/_index.html`；共享导航、页脚以及文档阅读布局位于 `layouts/`。`assets/scss/_styles_project.scss` 统一维护首页与文档样式，在 Docsy 默认样式之后加载，避免改动主题依赖。`assets/js/site.js` 提供手机目录、可键盘操作的章节折叠、代码复制和页内目录定位，未新增前端依赖。

品牌标记使用 `static/img/macula-mark.svg`，保留 M 形结构和蓝、青、白配色。大写 `MACULA` 字标使用 `static/img/macula-wordmark.svg`，按参考图的宽厚几何字形制作成独立矢量路径，避免设备字体不同导致外观变化。`layouts/_partials/brand.html` 统一导航和页脚标识，尺寸在共享样式中维护；浏览器图标复用 M 形标记。字标、页面强调色与主按钮统一使用品牌蓝 `#1672CE`，Logo 底色使用同色系的轻微明暗变化。

修改后运行 `npm run build` 验证构建，并通过 `npm run dev` 检查桌面与手机布局。验收时检查：首页不显示版本菜单、五个文档版本可切换、手机目录可展开、代码和表格不会撑宽页面。版本化 Markdown 正文与同步规则独立维护，不应为样式调整重写各分支内容。

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
npm run build
```

5.x、6.0.x、latest 三个版本保持一致的栏目层级，以 `content/zh-cn/docs/5.x/` 为基准，包括平台简介、平台能力、开发规范、开发指引、运维指引和关于。6.0.x 与 latest 在“框架基础”下额外声明独立的 `Commons.md` 和 `Async.md`，各自同步对应分支的模块 README；栏目 `_index.md` 只保留简介与章节导航。源码模块路径只用于内容映射，不会生成另一套文档目录。

latest 的组件章节同时核对 main 中实际存在的 Starter POM（包含 Cloud 下的嵌套模块），缺少显式映射的新模块会使同步失败。已删除模块不再从 5.x 回填；旧章节地址跳转至对应栏目。目前 TSF 从 latest 微服务目录移除，Loggers、Metrics、Tracing 三份重复章节合并到生产准备的 Observability 文档。历史版本继续保留各自内容。仅更新当前版本时运行 `python3 scripts/sync-boot-docs.py --version latest`。

Macula Cloud 的管理端与后端同仓，入口为 `macula-cloud/macula-cloud-admin`。首页管理端链接指向该目录。latest 的快速开始、平台部署与 Sentinel 指引设置 `manual_content: true`，按当前源码维护；跨仓库资料使用 `source_repository`、`source_branch`、`source_commit` 和 `source_paths` 记录来源，后续同步不会覆盖这些说明。

3.1、4.0 分别独立维护在 `content/zh-cn/docs/3.1/`、`content/zh-cn/docs/4.0/`，保留各自历史目录结构，直接从顶部版本菜单进入，不再嵌套或复制到其他版本中。它们在版本配置中标记为 `archived: true`，同步工具会跳过历史版本。原始 `/docs/98_old/<版本>/` 及曾使用的 `/docs/<5.x|6.0.x|latest>/98_old/<版本>/` 章节地址均跳转到独立历史文档；旧图片地址通过 Hugo 静态挂载保留。原有“历史文档”目录入口跳转到 4.0 首页。

同步工具只读取 Git 已提交内容，不切换或修改 Boot 工作区。`scripts/sync-boot-docs.py` 中的 `MAPPING` 将分支 README 映射到已有章节或 `EXTRA_CHAPTERS` 显式声明的独立组件页；已有章节保留 5.x 的标题、导航名和排序，新增组件页单独维护标题与排序。同步页记录来源分支、提交和文件路径，编辑链接指向对应 Boot 分支。

暂无对应分支资料的章节沿用 5.x 内容并明确标注尚未核对，历史归档保持原文。执行同步会重新生成 6.0.x 和 latest 文档；人工修订应同步维护生成规则。生成器会检查文件路径符合基础章节与显式组件页声明，不会为新模块自动添加新的栏目，也不应将组件说明混入栏目首页。文档快照随官网保存，构建及部署无需再次访问 Boot 仓库。

人工编写的版本专属章节可在 Front Matter 中设置 `manual_content: true`，同步工具会完整保留该页面。6.0.x 与 latest 的“运维指引 → 升级指南”分别记录从 5.x、6.0.x 升级的步骤、分支对照提交和参考源码；它们不是某一份 README 的直接副本。latest 概述同步时会移除 README 中“从 6.0 升级到 6.1”的详细迁移章节，仅保留指向统一升级指南的入口。后续分支升级说明变化时，应同步维护对应指南及此提取规则。

历史版本名称与正式路径统一不带 `v` 前缀，原 `/docs/v3.1/`、`/docs/v4.0/` 及其章节地址保留跳转，图片等资源地址继续可用。
