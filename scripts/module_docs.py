"""Keep component documentation in six editorial sections without changing examples."""
import re
import xml.etree.ElementTree as ET

SECTIONS = ('概览', '组件坐标', '使用配置', '核心功能', '依赖引入', '版权说明')
ALIASES = {'概述': '概览', '使用说明': '使用配置', '引入依赖': '组件坐标',
           '自动启用与配置': '使用配置', '功能特性': '核心功能'}


def pom_defaults(poms):
    """Read actual Maven coordinates and direct, non-test dependencies at a source ref."""
    coordinates, dependencies = [], []
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    for text in poms:
        root = ET.fromstring(text)
        artifact = root.findtext('m:artifactId', namespaces=ns)
        group = (root.findtext('m:groupId', namespaces=ns)
                 or root.findtext('m:parent/m:groupId', namespaces=ns))
        if artifact and group:
            coordinates.append((group, artifact))
        for dep in root.findall('m:dependencies/m:dependency', ns):
            if dep.findtext('m:scope', namespaces=ns) == 'test':
                continue
            pair = (dep.findtext('m:groupId', namespaces=ns), dep.findtext('m:artifactId', namespaces=ns))
            if all(pair) and pair not in dependencies:
                dependencies.append(pair)

    def xml(items):
        return '\n\n'.join('```xml\n<dependency>\n'
            f'    <groupId>{group}</groupId>\n    <artifactId>{artifact}</artifactId>\n'
            + '</dependency>\n```' for group, artifact in dict.fromkeys(items))

    return {
        '组件坐标': xml(coordinates),
        '依赖引入': ('以下为对应分支 POM 的直接依赖（不含测试依赖）；版本由父 POM / BOM 管理。\n\n'
                 + xml(dependencies)) if dependencies else '',
    }


def place_web_response_extension(body):
    """Keep the list-passkey extension inside response processing, including old READMEs."""
    extension = re.search(r'(?m)^#{3,4} 授权列表的资源凭证扩展\s*$', body)
    response = re.search(r'(?m)^### 全局返回结构处理\s*$', body)
    if not extension or not response:
        return body
    next_response = re.search(r'(?m)^#{1,3} ', body[response.end():])
    response_end = response.end() + next_response.start() if next_response else len(body)
    if response.end() <= extension.start() < response_end:
        return body
    level = len(extension[0].split(' ', 1)[0])
    next_extension = re.search(r'(?m)^#{1,' + str(level) + r'} ', body[extension.end():])
    extension_end = extension.end() + next_extension.start() if next_extension else len(body)
    text = re.sub(r'^#{3,4} ', '#### ', body[extension.start():extension_end].strip(), count=1)
    remaining = body[:extension.start()].rstrip() + '\n\n' + body[extension_end:].lstrip()
    response = re.search(r'(?m)^### 全局返回结构处理\s*$', remaining)
    next_response = re.search(r'(?m)^#{1,3} ', remaining[response.end():])
    insert_at = response.end() + next_response.start() if next_response else len(remaining)
    result = remaining[:insert_at].rstrip() + '\n\n' + text + '\n\n' + remaining[insert_at:].lstrip()
    return result.rstrip() + '\n'


