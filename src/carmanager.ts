import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.carmanager.co.kr';
const extData = 'Car/Data';
const pageLimit = 500; // conservative page limit
// function for logging in
declare var commitLogin: any;
// function for advancing the list page
declare var goPageSubmit: any;
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(root, { waitUntil: 'networkidle2', timeout: 0 });
        await page.evaluate(() => (document.getElementById('userid') as HTMLInputElement).value = '');
        await page.focus('#userid');
        await page.keyboard.type('trive'); // type in id
        await page.evaluate(() => (document.getElementById('userpwd') as HTMLInputElement).value = '');
        await page.focus('#userpwd');
        await page.keyboard.type('trive1004'); // type in password
        await page.evaluate(() => commitLogin());
        await sleep(1000);
        await page.goto(`${root}/${extData}`, { waitUntil: 'networkidle2', timeout: 0 });
        for (let i = 1; i < pageLimit; i++) {
            await page.evaluate((idx: string) => goPageSubmit(idx), `${i}`);
            await sleep(3000);
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_list_carmanager', name), html, (err) => {
                if (err) console.log(err);
            });
            console.log(`page: ${i}`);
        }
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

