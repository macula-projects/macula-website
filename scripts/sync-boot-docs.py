#!/usr/bin/env python3
"""Sync branch content into shared categories with explicit component pages."""
import argparse
import json
import posixpath
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote, urlsplit

SITE = Path(__file__).resolve().parents[1]
DOCS = SITE / 'content/zh-cn/docs'
REMOTE = 'https://github.com/macula-projects/macula-boot'

# Editorial categories are shared across releases; repository paths are sources only.
EXTRA_CHAPTERS = {
    '01_services/框架基础/Commons.md': {
        'title': 'Macula Boot Commons', 'linkTitle': 'Commons', 'weight': -1,
    },
    '01_services/框架基础/Async.md': {
        'title': 'Macula Boot Starter Async', 'linkTitle': 'Async', 'weight': 0,
    },
}

MAPPING = {
    'README.md': '00_introduce/概述/_index.md',
    'macula-boot-archetype': '04_devmanual/创建应用平台.md',
    'macula-boot-commons': '01_services/框架基础/Commons.md',
    'macula-boot-examples': '04_devmanual/运行与测试.md',
    'docker': '04_devmanual/打包部署.md',
    'docs/migration/unified-observability.md': '05_ops/升级指南/_index.md',
}
for category, modules in {
    '框架基础': {'async': 'Async', 'web': 'Web', 'cache': 'Cache', 'crypto': 'Crypto',
              'jpa': 'DataJpa', 'kafka': 'Kafka', 'mapstruct': 'Mapstruct',
              'mybatis-plus': 'MyBatisPlus', 'redis': 'Redis', 'rocketmq': 'RocketMQ',
              'security': 'Security', 'springdoc': 'Springdoc'},
    '框架扩展': {'binlog4j': 'Binlog4j', 'idempotent': 'Idempotent', 'leaderelection': 'Leaderelection',
              'liteflow': 'LiteFlow', 'lock4j': 'Lock4j', 'oss': 'OSS', 'springretry': 'Retry',
              'sender': 'Sender', 'statemachine': 'Statemachine', 'websocket': 'WebSocket', 'wechat': 'Wechat'},
    '微服务': {'cloud': '_index', 'cloud-alibaba': 'Alibaba', 'cloud-alibaba-gray': 'Alibaba',
             'cloud-alibaba-scg': 'Alibaba', 'cloud-tencent-scg': 'Tencent',
             'cloud-gateway': 'Gateway', 'cloud-tencent': 'Tencent',
             'cloud-tsf': 'TSF', 'cloud-tsf-scg': 'TSF', 'dubbo': 'Dubbo', 'feign': 'Feign'},
    '生产准备': {'auditlog': 'Auditing', 'operationlog': 'Auditing', 'observability': '_index',
              'logstash': 'Loggers', 'prometheus': 'Metrics', 'skywalking': 'Tracing', 'sleuth': 'Tracing'},
    '通用平台': {'seata': 'Seata', 'system': 'System', 'task': 'Task', 'tinyid': 'ID'},
}.items():
    for module, chapter in modules.items():
        MAPPING['macula-boot-starter-' + module] = f'01_services/{category}/{chapter}.md'