def normalize_module(body, defaults=None, component=''):
    """Group headings while preserving fenced code and all original prose.

    Nested client sections and multiple source READMEs share one set of top-level
    headings. Existing canonical pages remain byte-stable on a second pass.
    """
    defaults = dict(defaults or {})
    if component == 'Web':
        body = place_web_response_extension(body)
    if component in {'Gateway', 'Security'} and '## 组件坐标' not in body:
        body = body.replace('## 职责与接入', '## 概览').replace('## 内层安全的职责', '## 概览')
        body = body.replace('```xml', '## 组件坐标\n\n```xml', 1)
        for title in ('Token：对接 IAM', 'JWT 验签配置'):
            body = body.replace('## ' + title, '## 使用配置\n\n### ' + title)
        for title in ('AK/SK：应用 HMAC 认证', 'SecurityUtils：读取认证上下文'):
            body = body.replace('## ' + title, '## 核心功能\n\n### ' + title)
    if component == 'Async' and '## 核心功能' not in body:
        body = body.replace('### `@Async` 上下文传播', '## 核心功能\n\n### `@Async` 上下文传播')
    if component == 'Observability' and '## 核心功能' not in body:
        body = body.replace('### 结构化日志与日志导出', '## 核心功能\n\n### 结构化日志与日志导出')
    if component == 'Commons':
        body = body.replace('# Macula Boot Commons', '## 概览', 1)
        defaults['使用配置'] = 'Commons 提供公共数据结构与工具契约，无独立 YAML 配置项；按下文接口在业务代码中使用。'
    if component == 'Mapstruct':
        defaults['使用配置'] = '该组件在编译期生成转换代码，无独立运行时 YAML 配置。继承 Macula Boot 父 POM 的注解处理配置，并在 IDE 启用注解处理；具体写法见“核心功能”。'
    if component == 'IAM':
        defaults['组件坐标'] = 'IAM 为独立部署的平台服务。应用通过网关的 OAuth2 Resource Server 接入，配置方式见下节；不存在独立的 IAM Starter 坐标。'
        defaults['依赖引入'] = '网关侧通过 OAuth2 Resource Server 验证外部 Token；使用 Macula Gateway 组合 Starter 接入。IAM 服务端单独部署，不作为业务服务的库依赖。'
    configurations = {
        'Dubbo': '本模块沿用 Dubbo 的 `dubbo.*` 配置，设置应用名、注册中心和服务协议；具体属性与接入方式见下文。',
        'Statemachine': '状态流转通过 Java DSL 定义，无独立 YAML 配置项。业务负责状态持久化、事务与并发控制，规则定义见“核心功能”。',
        'Retry': '通过方法上的重试注解声明重试次数、异常与退避策略，具体用法见“核心功能”。',
        'Metrics': '通过 Actuator 暴露指标，按环境配置端点与指标采集端；具体接入说明见“核心功能”。',
        'WebSocket': '该分支 README 未提供独立配置示例；接入时核对该分支的 WebSocket 自动配置、STOMP 端点与 Redis 连接配置。',
        'Async': '沿用 Spring 异步线程池配置；TTL 装饰器与显式 Executor 的使用方式见“核心功能”。',
    }
    if component in configurations:
        defaults['使用配置'] = configurations[component]
    if component == 'Async':
        defaults['概览'] = '本模块为异步任务提供线程上下文传播。该分支使用 Alibaba TTL，`@Async` 与显式异步调用的接入方式如下。'
    features = {
        'Loggers': '通过 Logback 配置日志输出和 Logstash 集成；格式、输出位置与 Appender 配置见“使用配置”。',
        'Auditing': '通过审计注解触发日志事件，应用可监听事件并保存审计记录，具体示例见“使用配置”。',
        'WebSocket': '支持基于 STOMP 的 WebSocket 通信，并通过 Redis Pub/Sub 在多个应用实例之间传递消息。',
    }
    if component in features:
        defaults['核心功能'] = features[component]
    buckets = {name: [] for name in SECTIONS}
    current = '概览'
    fence = None
    source_level = 2
    demoted_group = False
    for line in body.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            value = marker[1]
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            buckets[current].append(line)
            continue
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line) if fence is None else None
        if not heading:
            # A source separator has no meaning after the sources share sections.
            if fence is not None or line.strip() != '---':
                buckets[current].append(line)
            continue
        level, title = len(heading[1]), heading[2]
        canonical = ALIASES.get(title, title)
        if canonical in SECTIONS:
            current, source_level = canonical, level
            demoted_group = False
            continue
        if title == '版本说明' and current == '依赖引入':
            # Older READMEs use this label for third-party license attribution.
            current, source_level = '版权说明', level
            demoted_group = False
            continue
        if level == 1:
            # Source README title; the page title is already rendered by Hugo.
            current, source_level = '概览', 2
            demoted_group = False
            continue
        if title in {'生产者配置建议', '消费者配置建议', '基于springboot使用dubbo'}:
            current, source_level = '使用配置', max(2, level - 1)
            demoted_group = False
        if title in {'使用 Spring Cache 注解', 'SnailJob 原生任务', '兼容旧 XXL Handler',
                     'dubbo与spring cloud互通', 'Macula 额外扩展'}:
            current, source_level = '核心功能', max(2, level - 1)
            demoted_group = False
        if level <= 2:
            if title in {'客户端接入', '客户端使用', '客户端介绍'}:
                current, source_level = '使用配置', 2
                demoted_group = False
                continue
            if title in {'前置条件', '启动', '配置与启动'}:
                current, source_level = '使用配置', 2
            elif current in {'概览', '组件坐标', '版权说明'} or title == '服务端介绍' or (
                    current == '使用配置' and not any(word in title for word in ('配置', '启动', '接入'))):
                current, source_level = '核心功能', 2
            demoted_group = True
        # Child headings remain below the six canonical sections.
        nested = max(3, min(6, level + 2 - source_level + (1 if demoted_group and level > 2 else 0)))
        buckets[current].append('#' * nested + ' ' + title)

    fallbacks = {
        '概览': '本页介绍该组件的接入配置、主要能力及依赖关系。',
        '组件坐标': '本能力通过所属 Starter 接入，具体集成依赖见下文。',
        '使用配置': '先完成组件依赖接入；相关 API 与集成方式见“核心功能”。',
        '核心功能': '组件的接入流程与使用示例见“使用配置”。',
        '依赖引入': '在应用中引入上述组件坐标；具体依赖以对应分支的模块 POM 为准。',
        '版权说明': 'Macula Boot 使用 [Apache License 2.0](https://github.com/macula-projects/macula-boot/blob/main/LICENSE)。第三方组件遵循各自许可证。',
    }
    parts = []
    for name in SECTIONS:
        text = '\n'.join(buckets[name]).strip()
        if not text:
            text = defaults.get(name) or fallbacks[name]
        parts.append('## ' + name + '\n\n' + text)
    return '\n\n'.join(parts) + '\n'
