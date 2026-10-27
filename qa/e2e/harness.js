const { chromium } = require('playwright');
const B = require('./backend.js'); const SDK = require('./sdk-stub.js');
exports.newCtx = async (browser, htmlPath, opts = {}) => {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1100, height: 800 } }, opts));
  await ctx.exposeFunction('__fs', (auth, op, a) => B.handle(auth, op, a));
  await ctx.route(/gstatic\.com\/firebasejs/, r => { const f = r.request().url().split('/').pop(); r.fulfill({ contentType: 'application/javascript', body: SDK[f] || (f.includes('compat') ? '' : '') }); });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|googletagmanager|cdnjs/, r => r.abort());
  return ctx;
};
exports.B = B;
