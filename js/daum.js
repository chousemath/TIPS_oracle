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
const months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1];
const sequence = [
    { year: 2020, months: [5, 4, 3, 2, 1] },
    { year: 2019, months },
    { year: 2018, months },
    { year: 2017, months },
];
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer_1.default.launch({ headless: false, args: ['--no-sandbox'] });
    const page = await browser.newPage();
    for (let seq of sequence) {
        for (let month of seq.months) {
            try {
                const baseURL = `https://auto.daum.net/news?year=${seq.year}&month=${month}`;
                await page.goto(baseURL, { waitUntil: 'networkidle2', timeout: 0 });
                const html = await page.content();
                const name = `${seq.year}-${month}.html`;
                await fs.writeFile(path.join(__dirname, 'pages_daum_news', name), html, (err) => {
                    if (err)
                        console.log(err);
                    else
                        console.log(`page: ${seq.year}, ${month}`);
                });
            }
            catch (e) {
                console.log(e);
            }
        }
    }
    console.log('daum.ts has finished running');
    await browser.close();
})();
