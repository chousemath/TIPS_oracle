import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.carmanager.co.kr';
const extData = 'Car/Data';
const pageLimit = 175; // conservative page limit
// function for advancing the list page
declare var commitLogin: any;
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
console.log('starting script');
(async () => {
    console.log('inside script');
    const browser = await puppeteer.launch({headless: false, args: ['--no-sandbox']});
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        console.log('starting wait');
        await page.goto(root, { waitUntil: 'networkidle2' });
        console.log('finished wait');
        await page.evaluate(() => (document.getElementById('userid') as HTMLInputElement).value = '');
        await page.focus('#userid');
        await page.keyboard.type('trive'); // type in id
        await page.evaluate(() => (document.getElementById('userpwd') as HTMLInputElement).value = '');
        await page.focus('#userpwd');
        await page.keyboard.type('122333'); // type in password
        await page.screenshot({path: 'carmanager-before-login.png'});
        await sleep(1000);
        await page.evaluate(() => commitLogin());
        console.log('beginning to sleep');
        await sleep(1000);
        await page.screenshot({path: 'carmanager-after-login.png'});
        await page.goto(`${root}/${extData}`, { waitUntil: 'networkidle2' });
        console.log('finished sleeping 2');
        await page.screenshot({path: 'example.png'});
        console.log('took snapshot right after');
        await sleep(1000);
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        console.log('took snapshot');
        //await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        //for (let i = 1; i < pageLimit; i++) {
        //    await page.evaluate((idx: string) => CmPageMove(idx, '100'), `${i}`);
        //    await sleep(3000);
        //    const html = await page.content();
        //    const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
        //    await fs.writeFile(path.join(__dirname, 'pages_list_aj', name), html, (err) => {
        //        if (err) console.log(err);
        //    });
        //    console.log(`page: ${i}`);
        //}
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

