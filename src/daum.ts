import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1];
const sequence = [
    { year: 2020, months: [5, 4, 3, 2, 1] },
    { year: 2019, months },
    { year: 2018, months },
    { year: 2017, months },
];

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
    const page = await browser.newPage();
    for (let seq of sequence) {
        for (let month of seq.months) {
            try {
                const baseURL = `https://auto.daum.net/news?year=${seq.year}&month=${month}`;
                await page.goto(baseURL, { waitUntil: 'networkidle2', timeout: 0 });
                const html = await page.content();
                const name = `${seq.year}-${month}.html`
                await fs.writeFile(path.join(__dirname, 'pages_daum_news', name), html, (err) => {
                    if (err) console.log(err);
                    else console.log(`page: ${seq.year}, ${month}`);
                });
            } catch(e) {
                console.log(e);
            }
        }
    }
    console.log('daum.ts has finished running');
    await browser.close();
})();