def split_page(text):
    match = re.match(r'\s*---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('Missing chapter front matter')
    header = re.sub(r'^aliases:.*\n?', '', match[1], flags=re.M)
    return header, text[match.end():].lstrip('\n')


def url(version, chapter):
    path = chapter[:-len('_index.md')] if chapter.endswith('_index.md') else chapter[:-3] + '/'
    return f'/docs/{version}/{path.lower()}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boot-repo', type=Path, default=SITE.parent / 'macula-boot')
    parser.add_argument('--version', action='append', help='Sync only this version; may be repeated')
    args = parser.parse_args()
    versions = json.loads((SITE / 'data/doc_versions.json').read_text())
    sync_versions = {v['id'] for v in versions if v.get('branch') and v['id'] != '5.x'}
    if args.version and not set(args.version) <= sync_versions:
        parser.error(f'Versions available for sync: {", ".join(sorted(sync_versions))}')

    def git(*arguments):
        return subprocess.check_output(['git', '-C', str(args.boot_repo), *arguments], text=True).strip()

    template = DOCS / '5.x'
    template_files = {p.relative_to(template) for p in template.rglob('*')
                      if p.is_file() and not p.name.startswith('.')}
    for version in versions:
        if version['id'] == '5.x' or version.get('archived'):
            continue
        if args.version and version['id'] not in args.version:
            continue
        branch = version['branch']
        commit = git('rev-parse', branch)
        tree = git('ls-tree', '-r', '--name-only', commit).splitlines()
        starter_modules = {Path(p).parent.name for p in tree
                           if p.startswith('macula-boot-starters/') and p.endswith('/pom.xml')}
        starter_modules.discard('macula-boot-starters')
        unknown = starter_modules - MAPPING.keys()
        if unknown:
            raise ValueError(f'Starters need an explicit chapter mapping: {sorted(unknown)}')
        removed_chapters = set()
        if version['id'] == 'latest':
            # Preserve categories, but never reintroduce a removed Starter from the 5.x template.
            owners = defaultdict(set)
            for module, chapter in MAPPING.items():
                if module.startswith('macula-boot-starter-'):
                    owners[Path(chapter)].add(module)
            removed_chapters = {chapter for chapter, modules in owners.items()
                                if not chapter.name.startswith('_index') and not modules & starter_modules}
        expected_files = (template_files | {Path(path) for path in EXTRA_CHAPTERS}) - removed_chapters
        retired_aliases = defaultdict(list)
        for chapter in sorted(removed_chapters):
            retired_aliases[(chapter.parent / '_index.md').as_posix()].append(url(version['id'], chapter.as_posix()))
        sources = [p for p in tree if p == 'README.md'
                   or (p.startswith('macula-boot-') and p.endswith('/README.md') and '/src/' not in p)
                   or (p.startswith('docs/') and p.endswith('.md'))]

        def chapter_for(source):
            if source == 'README.md' or source.startswith('docs/'):
                return MAPPING[source]
            module = Path(source).parent.name
            if module.startswith('macula-example-'):
                if module == 'macula-example-binlog4j':
                    return '01_services/框架扩展/Binlog4j.md'
                if module == 'macula-example-task':
                    return '01_services/通用平台/Task.md'
                return '04_devmanual/运行与测试.md'
            return MAPPING[module]

        chapters = defaultdict(list)
        for source in sources:
            chapter = chapter_for(source)
            if Path(chapter) not in expected_files:
                raise ValueError(f'Chapter is not in the shared layout or explicit additions: {chapter}')
            chapters[chapter].append(source)
        observability = next((p for p in sources if p.endswith('macula-boot-starter-observability/README.md')), None)
        if observability and version['id'] != 'latest':
            for name in ['Loggers', 'Metrics', 'Tracing']:
                chapters[f'01_services/生产准备/{name}.md'].append(observability)
        routes = {p: url(version['id'], chapter_for(p)) for p in sources}
        routes.update({posixpath.dirname(p): routes[p] for p in sources if p.endswith('/README.md')})

        def render(source):
            content = git('show', f'{commit}:{source}') + '\n'
            if version['id'] == 'latest' and source == 'README.md':
                # Keep migration details in the dedicated, manually maintained guide.
                content = re.sub(r'(?ms)^## 从 6\.0 升级到 6\.1\n.*?(?=^## |\Z)', '', content)
                content = content.replace('[统一可观测性迁移指南]', '[从 6.0.x 迁移到 latest 的升级指南]')

            def rewrite(match):
                image, label, destination = match.groups()
                if version['id'] == 'latest' and destination == 'https://github.com/macula-projects/macula-cloud-admin':
                    destination = 'https://github.com/macula-projects/macula-cloud/tree/main/macula-cloud-admin'
                    return f'{image}[{label}]({destination})'
                parts = urlsplit(destination)
                if parts.scheme or parts.netloc or destination.startswith(('#', '/')):
                    return match.group(0)
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), parts.path))
                target = routes.get(resolved) or routes.get(resolved.rstrip('/') + '/README.md')
                if image or not target:
                    kind = 'raw' if image else 'blob'
                    target = f'{REMOTE}/{kind}/{commit}/{quote(resolved)}'
                if parts.fragment:
                    target += '#' + parts.fragment
                return f'{image}[{label}]({target})'

            parts = re.split(r'(^```.*?$.*?^```[^\n]*$|^~~~.*?$.*?^~~~[^\n]*$)', content, flags=re.M | re.S)
            return ''.join(part if i % 2 else re.sub(
                r'(!?)\[([^\]\n]*)\]\(([^\s)]+)\)', rewrite, part
            ) for i, part in enumerate(parts))

        root = DOCS / version['id']
        for chapter in removed_chapters:
            previous = root / chapter
            if previous.exists():
                previous_header, _ = split_page(previous.read_text())
                if re.search(r'^manual_content:\s*true\s*$', previous_header, re.M):
                    raise ValueError(f'Removed Starter has a manual page; relocate it first: {previous}')
                previous.unlink()
        # Remove only pages owned by the previous generator; preserve unexpected files.
        for previous in root.rglob('*'):
            if not previous.is_file() or previous.relative_to(root) in expected_files:
                continue
            if previous.suffix == '.md' and any(marker in previous.read_text() for marker in (
                    '\nsource_path:', '\nsnapshot_generated:')):
                previous.unlink()
            else:
                raise ValueError(f'Unexpected file; relocate it manually: {previous}')
        for directory in sorted(root.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()

        for relative in sorted(expected_files):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.suffix == '.md' and target.exists():
                current_header, _ = split_page(target.read_text())
                if re.search(r'^manual_content:\s*true\s*$', current_header, re.M):
                    continue
            if relative.suffix != '.md':
                shutil.copyfile(template / relative, target)
                continue
            path = relative.as_posix()
            if path in EXTRA_CHAPTERS:
                header = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}'
                                   for key, value in EXTRA_CHAPTERS[path].items())
                body = ''
            else:
                header, body = split_page((template / relative).read_text())
            if path in retired_aliases:
                header += '\naliases: ' + json.dumps(retired_aliases[path], ensure_ascii=False)
            page_sources = chapters.get(path, [])
            if page_sources:
                body = '\n\n---\n\n'.join(render(source) for source in page_sources)
                metadata = {'source_path': page_sources[0], 'source_paths': page_sources,
                            'source_branch': branch, 'source_commit': commit}
                header += '\n' + '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}'
                                           for key, value in metadata.items())
            elif body.strip() and path != '_index.md':
                body = (f"> 本章沿用 5.x 的文档内容，尚未按 {version['label']} 分支核对。"
                        f"涉及依赖、配置或 API 时，请以 [{branch} 分支源码]({REMOTE}/tree/{branch}) 为准。\n\n" + body)
            if path == '01_services/框架基础/_index.md':
                body = '框架基础组件按职责独立成篇。请从下方目录选择 Commons、Async、Web、数据访问、缓存等组件。\n'
            if version['id'] == 'latest' and path == '01_services/微服务/_index.md':
                body += ('\n\n## 已移除的 TSF 接入\n\n'
                         'main 已移除 `macula-boot-starter-cloud-tsf` 与 `macula-boot-starter-cloud-tsf-scg`。'
                         '当前云接入方式见上方 Alibaba、Tencent 与 Gateway 文档；'
                         '旧版 TSF 用法保存在 [5.x 历史文档](/docs/5.x/01_services/微服务/tsf/)。\n')
            if path == '_index.md':
                header = header.replace('docs_version: "5.x"', f'docs_version: "{version["id"]}"')
                header = header.replace('title: "Macula 5.x 文档"', f'title: "Macula {version["label"]} 文档"')
                # Retain the 5.x landing-page cards, fixing their obsolete links.
                header = header.replace('02_deploy/', '05_ops/')
                header = re.sub(r'^.*\[数据库开发规范\].*\n?', '', header, flags=re.M)
                header = header.replace('[前端开发手册](04_devmanual/前端开发手册)',
                                        '[创建应用平台](04_devmanual/创建应用平台)')
                header = header.replace('[后端开发手册](04_devmanual/后端开发手册)',
                                        '[创建服务模块](04_devmanual/创建服务模块)')
                header = header.replace('[开发示例](04_devmanual/开发示例)',
                                        '[运行与测试](04_devmanual/运行与测试)')
                body = (f"文档版本：**{version['label']}**，对应 Macula Boot **{branch}** 分支。\n\n"
                        '各版本保留相同栏目，组件章节以对应分支实际提供的模块为准。\n\n{{% docs/document_box %}}\n')
            target.write_text('---\n' + header + '\n---\n\n' + body)
        actual = {p.relative_to(root) for p in root.rglob('*') if p.is_file() and not p.name.startswith('.')}
        if actual != expected_files:
            raise ValueError(f'Layout differs from the declared chapters: {actual ^ expected_files}')
        print(f"{version['id']}: {len(template_files)} base files and {len(EXTRA_CHAPTERS)} component pages; "
              f'{len(removed_chapters)} retired chapters omitted; '
              f'{len(sources)} source documents mapped into {len(chapters)} chapters')


if __name__ == '__main__':
    main()
