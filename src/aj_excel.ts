import puppeteer from 'puppeteer';

const root = 'http://www.sellcarauction.co.kr';
const extLogin = 'newfront/login.do';
const extList = 'newfront/receive/rc/receive_rc_list.do';
const extExcel = '/newfront/receive/rc/receive_rc_excelDown.do'

// function for generating excel file
declare var fncExcelDownload_new: any;

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
(async () => {
    const browser = await puppeteer.launch({
        headless: false,
        args: [
            '--no-sandbox',
            '--profile-directory="Default"',
        ],
    });
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1366, height: 768});
        await page.goto(`${root}/${extLogin}`, { waitUntil: 'networkidle2', timeout: 0 });
        await page.focus('#i_sUserId');
        await page.keyboard.type('462001'); // type in id
        await page.focus('#i_sPswd');
        await page.keyboard.type('yi313031'); // type in password
        await page.keyboard.press('Enter'); // press enter key
        await sleep(1000);
        await page.goto(`${root}/${extList}`, { waitUntil: 'networkidle2', timeout: 0 });
        await page.evaluate(() => {
            fncExcelDownload_new('/newfront/receive/rc/receive_rc_excelDown.do', 'ALL');
        });
        await sleep(2000);
    } catch(e) {
        console.log(e);
    }
    await browser.close();
})();

