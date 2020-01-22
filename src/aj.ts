import puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as path from 'path';

const root = 'http://www.sellcarauction.co.kr';
const extLogin = 'newfront/login.do';
const extList = 'newfront/receive/rc/receive_rc_list.do';
// <a href="javascript:void(0);" onclick="javascript:carInfo('RC202001160074');">1 르노삼성 SM3 네오 (14년~현재) RE</a>
//{
//var frm = document.frm;
//frm["receivecd"].value = 'RC202001160074';
//frm.action = "/newfront/onlineAuc/on/onlineAuc_on_detail.do";
//frm.submit();
//}

// function for advancing the list page
declare var CmPageMove: any;

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox'],
    });
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        // await page.click('#i_sLoginGubun2'); // 경매회원 checkbox
        await page.focus('#i_sUserId');
        await page.keyboard.type('462001'); // type in id
        await page.focus('#i_sPswd');
        await page.keyboard.type('yi313031'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        for (let i = 1; i < 4; i++) {
            await page.evaluate((idx: string) => CmPageMove(idx, '100'), `${i}`);
            await sleep(3000);
            const html = await page.content();
            const name = `${(new Date()).valueOf()}-${Math.floor(10000000 * Math.random())}.html`
            await fs.writeFile(path.join(__dirname, 'pages_list_aj', name), html, (err) => {
                if (err) console.log(err);
            });
            console.log(`page: ${i}`);
        }
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

/*
 * - pages_list
 * - pages_detail
 * */
