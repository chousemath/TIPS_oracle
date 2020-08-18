import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.sellcarauction.co.kr';
const extLogin = 'newfront/login.do';
const extList = 'newfront/receive/rc/receive_rc_list.do';
const pageLimit = 175; // conservative page limit
// function for advancing the list page
declare var CmPageMove: any;
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({headless: false, args: ['--no-sandbox']});
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        // await page.click('#i_sLoginGubun2'); // 경매회원 checkbox
        await page.focus('#i_sUserId');
        await page.keyboard.type('462001'); // type in id
        await page.focus('#i_sPswd');
        await page.keyboard.type('yi313031'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        for (let i = 1; i < pageLimit; i++) {
            await page.evaluate((idx: string) => CmPageMove(idx, '100'), `${i}`);
            await sleep(3000);
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_list_aj', name), html, (err) => {
                if (err) console.log(err);
            });
            console.log(`page: ${i}`);
        }
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

