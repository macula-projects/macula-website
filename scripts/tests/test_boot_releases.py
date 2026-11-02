"""Verify public release selection, useful summaries and safe snapshot updates."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('boot_releases', Path(__file__).parents[1] / 'sync-boot-releases.py')
feed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed)


def release(tag='v6.0.0', **changes):
    result = {'tag_name': tag, 'html_url': feed.RELEASES_URL + '/tag/' + tag,
              'published_at': '2026-05-28T02:45:54Z', 'body': '- 接入新组件',
              'draft': False, 'prerelease': False}
    result.update(changes)
    return result


class ReleaseFeedTest(unittest.TestCase):
    def test_public_history_uses_publication_date_not_version_order(self):
        result = feed.normalize([release(), release('v5.0.20', published_at='2026-07-07T02:24:45Z'),
                                 release('v6.1.0', draft=True)])
        self.assertEqual([r['version'] for r in result], ['5.0.20', '6.0.0'])
        self.assertEqual(result[1]['series'], '6.0')

    def test_summaries_include_fixes_and_skip_credits_and_empty_sections(self):
        body = ('## Features\n- 新特性 A\n- 新特性 B\n- 新特性 C\n- 新特性 D\n'
                '## Bug Fixes\n- 修复问题\n- 暂无\n'
                '## New Contributors\n- @alice made a contribution\n')
        self.assertEqual(feed.summary_lines(body), ['新特性 A', '新特性 B', '新特性 C', '修复问题'])
        self.assertEqual(feed.summary_lines('## Bug Fixes\n- 暂无\n- `macula.*` 配置修复'), ['macula.* 配置修复'])

    def test_prerelease_and_empty_body_are_explicit(self):
        result = feed.normalize([release('v5.0.0-RC4', prerelease=True, body=None)])[0]
        self.assertTrue(result['prerelease'])
        self.assertEqual(result['version'], '5.0.0-RC4')
        self.assertIn('未提供', result['summary'][0])

    def test_dates_use_beijing_calendar(self):
        self.assertEqual(feed.normalize([release(published_at='2023-07-26T16:15:07Z')])[0]['date'], '2023-07-27')

    def test_invalid_source_and_duplicate_versions_are_rejected(self):
        for values in [[release(html_url='https://example.org/tag/v6.0.0')],
                       [release('unversioned')], [release(), release()], []]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                feed.normalize(values)

    def test_api_pages_are_all_read(self):
        pages = [io.BytesIO(json.dumps([{'id': n} for n in range(100)]).encode()),
                 io.BytesIO(json.dumps([{'id': 100}]).encode())]
        with patch.object(feed, 'urlopen', side_effect=pages) as request:
            self.assertEqual(len(feed.fetch_releases()), 101)
            self.assertIn('page=2', request.call_args_list[1].args[0].full_url)

    def test_failed_sync_keeps_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'releases.json'
            output.write_text('last good snapshot')
            with patch('sys.argv', ['sync', '--output', str(output)]), \
                 patch.object(feed, 'fetch_releases', side_effect=RuntimeError('API unavailable')):
                with self.assertRaises(RuntimeError):
                    feed.main()
            self.assertEqual(output.read_text(), 'last good snapshot')


if __name__ == '__main__':
    unittest.main()
