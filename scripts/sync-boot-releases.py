#!/usr/bin/env python3
"""Save public Macula Boot Releases as a small, offline-friendly changelog feed."""
import argparse
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

SITE = Path(__file__).resolve().parents[1]
REPOSITORY = 'macula-projects/macula-boot'
RELEASES_URL = f'https://github.com/{REPOSITORY}/releases'
API_URL = f'https://api.github.com/repos/{REPOSITORY}/releases'


def summary_lines(body):
    """Keep a few actual release bullets, including fixes after feature lists."""
    features, fixes = [], []
    in_fixes = False
    in_credits = False
    in_code = False
    for line in (body or '').splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            in_code = not in_code
        if in_code:
            continue
        if line.startswith('#'):
            in_fixes = bool(re.search(r'fix|修复|修正|缺陷', line, re.I))
            in_credits = bool(re.search(r'contributors|贡献者', line, re.I))
        if in_credits:
            continue
        bullet = re.match(r'^\s*[-*+]\s+(.+)', line)
        if not bullet:
            continue
        text = bullet[1]
        text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text.replace('`', '')).strip()
        text = re.sub(r'\s+by @\S+ in https://github\.com/\S+$', '', text)
        if not text or re.search(r'full changelog|完整变更|^https?://', text, re.I):
            continue
        if re.fullmatch(r'(暂无|无|none|n/a)[。.]?', text, re.I) or text.startswith('@'):
            continue
        if re.match(r'^(feature|release|hotfix)/', text, re.I):
            continue
        (fixes if in_fixes else features).append(text)
    # Reserve space for a bug fix when a longer feature list precedes it.
    lines = features[:3] + fixes[:1] if features and fixes else (features or fixes)[:4]
    return list(dict.fromkeys(lines)) or ['此版本未提供条目摘要，请查看 Release 发布详情。']


def normalize(releases):
    result = []
    seen = set()
    for release in releases:
        if release.get('draft'):
            continue
        tag = release['tag_name']
        match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?', tag, re.I)
        if not match:
            raise ValueError(f'Unsupported release version: {tag}')
        url = release['html_url']
        if not url.startswith(RELEASES_URL + '/tag/'):
            raise ValueError(f'Unexpected release URL: {url}')
        if tag in seen:
            raise ValueError(f'Duplicate release tag: {tag}')
        seen.add(tag)
        published = datetime.fromisoformat(release['published_at'].replace('Z', '+00:00'))
        result.append({
            'version': re.sub(r'^v', '', tag, flags=re.I),
            'tag': tag,
            'major': int(match[1]),
            'series': f'{match[1]}.{match[2]}',
            'published_at': release['published_at'],
            'date': published.astimezone(timezone(timedelta(hours=8))).date().isoformat(),
            'url': url,
            'prerelease': bool(release.get('prerelease')),
            'summary': summary_lines(release.get('body')),
        })
    if not result:
        raise ValueError('No published releases found; keep the existing snapshot')
    return sorted(result, key=lambda r: r['published_at'], reverse=True)


def fetch_releases():
    headers = {'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'macula-website'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    releases = []
    page = 1
    while True:
        request = Request(f'{API_URL}?per_page=100&page={page}', headers=headers)
        with urlopen(request, timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError('Unexpected GitHub Releases response')
        releases.extend(batch)
        if len(batch) < 100:
            return releases
        page += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Read an API response JSON file instead of the network')
    parser.add_argument('--output', type=Path, default=SITE / 'data/boot_releases.json')
    args = parser.parse_args()
    releases = json.loads(args.input.read_text()) if args.input else fetch_releases()
    data = {'repository': REPOSITORY, 'source_url': RELEASES_URL, 'releases': normalize(releases)}
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Finish fetching and validating every page before replacing the last good snapshot.
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(text)
    temporary.replace(args.output)
    print(f"Synced {len(data['releases'])} public releases from {REPOSITORY}")


if __name__ == '__main__':
    main()
