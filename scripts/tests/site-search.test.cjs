const { test } = require('node:test');
const assert = require('node:assert/strict');
const { search, versionFromPath } = require('../../assets/js/site-search.js');
const pages = [
  { title: 'Gateway', body: '接口加解密与签名 jwk-set-uri', version: 'latest', url: '/docs/latest/gateway/' },
  { title: 'Gateway', body: '接口加解密与签名', version: '5.x', url: '/docs/5.x/gateway/' },
  { title: '安全架构', body: 'Gateway jwk-set-uri', version: 'latest', url: '/docs/latest/security/' },
  { title: '博客', body: 'Gateway', version: '', url: '/blog/example/' },
];
test('current version excludes historical and public pages; scope can be changed', () => {
  assert.deepEqual(search(pages, 'Gateway', versionFromPath('/docs/latest/security/')).map(p => p.url), ['/docs/latest/gateway/', '/docs/latest/security/']);
  assert.equal(search(pages, 'gateway', '5.x').length, 1);
  assert.equal(search(pages, 'gateway', 'all').length, 4);
  assert.equal(versionFromPath('/docs/3.1/chapter/'), '3.1');
  assert.equal(versionFromPath('/blog/'), 'all');
});
test('Chinese phrases and configuration identifiers work without external tokenizer', () => {
  assert.equal(search(pages, '加解密', 'latest')[0].title, 'Gateway');
  assert.equal(search(pages, 'gateway jwk-set-uri', 'latest').length, 2);
  assert.deepEqual(search(pages, '不存在', 'all'), []);
  assert.deepEqual(search(pages, '   ', 'all'), []);
});
