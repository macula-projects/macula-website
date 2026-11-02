# AGENTS.md

本文件适用于 `macula-website` 全仓库，记录用户在官网维护中已经确认的约定。后续修改应遵守这些约定，避免重复询问已确认的问题。用户当前明确指示优先；同一问题以较新的确认结果为准，不恢复已被纠正的旧方案。

## 开始工作

- 先检查 `git status --short`，保留已有修改，不覆盖、清理或回退用户的工作。
- 先读目标页面、相关同步脚本和实际来源，再修改。用 `rg` / `rg --files` 定位，不无目的扫描其他仓库。
- 本仓库是官网与文档，不因修改文档而改动 Macula Boot、Macula Cloud 或 Samples 的实现，也不启动它们的服务、容器或发布脚本。
- 调整内容结构前，先列清原有功能、图片、代码示例和链接的去向；整理后逐项核对。压缩文字不等于删减能力。
- README 介绍项目与维护命令，本文件约束维护行为。发现两者与用户最新决定不一致时，同步修正相关说明，不保留相互矛盾的约定。

## 文档版本与目录

- 文档版本为 `latest（当前）`、`5.x`、`4.0`、`3.1`，展示名称不加 `v`。
- `latest` 对应 Macula Boot `main`，`5.x` 对应同名分支。`6.0.x` 未正式发布，不维护独立文档版本，不重新加入版本菜单或同步目标。来源映射见 `data/doc_versions.json`。
- 版本切换放在文档顶部，不显示“文档版本”几个字。官网首页不区分版本，博客等公共内容不复制成多个版本。
- 切换版本时，目标版本存在相同章节则保留章节，否则进入目标版本首页；左侧目录只展示当前版本。
- `5.x`、`latest` 保持相同的基础栏目层级，以 `5.x` 为基准。分支新增组件通过同步脚本显式声明，不按源码模块路径另造一套目录。
- `3.1`、`4.0` 独立放在各自版本目录，通过顶部切换进入，保留历史结构。维护旧路径跳转和图片地址，不重新嵌套回 `98_old`。
- 历史版本按各自分支维护。只修改当前文档时，不将 main 的内容或配置覆盖到旧版本。

## 首页、栏目页与内容归属

- **开发指引首页和微服务首页不写说明正文，只保留标题与自动生成的章节目录。** 不添加阅读顺序、配置表、依赖示例、迁移说明或重复导览。
- 其他栏目首页只承担分类导览；具体组件的说明放在独立组件页。特别是 `Commons.md` 必须独立，不能把 Commons README 填入“框架基础”的 `_index.md`。
- 微服务依赖选择与配置分别归入 Alibaba、Tencent、Gateway 等模块；TSF 移除说明放在升级指南，不写回微服务首页。
- latest 的升级指南直接介绍 `5.x → latest`，整合 Java/Jakarta 与最新框架变更，不要求先升级到未发布的中间版本。详细升级内容放在“运维指引 → 升级指南”，概述保留简短入口。
- Web 的“授权列表的资源凭证扩展”放在“核心功能 → 全局返回结构处理”下，作为其子节，不得落在版权说明之后。
- 移动章节时检查旧链接、页内锚点与同步逻辑，避免重新生成后恢复旧位置。

## 组件文档统一结构

`5.x`、`latest` 的组件页统一使用以下六个二级标题，按此顺序排列：

1. 概览
2. 组件坐标
3. 使用配置
4. 核心功能
5. 依赖引入
6. 版权说明

功能细分使用三级及以下标题。不要为凑结构删除原有功能、重写代码块或把功能追加到版权之后。归档版本保持原貌。

## 快速开始与开发指引

### 快速开始

- 以最短可运行流程为主：**下载并启动 Macula Cloud → 下载 Macula Boot 并运行 `macula-boot-examples` → 调用一个接口验证**。
- 简要介绍 Gateway、Consumer（BFF）、Provider（Service）的职责与调用方向即可。不要把快速开始重新写成详细配置手册。
- 简述三个配置方向：Gateway 验证 IAM Token；Consumer/BFF 用 Cloud endpoint 和应用凭据获取菜单、用户信息；Consumer、Provider 等非网关后端用应用网关的 `jwk-set-uri` 验证内部 JWT。
- 启动命令、端口、环境变量和验证接口必须对照当前 README、配置与脚本。区分免认证连通测试和真实认证验证，不能将前者称为完成认证验收。
- 详细认证配置链接到安全架构及对应模块，IDE 启动和更多示例链接到 Examples README。
- 快速开始末尾简要介绍 Archetype 创建自有单仓项目，提供可核对的模板安装、生成命令及必要参数；区分业务 `version` 与模板 `archetypeVersion`，详细说明链接到 Archetype README 和开发指引。

