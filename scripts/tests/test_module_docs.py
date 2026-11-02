import sys
import re
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from module_docs import SECTIONS, normalize_module, pom_defaults


class ModuleDocsTest(unittest.TestCase):
    def test_gateway_documents_all_its_capabilities(self):
        page = (Path(__file__).resolve().parents[2] /
                'content/zh-cn/docs/latest/01_services/微服务/Gateway.md').read_text()
        for heading in ('HTTP 与 WebSocket 路由', 'Token 的角色、菜单与 URL 权限',
                        'AK/SK：应用 HMAC 认证', 'API Key：平台应用身份', '转换为内部 JWT',
                        '接口加解密与签名', '独立 System Redis', 'Token 缓存移除',
                        'Trace ID 响应头', '灰度标签传递'):
            with self.subTest(capability=heading):
                self.assertIn('### ' + heading, page)
        for protocol in ('/gateway/protect/urls', '/gateway/protect/key',
                         'getSm2PublicKey()', 'decryptSm4Key(', 'HexUtil.decodeHex(sm4Key)',
                         'timestamp:', 'nonce:', 'signature:', 'protect-urls:', 'sysRedisTemplate'):
            with self.subTest(protocol=protocol):
                self.assertIn(protocol, page)

    def test_maintained_component_pages_use_six_sections(self):
        docs = Path(__file__).resolve().parents[2] / 'content/zh-cn/docs'
        for version in ('5.x', '6.0.x', 'latest'):
            for page in (docs / version / '01_services').rglob('*.md'):
                if page.name.startswith('_index'):
                    continue
                fence = None
                headings = []
                for line in page.read_text().splitlines():
                    marker = re.match(r'^\s*(`{3,}|~{3,})', line)
                    if marker:
                        value = marker[1]
                        if fence is None:
                            fence = value
                        elif value[0] == fence[0] and len(value) >= len(fence):
                            fence = None
                    elif fence is None and line.startswith('## '):
                        headings.append(line[3:])
                with self.subTest(page=str(page.relative_to(docs))):
                    self.assertEqual(headings, list(SECTIONS))

    def test_nested_client_sections_and_multiple_sources_are_grouped(self):
        source = ('## 概述\n\n客户端 A\n\n## 客户端接入\n\n### 组件坐标\n\n坐标 A\n'
                  '\n### 使用配置\n\n配置 A\n\n### 核心功能\n\n功能 A\n'
                  '\n## 概述\n\n客户端 B\n\n## 组件坐标\n\n坐标 B\n')
        result = normalize_module(source)
        headings = [line[3:] for line in result.splitlines() if line.startswith('## ')]
        self.assertEqual(headings, list(SECTIONS))
        for text in ('客户端 A', '客户端 B', '坐标 A', '坐标 B', '配置 A', '功能 A'):
            self.assertIn(text, result)

    def test_fenced_code_is_unchanged_and_second_pass_is_stable(self):
        code = '```bash\n# README\n## 核心功能\n---\necho example\n```'
        result = normalize_module('## 概述\n\n说明\n\n## 使用配置\n\n' + code)
        self.assertIn(code, result)
        self.assertEqual(result, normalize_module(result))

    def test_feature_subheadings_keep_their_hierarchy(self):
        result = normalize_module('## 核心功能\n\n## 资源校验\n\n### 返回值校验\n\n说明')
        self.assertIn('### 资源校验\n\n#### 返回值校验', result)
        self.assertEqual(result, normalize_module(result))

    def test_pom_defaults_use_actual_coordinates_and_exclude_test_dependencies(self):
        pom = '''<project xmlns="http://maven.apache.org/POM/4.0.0">
          <parent><groupId>dev.macula.boot</groupId></parent><artifactId>example</artifactId>
          <dependencies><dependency><groupId>runtime</groupId><artifactId>client</artifactId></dependency>
          <dependency><groupId>testing</groupId><artifactId>test-only</artifactId><scope>test</scope></dependency>
          </dependencies></project>'''
        result = pom_defaults([pom])
        self.assertIn('<artifactId>example</artifactId>', result['组件坐标'])
        self.assertIn('<artifactId>client</artifactId>', result['依赖引入'])
        self.assertNotIn('test-only', result['依赖引入'])


if __name__ == '__main__':
    unittest.main()
