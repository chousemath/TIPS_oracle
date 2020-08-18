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
const data = require('./links_aj.json');
const root = 'http://www.sellcarauction.co.kr';
const extLogin = 'newfront/login.do';
const extList = 'newfront/receive/rc/receive_rc_list.do';
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer_1.default.launch({ headless: false, args: ['--no-sandbox'] });
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768 });
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        await page.focus('#i_sUserId');
        await page.keyboard.type('462001'); // type in id
        await page.focus('#i_sPswd');
        await page.keyboard.type('yi313031'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        const links = lodash_1.default.shuffle(Object.keys(data));
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        for (let link of links) {
            console.log(link);
            try {
                await page.evaluate((_link) => carInfo(_link), link);
                await sleep(3000);
                const html = await page.content();
                const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`;
                await fs.writeFile(path.join(__dirname, 'pages_detail_aj', name), html, (err) => {
                    if (err)
                        console.log(err);
                });
                await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
            }
            catch (e) {
                console.log(e);
            }
        }
        console.log('aj_detail.ts has finished running');
    }
    catch (e) {
        console.log(e);
    }
    await browser.close();
})();
