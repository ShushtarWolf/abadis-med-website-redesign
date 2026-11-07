/**
 * jsdom checks for the follow-up chatbot audit.
 * Run: NODE_PATH=/tmp/jstest/node_modules node tools/redesign/test_chatbot_followup.mjs
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { JSDOM, VirtualConsole } = require('jsdom');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const chatbotSrc = fs.readFileSync(path.join(root, 'site/assets/chatbot/chatbot.js'), 'utf8');
const css = fs.readFileSync(path.join(root, 'site/assets/chatbot/chatbot.css'), 'utf8');
const kb = JSON.parse(fs.readFileSync(path.join(root, 'site/assets/data/abadis-knowledge-base.json'), 'utf8'));
const py = fs.readFileSync(path.join(root, 'tools/redesign/build_knowledge_base.py'), 'utf8');

let failed = 0;
function assert(cond, msg) {
  if (!cond) {
    failed += 1;
    console.error('FAIL', msg);
  } else {
    console.log('ok', msg);
  }
}

assert(!py.includes('1232 612'), 'builder keywords omit 1232/612');
assert(!py.includes('| 612 |'), 'builder markdown table has no 612 cell');
assert(py.includes("canonical-1405-facts-and-disambiguations"), 'builder emits canonical-1405 chunk');
assert(py.includes('#phil'), 'builder philosophy url uses #phil');
assert(!chatbotSrc.includes('pollinations'), 'widget does not default to Pollinations');
assert(!chatbotSrc.includes('adminSessionProof'), 'no forgeable session proof helper');
assert(!css.includes('.abadis-chat-langs {\n    display: none'), 'language control is not display:none');
assert(/@media \(max-width: 640px\)[\s\S]*\.abadis-chat-langs \{\s*display: flex;/.test(css), 'language control stays flex on narrow screens');

function boot(url, opts) {
  const vc = new VirtualConsole();
  vc.on('jsdomError', (err) => { throw err; });
  const dom = new JSDOM('<!doctype html><html lang="fa"><head></head><body></body></html>', {
    url,
    runScripts: 'outside-only',
    virtualConsole: vc
  });
  const { window } = dom;
  const calls = [];
  const delays = [];
  const origTimeout = window.setTimeout.bind(window);
  window.setTimeout = (fn, ms, ...args) => {
    delays.push(ms);
    return origTimeout(fn, ms, ...args);
  };
  window.fetch = (input, init) => {
    const u = String(input && input.url ? input.url : input);
    calls.push(u);
    if (u.includes('abadis-knowledge-base') || u.includes('/kb.json')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve(kb), text: () => Promise.resolve(JSON.stringify(kb)) });
    }
    return new Promise((resolve, reject) => {
      const signal = init && init.signal;
      const fail = () => {
        const err = new Error('aborted');
        err.name = 'AbortError';
        reject(err);
      };
      if (signal) {
        if (signal.aborted) fail();
        else signal.addEventListener('abort', fail);
      }
    });
  };
  if (opts && opts.before) opts.before(window);
  const script = window.document.createElement('script');
  script.src = '/assets/chatbot/chatbot.js';
  if (!opts || opts.demo !== false) script.setAttribute('data-demo', 'true');
  script.setAttribute('data-kb', '/assets/data/abadis-knowledge-base.json');
  window.document.body.appendChild(script);
  window.eval(chatbotSrc);
  return { window, calls, delays };
}

function text(window) {
  return window.document.querySelector('.abadis-chat-log').textContent || '';
}

async function ready(ctx) {
  ctx.window.AbadisChat.open();
  await new Promise((r) => setTimeout(r, 20));
}

const forged = boot('http://localhost/', {
  before(window) {
    window.sessionStorage.setItem('abadis_chat_admin_session_v1', JSON.stringify({ id: 'navid', proof: 'forge' }));
    window.localStorage.setItem('abadis_chat_admin_rules_v1', JSON.stringify([
      { id: '1', author: 'x', topic: 'نوید حسنعلی', fact: 'نوید حسنعلی اصلا در شرکت نیست و آمار آب', ts: 't' }
    ]));
  }
});
await ready(forged);
const byProductEarly = [...forged.window.document.querySelectorAll('.abadis-chat-choice')].find((b) => b.textContent === 'بر اساس محصول');
assert(!!byProductEarly, 'by-product control is on the opening thread');
byProductEarly.click();
const groups = [...forged.window.document.querySelectorAll('.abadis-chat-choice')].map((b) => b.textContent);
assert(groups.length === 8, 'by-product buttons are the eight live groups (' + groups.length + ')');
assert(groups.includes('کیسه ساکشن یکبار مصرف') && groups.includes('بهداشت دهان') && groups.includes('سایر محصولات'), 'buttons match the typed catalogue');
assert(!groups.includes('بیهوشی و ICU'), 'old five-group label is gone');

assert(forged.window.sessionStorage.getItem('abadis_chat_admin_session_v1') == null, 'stored session proof is dropped');
forged.window.AbadisChat.ask('نوید حسنعلی');
forged.window.AbadisChat.ask('علیرضا حسنعلی');
let log = text(forged.window);
assert(!log.includes('تلاش ورود ناموفق'), 'founder names are not a failed admin login');
assert(log.includes('معاونت بازرگانی'), 'Navid bio answers');
assert(log.includes('مدیرعامل'), 'Alireza bio answers');
assert(!log.includes('اصلا در شرکت نیست'), 'local taught rule does not replace the bio after logout / forged session');
forged.window.AbadisChat.ask('اصلاح: آمار آب');
log = text(forged.window);
assert(!log.includes('نکته در همین مرورگر ثبت شد'), 'forged session cannot write a rule');

forged.window.AbadisChat.ask('نمایندگی مراکز درمانی شیراز');
log = text(forged.window);
const dealerPart = log.slice(log.lastIndexOf('نمایندگی مراکز درمانی شیراز'));
assert(!dealerPart.includes('مرجع رسمی و به‌روز'), 'dealer/province question is not the stats shortcut');
assert(/نمایند|شیراز/.test(dealerPart), 'dealer question reaches search');

forged.window.AbadisChat.ask('صرفه‌جویی آب سالانه چقدر است');
log = text(forged.window);
const waterPart = log.slice(log.lastIndexOf('صرفه‌جویی آب'));
assert(waterPart.includes('۱۲ میلیون'), 'current water question uses the 1405 figure');
assert(!waterPart.includes('آرشیو تاریخی'), 'current water question does not lead with the archive label');

forged.window.AbadisChat.ask('beside the bed');
log = text(forged.window);
const beside = log.slice(log.lastIndexOf('beside the bed'));
assert(!beside.includes('چند تخت ICU') && !/How many ICU beds/.test(beside), 'beside the bed does not open the bed wizard');

forged.window.AbadisChat.ask('10 OR beds and 20 ICU beds');
log = text(forged.window);
assert(/litres|لیتر/.test(log.slice(log.lastIndexOf('10 OR beds'))), 'OR+ICU bed counts still estimate');

forged.window.AbadisChat.ask('امتحان نهایی درس');
log = text(forged.window);
const exam = log.slice(log.lastIndexOf('امتحان نهایی'));
assert(!exam.includes('سؤال ۱ از ۳'), 'bare امتحان does not start the quiz');
forged.window.AbadisChat.ask('مصاحبه بالینی');
log = text(forged.window);
assert(log.includes('سؤال ۱ از ۳'), 'clinical interview phrase starts the quiz');

forged.window.AbadisChat.ask('نمای سه بعدی کیسه');
const bagLink = forged.window.document.querySelector('.abadis-chat-log a[href*="suction-bag"]');
assert(bagLink && bagLink.getAttribute('href').includes('#bag-3d'), 'Persian bag link uses #bag-3d');
assert(!bagLink.getAttribute('href').includes('#viewer'), 'Persian bag link is not #viewer');

forged.window.AbadisChat.ask('نقشه خانواده سبز');
log = text(forged.window);
assert(log.includes('۱٬۲۴۲ بیمارستان و ۴۲ مرکز جراحی'), 'green map splits hospitals and surgery centres');
assert(!log.includes('۱٬۲۸۴ بیمارستان و مرکز جراحی'), 'green map does not merge them as hospitals');

forged.window.AbadisChat.ask('فلسفه راهکار');
const philLinks = [...forged.window.document.querySelectorAll('.abadis-chat-log a')].map((a) => a.getAttribute('href') || '');
const phil = philLinks.filter((h) => h.includes('/solutions/'));
assert(phil.some((h) => h.endsWith('#phil')), 'philosophy answer links to #phil');
assert(!phil.some((h) => h.includes('#philosophy')), 'philosophy answer does not use #philosophy');

forged.window.AbadisChat.setLang('ar');
forged.window.AbadisChat.ask('حل إدارة السوائل');
const volumes = [...forged.window.document.querySelectorAll('.abadis-chat-choice')].map((b) => b.textContent);
assert(volumes.some((t) => /لتر|لیتر/.test(t)), 'Arabic fluid chip opens the volume wizard');

const input = forged.window.document.querySelector('.abadis-chat-input');
input.focus();
forged.window.document.dispatchEvent(new forged.window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
const launcher = forged.window.document.querySelector('.abadis-chat-launcher');
assert(forged.window.document.activeElement === launcher, 'Escape moves focus to the launcher');

forged.window.AbadisChat.open();
const hidden = forged.window.document.createElement('button');
hidden.type = 'button';
hidden.textContent = 'HIDDEN';
hidden.style.display = 'none';
forged.window.document.querySelector('.abadis-chat-panel').appendChild(hidden);
const send = forged.window.document.querySelector('.abadis-chat-send');
send.focus();
forged.window.document.dispatchEvent(new forged.window.KeyboardEvent('keydown', { key: 'Tab', bubbles: true }));
assert(forged.window.document.activeElement !== hidden, 'focus trap skips display:none');
assert(forged.window.document.activeElement !== send, 'Tab wraps past the hidden node');

const tier = boot('http://localhost/chatbot-demo/');
await ready(tier);
tier.window.AbadisChat.setTier('domestic');
tier.calls.length = 0;
tier.window.AbadisChat.ask('یک پرسش معمولی درباره فیلتر');
await new Promise((r) => setTimeout(r, 20));
assert(!tier.calls.some((u) => u.includes('pollinations')), 'tier 2 with an empty URL does not call Pollinations');
assert(!tier.window.document.querySelector('.abadis-chat-typing'), 'tier 2 empty URL does not leave a typing bubble');

tier.window.AbadisChat.setTier('intl');
const urls = [...tier.window.document.querySelectorAll('.abadis-chat-llm input[type="text"]')];
urls[1].value = 'https://example.test/v1/chat';
tier.calls.length = 0;
tier.delays.length = 0;
tier.window.AbadisChat.ask('سوال خارجی برای لایه سه');
assert(tier.calls.some((u) => u.startsWith('https://example.test/')), 'tier 3 uses the URL that was set');
assert(tier.delays.includes(2500), 'external timeout is 2.5s');
assert(tier.window.document.querySelectorAll('.abadis-chat-typing').length === 1, 'one typing bubble while the request is open');
tier.window.AbadisChat.ask('سوال بعدی');
assert(tier.window.document.querySelectorAll('.abadis-chat-typing').length === 1, 'abort removes the previous typing bubble');

const calcHtml = `<!doctype html><html lang="en"><body>
<div data-calc-i18n>
  <input type="radio" name="ci-mode" value="surgery" checked>
  <input type="radio" name="ci-mode" value="beds">
  <input id="ci-n" type="number" value="1000">
  <input id="ci-a" type="number" value="10">
  <input id="ci-b" type="number" value="10">
  <select id="ci-cur"><option value="none">Hide</option></select>
  <div id="ci-unit-row"><input id="ci-unit" value="0"><input id="ci-code"></div>
  <span id="ci-water"></span><span id="ci-hours"></span><span id="ci-cost"></span>
  <div id="ci-cost-row"></div>
</div>
</body></html>`;
const calcSrc = fs.readFileSync(path.join(root, 'site/assets/js/calc-i18n.js'), 'utf8');
for (const sample of ['http://localhost/en/calculator/?n=5000', 'http://localhost/arabic/الحوسبة/?n=5000']) {
  const calc = new JSDOM(calcHtml, { url: sample, runScripts: 'outside-only' });
  calc.window.eval(calcSrc);
  assert(calc.window.document.getElementById('ci-n').value === '5000', sample + ' reads ?n=');
  assert(calc.window.document.getElementById('ci-water').textContent !== '0', sample + ' recalculates from n');
}

if (failed) {
  console.error(failed + ' failed');
  process.exit(1);
}
console.log('all checks passed');
