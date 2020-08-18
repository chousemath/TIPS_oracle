import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';
import _ from 'lodash';
const data = require('./links_aj.json');

const root = 'http://www.sellcarauction.co.kr';
const extLogin = 'newfront/login.do';
const extList = 'newfront/receive/rc/receive_rc_list.do';
// function for navigating to the details page for a specific car
declare var carInfo: any;

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({headless: false, args: ['--no-sandbox']});
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        await page.focus('#i_sUserId');
        await page.keyboard.type('462001'); // type in id
        await page.focus('#i_sPswd');
        await page.keyboard.type('yi313031'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        const links = _.shuffle(Object.keys(data));
        await page.evaluate(() => window.scrollTo(0,document.body.scrollHeight));
        for (let link of links) {
            console.log(link);
            try {
                await page.evaluate((_link: string) => carInfo(_link), link);
                await sleep(3000);
                const html = await page.content();
                const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`
                await fs.writeFile(path.join(__dirname, 'pages_detail_aj', name), html, (err) => {
                    if (err) console.log(err);
                });
                await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
            } catch(e) {
                console.log(e);
            }
        }
        console.log('aj_detail.ts has finished running');
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();
