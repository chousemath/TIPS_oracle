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
const root = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.N.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D';
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const baseURL = (pgNum) => root.replace('page%22%3A1', `page%22%3A${pgNum}`);
    const browser = await puppeteer_1.default.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    for (let pg = 1; pg < 1600; pg++) {
        try {
            await page.goto(baseURL(pg), { waitUntil: 'networkidle2', timeout: 0 });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`;
            await fs.writeFile(path.join(__dirname, 'pages_list', name), html, (err) => {
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
    console.log('encar.ts has finished running');
    await browser.close();
})();
/*
 * - pages_list
 * - pages_detail
 * */
