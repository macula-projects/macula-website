# Macula 官网与文档

基于 Hugo 和 Docsy，包含项目官网、版本化文档、博客与变更历史。维护约定见 [AGENTS.md](AGENTS.md)。

## 本地开发

环境：Hugo Extended **0.169.0**、Node.js **24 LTS**、Go **1.24+**；Docsy **0.18.1** 由 Hugo Modules 管理。

```bash
nvm use
npm ci
npm run dev
```

构建静态网站：

```bash
npm run build
```

Dart Sass 随 npm 依赖安装。请使用上述命令，避免直接运行 Hugo 时找不到 Sass；Hugo 安装见[官方说明](https://gohugo.io/installation/)。

## 内容位置

- `content/zh-cn/`：首页、文档和博客。
- `layouts/`、`assets/`、`static/`：模板、样式、脚本和静态资源。
- `data/`、`scripts/`：版本映射、Release 数据与同步工具。

## 文档版本与同步

文档维护 `latest`、`5.x`、`4.0`、`3.1`；latest 对应 Macula Boot main，4.0 和 3.1 为归档。映射见 [data/doc_versions.json](data/doc_versions.json)。

更新 latest 的来源文档：

```bash
python3 scripts/sync-boot-docs.py --version latest --boot-repo ../macula-boot
```

同步只读取 Boot 分支的已提交内容。先在临时副本比较差异；标记 `manual_content: true` 的人工页面会保留，新增章节需登记同步映射。

更新 GitHub Releases 快照：

```bash
npm run sync:releases
```

## 验证

修改内容后运行 `npm run build`；修改同步逻辑时另运行：

```bash
python3 -m unittest discover -s scripts/tests -v
```

修改页面交互后检查桌面与手机显示，搜索逻辑可运行 `node --test scripts/tests/site-search.test.cjs`。不提交生成的 `public/`、`resources/` 或本地环境文件。
