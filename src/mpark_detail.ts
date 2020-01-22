import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';
import _ from 'lodash';
const data = require('./links_mpark.json');

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    const links = _.shuffle(Object.keys(data));
    for (let link of links) {
        try {
            console.log(link);
            await page.goto(link, { waitUntil: 'networkidle2', timeout: 0 });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_detail_mpark', name), html, (err) => {
                if (err) console.log(err);
            });
        } catch(e) {
            console.log(e);
        }
    }
    console.log('mpark_detail.ts has finished running');
    await browser.close();
})();
