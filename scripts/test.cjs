const {chromium}=require('@playwright/test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const qs=JSON.parse(fs.readFileSync('questions.json'));
const base=process.env.TEST_URL||'http://localhost:4173';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('#start').waitFor();
 await page.locator('#help').click();assert(await page.locator('#help-dialog').evaluate(d=>d.open));await page.locator('#help-dialog .primary').click();
 await page.locator('#sound').click();assert.equal(await page.locator('#sound').getAttribute('aria-pressed'),'true');await page.locator('#sound').click();
 await page.screenshot({path:'/tmp/shigicchi-home-desktop.png',fullPage:true});
 await page.locator('[data-count="26"]').click();await page.locator('#start').click();
 assert.equal(await page.evaluate(()=>score(2,3)),67);assert.equal(await page.evaluate(()=>score(1,3)),33);
 const seen=new Set();
 for(let i=0;i<26;i++){
  const q=await page.evaluate(()=>round[index]);assert(q.active);assert(!seen.has(q.id));seen.add(q.id);
  assert.equal(await page.locator('.choice').count(),q.options.length);
  if(process.env.CHECK_IMAGES){await page.locator('.question-picture img').evaluate(im=>im.decode());assert(await page.locator('.question-picture img').evaluate(im=>im.naturalWidth>0));}
  if(i===0){await page.locator('#quit').click();await page.locator('#stay').click();assert.equal(await page.evaluate(()=>index),0);}
  await page.locator(`[data-choice="${q.correct[0]}"]`).click();
  assert.equal(await page.evaluate(()=>results.length),i+1);
  assert(await page.locator('.feedback h2').textContent().then(s=>s.includes('だいせいかい')));
  if(q.explanation)assert((await page.locator('#feedback').textContent()).includes(q.explanation));
  await page.locator('#next').click();
 }
 assert.equal(await page.locator('.score').innerText(),'100 点');assert.equal(seen.size,26);
 await page.screenshot({path:'/tmp/shigicchi-result.png',fullPage:true});
 await page.locator('#back').click();await page.locator('[data-count="10"]').click();await page.locator('#start').click();
 for(let i=0;i<10;i++){const q=await page.evaluate(()=>round[index]);const wrong=q.options.findIndex((_,n)=>!q.correct.includes(n));await page.locator(`[data-choice="${wrong}"]`).click();await page.locator('#next').click()}
 assert.equal(await page.locator('.score').innerText(),'0 点');await page.locator('#retry').click();assert.equal(await page.evaluate(()=>round.length),10);
 for(let i=0;i<10;i++){const q=await page.evaluate(()=>round[index]);const n=i<7?q.correct[0]:q.options.findIndex((_,n)=>!q.correct.includes(n));await page.locator(`[data-choice="${n}"]`).click();await page.locator('#next').click()}
 assert.equal(await page.locator('.score').innerText(),'70 点');
 await page.evaluate(()=>start([data.find(q=>q.id===16)]));await page.locator('[data-choice="0"]').click();await page.locator('[data-choice="1"]').click();await page.locator('[data-choice="2"]').click();await page.locator('#submit').click();assert.equal(await page.evaluate(()=>results[0].good),true);await page.locator('#next').click();
 await page.locator('#back').click();
 for(const width of [390,768,1440]){
  await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(width===390)await page.screenshot({path:'/tmp/shigicchi-home-mobile.png',fullPage:true});
  await page.evaluate(()=>start([data.find(q=>q.id===14)]));assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(width===390)await page.screenshot({path:'/tmp/shigicchi-question-mobile.png',fullPage:true});
  if(width===1440)await page.screenshot({path:'/tmp/shigicchi-question-desktop.png',fullPage:true});
  await page.locator('[data-choice="1"]').click();assert.equal(await page.evaluate(()=>results[0].good),false);
  if(width===390)await page.screenshot({path:'/tmp/shigicchi-feedback-mobile.png',fullPage:true});
  await page.locator('#next').click();await page.locator('#back').click();
 }
 await page.goto(base+'/teacher.html');await page.locator('details').first().waitFor();assert.equal(await page.locator('details').count(),41);
 assert.equal(errors.length,0,errors.join('\n'));
 await browser.close();console.log('PASS: all 26 active questions, 100/0/70 point grading, retry, explanations, multi-answer, home/help/sound, 390/768/1440 layouts, teacher audit; no JavaScript errors.');
})().catch(e=>{console.error(e);process.exit(1)});
