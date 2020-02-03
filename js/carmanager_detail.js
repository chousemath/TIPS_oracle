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
    const browser = await puppeteer_1.default.launch({ headless: true, args: ['--no-sandbox'] });
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
                const newPagePromise = new Promise(x => browser.once('targetcreated', target => x(target.page())));
                await page.evaluate((x) => {
                    eval(x);
                }, link);
                const newPage = await newPagePromise;
                await sleep(2000);
                const html = await newPage.content();
                const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`;
                await fs.writeFile(path.join(__dirname, 'pages_detail_carmanager', name), html, (err) => {
                    if (err)
                        console.log(err);
                });
                await newPage.close();
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
