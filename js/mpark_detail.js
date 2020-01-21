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
const data = require('./links_mpark.json');
const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer_1.default.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    const page = await browser.newPage();
    const links = lodash_1.default.shuffle(Object.keys(data));
    for (let link of links) {
        try {
            console.log(link);
            await page.goto(link, { waitUntil: 'networkidle2' });
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(100000000 * Math.random())}.html`;
            await fs.writeFile(path.join(__dirname, 'pages_detail_mpark', name), html, (err) => {
                if (err)
                    console.log(err);
            });
        }
        catch (e) {
            console.log(e);
        }
    }
    await browser.close();
})();
