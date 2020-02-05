import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';
import _ from 'lodash';
const data = require('./links_autoinside.json');

const root = 'https://www.autoinside.co.kr';
const extList = 'auc_end_car_list.do#PAGENUM';
const extLogin = 'mbr/mbr_member_login.do';
const pageLimit = 400; // conservative page limit
// function for advancing the list page
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        await page.focus('#i_sBidUserCd');
        await page.keyboard.type('B61701'); // type in id
        await page.focus('#i_sAucPswd');
        await page.keyboard.type('qkrgusxor1!'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        const links = _.shuffle(Object.keys(data));
        for (let link of links) {
            console.log(link);
            try {
                await page.goto(link, { waitUntil: 'networkidle2', timeout: 0 });
                await sleep(1000);
                const html = await page.content();
                const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`
                await fs.writeFile(path.join(__dirname, 'pages_detail_autoinside', name), html, (err) => {
                    if (err) console.log(err);
                });
            } catch(e) {
                console.log(e);
            }
        }
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