### 开发指引

- 主线以 [GitHub macula-samples](https://github.com/macula-projects/macula-samples) 的**单仓模式**为准，模块是同一仓库内的目录。
- “开发环境准备 → 获取源码”同时简要提及可用 Archetype 创建自己的项目，生成命令统一链接到快速开始的 Archetype 小节。
- 多仓模式只在“开发环境准备 → 获取源码”附近简要提及，并链接 [macula-samples-workspace](https://cnb.cool/macula-projects/macula-samples-workspace)。不要放在开发指引首页，也不展开多仓管理教程。
- 获取源码、模块结构、运行测试和部署步骤统一使用单仓的真实文件与命令。不要混入多仓 `repo.sh` 流程。
- “运行与测试”介绍 Samples；Examples 的启动说明放在快速开始，不能用 Examples README 覆盖 Samples 指引。
- 开发指引覆盖模块职责、`application.yml` 的组织规范、profile、Nacos、运行测试与部署；业务开发要交代应用分层及跨服务 API 契约。
- 区分 Java/IDE、Compose、Vite 对 `.env` 的读取方式，以及本机、容器、浏览器使用的地址；属性前缀以各模块的真实绑定代码为准，不机械统一。
- Macula Cloud 后端和管理端同仓，管理端位于 `macula-cloud/macula-cloud-admin`。不要重新链接已废弃的独立 `macula-cloud-admin` 仓库。

## 应用分层与原有资料保留

- “后端开发规范 → 应用分层”是通用规范，不写“Samples 阅读入口”，末尾可用“相关指引”。
- 保留原有架构图、工程目录图和模型传递图，整理文字时不得漏掉：
  - `content/zh-cn/docs/latest/03_devrules/后端开发规范/images/model-small.png`
  - `content/zh-cn/docs/latest/03_devrules/后端开发规范/images/structure.png`
  - `content/zh-cn/docs/latest/03_devrules/后端开发规范/images/layer-model.png`
  - `content/zh-cn/docs/latest/03_devrules/后端开发规范/images/model2.png`
- 说明 Controller、Service、Mapper、Converter 的职责，Query、Form、DTO、VO、BO、Entity 的语义，以及 BFF、业务服务和 API 契约的边界。
- “平台简介 → 值对象与分层”以原有 `layer-model.png`、`model2.png` 两图为主，概要说明命名、服务内传递和跨服务转换；复用原图并保留放大查看，详细规范仍在应用分层章节。稳定 API 契约可包含 Query/Form/VO，不强制跨服务全部改成 DTO，也不要求每层机械复制对象。
- 经典三层是可选的基础组织方式，不将某一示例工程的做法写成 Macula 强制的唯一架构。

## Gateway、安全与生产准备

- **Gateway 不能只介绍安全。** 对照 README 保留完整能力：HTTP/WebSocket 路由、入口认证授权、内部 JWT、接口加解密与签名、CryptoService、System Redis、Token 缓存管理、Trace ID 与灰度标签。
- Gateway 组件页直接说明组件的接入和使用，使用通用服务名及环境变量，不引入 `macula-boot-examples` 或 Samples 的工程操作步骤。
- “平台简介 → 安全架构”单独概要介绍分层安全并配原理图：外部 Token、AK/SK、API Key → Gateway 认证与入口权限 → 内部 JWT → BFF/微服务验签与细粒度授权。
- 讲清网关的登录认证、角色、菜单与 URL 权限，以及内层通过 `SecurityUtils` 获取上下文、通过 `@PreAuthorize`、`@PostAuthorize`、`@CheckOwner` 进一步授权的区别。
- 不把 AK/SK、API Key 应用身份写成登录用户身份，不声称它们自动具有用户角色；具体权限路径按实际实现说明。
- 不混淆 IAM introspection、Macula Cloud Gateway endpoint、应用 Gateway JWK 地址。
- 原理图附近简述相关关键配置和方向；完整参数、协议及细节放在 Gateway、Security、System 等组件页，避免概述过度膨胀。
- `@CheckOwner` 的返回后归属检查与执行前 Passkey 校验分别解释，不能把资源凭证当作列表过滤、按钮权限或租户数据范围的替代。变更说明时核对当前注解和实现。
- 生产准备包含 **Observability**，说明指标、链路、日志及其配置；不能只剩审计，也不能将已删除的旧可观测性 Starter 作为 main 的当前方案。

## 来源、同步与变更历史

- 内容以目标分支**已提交源码**为依据；读 README 时同时检查相关 POM、配置绑定和必要实现。不能只凭模块名称或历史描述推断能力。
- 核对 main 中实际存在的模块，删除模块不从 5.x 自动回填；保留历史版本说明和适当的旧链接跳转。
- 使用 Front Matter 的 `source_path` / `source_paths`、`source_branch`、`source_commit` 记录可追溯来源；跨仓库时补充 `source_repository`、必要的 `source_refs`。这些是元数据，不写入正文，不显示给读者。
- 每个来源路径必须存在于所记录提交。不能给来自多个仓库的文件冒用同一个仓库或提交，也不能用工作区未提交的扩展作为已发布文档依据。
- 同步脚本只读 Boot 的已提交内容，不切换、清理或修改其工作区。人工维护页使用 `manual_content: true`，并核对同步后仍保留内容。
- 修改生成页面时同时处理同步规则或人工维护标记，防止下次同步覆盖修订。大范围同步先在临时副本比较，避免将无关分支更新混入本次修改。
- 变更历史依据 Macula Boot **GitHub Releases**：直接使用 Release 版本号，提供简短功能/修复摘要，详情链接到原 Release；不把 main 未发布内容写成正式版本变更。
- 6.0 系列保留 Release 历史，统一标注“不建议使用”，不重新建立独立文档版本。人工使用建议放在 `data/release_advisories.json`，展示时优先于普通发布状态标签，不修改 GitHub 来源数据，也不让每日同步覆盖该标注。
- Release 数据共用 `data/boot_releases.json`；保留版本筛选、预发布标记、北京时间日期和同步失败保留旧快照的行为。

## 视觉、排版与阅读

- 整体采用简洁、专业的技术官网风格；首页、博客、文档、导航、目录和变更历史使用统一字体体系。
- 品牌名使用大写 **MACULA**，字标采用用户最终认可的宽厚几何字形。复用现有 SVG，不重新换成狭窄、细长的字体；Logo、字标、正文强调色与按钮保持同色系协调。
- 当前确认基准：正文 PC **15px**、移动端 **14px**；导航/目录 14px；表格和代码 PC 14px、移动端 13px。这是用户反馈正文过大后的结果，不恢复早先试过的 PC 16px。具体实现使用共享变量和相对单位。
- 文档左右导航靠浏览器两侧，正文居中、自适应，最大约 960px；参考 Dubbo 的侧栏布局与 OSCHINA 的阅读密度，不把整个文档区域挤进窄居中容器。
- 表格首列保留可读的完整标签，宽表在自己的可键盘操作区域滚动；避免反复换行，也不让宽表或代码撑宽整个页面。
- 左侧目录只让 `.td-sidebar-nav` 承担滚动，搜索框保持定位。保留可辨识的层级缩进、展开/收起按钮与当前页状态，不能出现双滚动条或扁平化目录。
- 安全原理图的字体跟正文/代码变量一致，保持 720px 原生画布，宽屏不放大字体；窄屏在图内横向滚动。
- 保留图片说明、放大查看、键盘操作、焦点状态和移动端目录能力。样式调整不要顺带改写不同版本的正文。

## 构建、验证与交付

- 构建工具版本以 README、锁文件、`.nvmrc`、`go.mod` 及工作流的实际配置为准；更新 Hugo/Docsy 时同时检查本地、GitHub Pages 与 Netlify。
- 使用 `npm ci`、`npm run dev`、`npm run build`。Dart Sass 来自 npm 依赖；直接执行 Hugo 时需将 `node_modules/.bin` 加入 PATH，不能把缺少 Sass 误判为页面内容问题。
- Hugo 构建不接受 deprecated 警告或已移除接口。升级后核对配置键、模块挂载、模板路径和内部模板，不恢复旧 `includeFiles`、旧 analytics 模板或旧 artifact action。
- 修改 `content/`、模板、样式或构建配置后运行 `npm run build`；修改同步逻辑后运行 `python3 -m unittest discover -s scripts/tests -v`，并做相关同步比较。
- 按改动验证实际结果：页面归属与锚点、图片加载、版本切换、桌面/手机宽度、目录层级及滚动。代码或样式变化需要浏览器检查；纯维护规则文档不必启动网站或后端。
- 不提交 `public/`、`resources/` 等生成物、凭据或本地环境文件。提交前检查差异，只包含当前任务及用户已明确允许合并的修改。
- 提交、推送沿用当前会话已有明确授权；不能把本文件本身当作永久发布授权。获得构建推送授权后完成提交与推送，若声称已上线，必须确认对应提交的构建和部署均成功。
- 完成时简要说明修改结果、验证情况和必要的限制；不以“准备做”“可以继续”替代已经要求完成的工作。
