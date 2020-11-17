"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const puppeteer_1 = __importDefault(require("puppeteer")); // https://developers.google.com/web/tools/puppeteer
const root = 'https://www.nextunicorn.kr/online-ir/scale_up_IR';
(async () => {
    const browser = await puppeteer_1.default.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();
    try {
        await page.goto(root, { waitUntil: 'networkidle2', timeout: 0 });
        await page.evaluate(() => Array.from(document.getElementsByTagName('button')).filter(x => x.dataset.contentId === '784f4db163ee4b39')[0].click());
    }
    catch (e) {
        console.log(e);
    }
    console.log('vote.ts has finished running');
    await browser.close();
})();
