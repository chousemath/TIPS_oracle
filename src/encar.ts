/* General Link Scraper for Encar.com
 * The purpose of this script is to scrape all the detail page links for
 * the encar.com, foreign car platform.
 * Only the links (not the details on the details page) are scraped using this script
 * Last update 2020/01/28, Joseph Sungpil Choi
*/

// puppeteer is our web scraper of choice
import puppeteer from 'puppeteer'; // https://developers.google.com/web/tools/puppeteer
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.N.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D';
// a conservative limit on the number of pages of foreign
// cars on the Encar.com platform
const pageLimit = 1700;

// some parts of the script require a manual delay to allow for
// network latency
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    // The navigation strategy used by Encar.com follows a regular pattern
    const baseURL = (pgNum: number): string => root.replace('page%22%3A1', `page%22%3A${pgNum}`);
    const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
    const page = await browser.newPage();
    for (let pg = 1; pg < pageLimit; pg++) {
        try {
            await page.goto(baseURL(pg), { waitUntil: 'networkidle2', timeout: 0 });
            const html = await page.content();
            // we scrape the raw html of the listing page in order to comfortably scrape
            // the page at a later date/time
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_list', name), html, (err) => {
                if (err) console.log(err);
                else console.log(`page: ${pg}`);
            });
        } catch(e) {
            console.log(e);
        }
    }
    console.log('encar.ts has finished running');
    await browser.close();
})();

