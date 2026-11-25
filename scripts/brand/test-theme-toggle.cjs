// Behavioural test for docs/website/theme-toggle-reference.html (Playwright, Chromium).
//   node scripts/brand/test-theme-toggle.cjs
const { chromium } = require('playwright');
const path = require('path');
const url = 'file://' + path.resolve(__dirname, '../../docs/website/theme-toggle-reference.html');
let fails = 0;
const check = (ok, msg) => { console.log(`${ok ? '  ✓' : '  ✗'} ${msg}`); if (!ok) fails++; };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ colorScheme: 'dark' });
  const p = await ctx.newPage();
  const bg = () => p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  await p.goto(url);
  check(await bg() === 'rgb(11, 18, 32)', 'no saved choice + OS dark -> dark page');
  check(await p.getAttribute('#theme-toggle', 'aria-label') === 'Switch to light theme', 'label describes the action');
  await p.click('#theme-toggle');
  check(await bg() === 'rgb(244, 248, 252)', 'click switches the whole page to light instantly');
  await p.reload();
  check(await bg() === 'rgb(244, 248, 252)', 'choice persists after reload (no flash: set before paint)');
  await p.keyboard.press('Tab');
  check(await p.evaluate(() => document.activeElement.id) === 'theme-toggle', 'toggle is reachable by keyboard');
  await p.keyboard.press('Space');
  check(await bg() === 'rgb(11, 18, 32)', 'Space activates the toggle');
  await p.keyboard.press('Enter');
  check(await bg() === 'rgb(244, 248, 252)', 'Enter activates the toggle');
  await p.click('#theme-reset');
  check(await bg() === 'rgb(11, 18, 32)', '"Use system setting" returns to OS preference');
  await p.emulateMedia({ colorScheme: 'light' });
  check(await bg() === 'rgb(244, 248, 252)', 'follows live OS change while no choice is saved');
  await p.emulateMedia({ colorScheme: 'light', reducedMotion: 'reduce' });
  check(await p.evaluate(() => getComputedStyle(document.querySelector('#theme-toggle svg')).transitionDuration) === '0s', 'reduced motion disables icon transition');
  await b.close();
  console.log(fails ? `\n${fails} failure(s)` : '\nAll theme-toggle checks passed.');
  process.exit(fails ? 1 : 0);
})();
