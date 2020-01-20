import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';
const links = require('./links.json');


const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    for (let link in links) {
        await page.goto(link, { waitUntil: 'networkidle2' });
        const html = await page.content();
        const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`
        await fs.writeFile(path.join(__dirname, 'pages_detail', name), html, (err) => {
            console.log(err);
        });
    }
    await browser.close();
})();
