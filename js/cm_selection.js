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
const root = 'http://www.carmanager.co.kr';
const extData = 'Car/Data';
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
        await sleep(1000);
        const data = {};
        const makers = await page.evaluate(() => {
            return Array.from(document
                .getElementById('ui_searchcarmaker')
                .getElementsByTagName('li')).map(x => x.innerText);
        });
        for (let maker of makers) {
            data[maker] = {};
            await page.evaluate(itext => {
                for (let item of Array.from(document.getElementById('ui_searchcarmaker').getElementsByTagName('li'))) {
                    if (item.innerText === itext) {
                        item.click();
                        break;
                    }
                }
            }, maker);
            await sleep(200);
            const models = await page.evaluate(() => {
                return Array.from(document
                    .getElementById('ui_searchcarmodel')
                    .getElementsByTagName('li')).map(x => x.innerText);
            });
            for (let model of models) {
                data[maker][model] = {};
                await page.evaluate(itext => {
                    for (let item of Array.from(document.getElementById('ui_searchcarmodel').getElementsByTagName('li'))) {
                        if (item.innerText === itext) {
                            item.click();
                            break;
                        }
                    }
                }, model);
                await sleep(200);
                const modelDetails = await page.evaluate(() => {
                    return Array.from(document
                        .getElementById('ui_searchcarmodeldetail')
                        .getElementsByTagName('li')).map(x => x.innerText);
                });
                for (let modelDetail of modelDetails) {
                    data[maker][model][modelDetail] = {};
                    for (let _ of modelDetails) {
                        const unchecked = await page.evaluate(() => {
                            for (let item of Array.from(document.getElementById('ui_searchcarmodeldetail').getElementsByTagName('li'))) {
                                const imgs = item.getElementsByTagName('img');
                                if (imgs.length > 0 && imgs[0].src.indexOf('btn_check_on') > -1) {
                                    item.click();
                                    return item.innerText;
                                }
                            }
                            return null;
                        });
                        if (unchecked) {
                            console.log(`${unchecked} was unchecked`);
                            break;
                        }
                        await sleep(200);
                    }
                    await page.evaluate(itext => {
                        for (let item of Array.from(document.getElementById('ui_searchcarmodeldetail').getElementsByTagName('li'))) {
                            if (item.innerText === itext) {
                                item.click();
                                break;
                            }
                        }
                    }, modelDetail);
                    await sleep(200);
                    const grades = await page.evaluate(() => {
                        return Array.from(document
                            .getElementById('ui_searchcargrade')
                            .getElementsByTagName('li')).map(x => x.innerText);
                    });
                    for (let grade of grades) {
                        data[maker][model][modelDetail][grade] = {};
                        for (let _ of grades) {
                            const unchecked = await page.evaluate(() => {
                                for (let item of Array.from(document.getElementById('ui_searchcargrade').getElementsByTagName('li'))) {
                                    const imgs = item.getElementsByTagName('img');
                                    if (imgs.length > 0 && imgs[0].src.indexOf('btn_check_on') > -1) {
                                        item.click();
                                        return item.innerText;
                                    }
                                }
                                return null;
                            });
                            if (unchecked) {
                                console.log(`${unchecked} was unchecked`);
                                break;
                            }
                            await sleep(200);
                        }
                        await page.evaluate(itext => {
                            for (let item of Array.from(document.getElementById('ui_searchcargrade').getElementsByTagName('li'))) {
                                if (item.innerText === itext) {
                                    item.click();
                                    break;
                                }
                            }
                        }, grade);
                        await sleep(200);
                        const gradeDetails = await page.evaluate(() => {
                            return Array.from(document
                                .getElementById('ui_searchcargradedetail')
                                .getElementsByTagName('li')).map(x => x.innerText);
                        });
                        for (let gradeDetail of gradeDetails) {
                            data[maker][model][modelDetail][grade][gradeDetail] = 1;
                        }
                    }
                }
            }
        }
        await fs.writeFile(path.join(__dirname, 'cm_selection.json'), JSON.stringify(data), (err) => {
            if (err)
                console.log(err);
        });
    }
    catch (e) {
        console.log(e);
    }
    await browser.close();
})();
