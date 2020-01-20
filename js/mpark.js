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
const root = 'http://www.m-park.co.kr/buy/my_car_list.asp?gotopage=1&sListOrder=DemoDay_D&sPageSize=39&sSearch=1';
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const baseURL = (pgNum) => root.replace('gotopage=1', `gotopage=${pgNum}`);
    const browser = await puppeteer_1.default.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    for (let pg = 1; pg < 168; pg++) {
        try {
            await page.goto(baseURL(pg), { waitUntil: 'networkidle2' });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`;
            await fs.writeFile(path.join(__dirname, 'pages_list_mpark', name), html, (err) => {
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
    await browser.close();
})();
/*
 * - pages_list
 * - pages_detail
 * */
