"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const puppeteer_1 = __importDefault(require("puppeteer"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const lodash_1 = __importDefault(require("lodash"));
const data = require('./carmanager_links.json');
const root = 'http://www.carmanager.co.kr';
const extData = 'Car/Data';
const pageLimit = 500; // conservative page limit
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer_1.default.launch({ headless: false, args: ['--no-sandbox'] });
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768 });
        await page.goto(root, { waitUntil: 'networkidle2', timeout: 0 });
        await page.evaluate(() => document.getElementById('userid').value = '');
        await page.focus('#userid');
        await page.keyboard.type('trive'); // type in id
        await page.evaluate(() => document.getElementById('userpwd').value = '');
        await page.focus('#userpwd');
        await page.keyboard.type('trive1004'); // type in password
        await page.evaluate(() => commitLogin());
        await sleep(1000);
        await page.goto(`${root}/${extData}`, { waitUntil: 'networkidle2', timeout: 0 });
        const links = lodash_1.default.shuffle(Object.keys(data));
        for (let link of links) {
            console.log(link);
            try {
                //await page.goto(link, { waitUntil: 'networkidle2' });
                await page.evaluate((x) => {
                    carmangerDetailWindowPopUp(x, '', '', '', '', 2013.11, 104917, 1230);
                }, link);
                const pages = await browser.pages();
                const popup = pages[pages.length - 1];
                await sleep(5000);
                const html = await popup.content();
                const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`;
                await fs.writeFile(path.join(__dirname, 'pages_detail_carmanager', name), html, (err) => {
                    if (err)
                        console.log(err);
                });
                await popup.close();
                await sleep(5000);
            }
            catch (e) {
                console.log(e);
            }
        }
        console.log('finished running');
    }
    catch (e) {
        console.log(e);
    }
    await browser.close();
})();