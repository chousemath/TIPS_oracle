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
const root = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D';
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const baseURL = (pgNum) => root.replace('page%22%3A1', `page%22%3A${pgNum}`);
    const browser = await puppeteer_1.default.launch({ headless: false, args: ['--no-sandbox'] });
    const page = await browser.newPage();
    for (let pg = 1; pg < 3500; pg++) {
        try {
            await page.goto(baseURL(pg), { waitUntil: 'networkidle2' });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`;
            await fs.writeFile(path.join(__dirname, 'pages_list_encar_domestic', name), html, (err) => {
                if (err)
                    console.log(err);
                else
                    console.log(`page: ${pg}`);
            });
        }
        catch (e) {
            console.log(e);
        }
    }
    console.log('encar_domestic.ts has finished running');
    await browser.close();
})();
