import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.m-park.co.kr/buy/my_car_list.asp?gotopage=1&sListOrder=DemoDay_D&sPageSize=39&sSearch=1';
const pageLimit = 175; // conservative page limit
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const baseURL = (pgNum: number): string => root.replace('gotopage=1', `gotopage=${pgNum}`);
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    for (let pg = 1; pg < pageLimit; pg++) {
        try {
            await page.goto(baseURL(pg), { waitUntil: 'networkidle2', timeout: 0 });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_list_mpark', name), html, (err) => {
                if (err) console.log(err);
                else console.log(`page: ${pg}`);
            });
        } catch(e) {
            console.log(e);
        }
    }
    console.log('mpark.ts has finished running');
    await browser.close();
})();

