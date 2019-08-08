import { Command } from 'commander';
import puppeteer from 'puppeteer';
import _ from 'lodash';
import { config } from 'dotenv';
const { colorToNumber } = require('./mappings');
const { convertAndInsert } = require('./toBigQuery');

config();

const cmdr = new Command();

cmdr
  .version('0.0.1')
  .option('-c, --category [value]', 'Starting URL for the scraper script', 'domestic')
  .option('-n, --number [value]', 'Maximum number of pages', 3173)
  .parse(process.argv);

let scrapingLink = '';
let scrapingPageLimit = 0;

switch (cmdr.category) {
  case 'domestic':
    scrapingLink = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.Y.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D';
    scrapingPageLimit = 3312;
    break;
  case 'foreign':
    scrapingLink = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for&searchType=model&TG.R=B#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.N.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D';
    scrapingPageLimit = 1321;
    break;
}

const sleep = (ms = 0) => new Promise(r => setTimeout(r, ms));
console.log('>>>', process.env.MONGODB_URI);
const MongoClient = require('mongodb').MongoClient;
const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri, { useNewUrlParser: true });

interface VehicleDetails {
  mileage: number;
  dealerSalesInProgress: number;
  dealerSold: number;
  price: number;
  inquiries: number;
  likes: number;
  colorCode: number;
  timestamp: number;
  inspectionPerformed: boolean;
  title: string;
  year: string;
  fuel: string;
  category: string;
  displacement: string;
  transmission: string;
  color: string;
  plateNumber: string;
  dealerAddress: string;
  encarNumber: string;
  insurance: string;
  optionsExtra: string;
  insuranceReportDate: string;
  vehicleDetails: string;
  specialAccident: string;
  insuranceForDamage: string;
  insuranceForViolence: string;
  inspectionLight: string;
  '사고이력': string;
  '단순수리': string;
  '성능/상태점검자': string;
  '자동차 용도변경이력': string;
  dealerPhone: Array<string>;
  options: Array<string>;
  images: Array<string>;
}

interface Inspection {
  carInfo: string;
  inspectionDate: string;
  comments: string;
  '중고자동차 성능 상태 점검자': string;
  '중고자동차 성능 상태 고지자': string;
  comprehensiveStatus: any;
  repairStatus: any;
  stateDetails: any;
  visual: Array<string>;
}

client.connect((err: Error) => {
  const collectionEncar = client.db('oracle').collection('encar');
  const collectionSortingRequired = client.db('oracle').collection('sortingrequired');
  (async () => {
    const scrapeEncar = async (pageLimit: number, pageLink: string) => {
      const baseURL = (pageNumber: number) => pageLink.replace('page%22%3A1', `page%22%3A${pageNumber}`);
      const pageLinks = _.shuffle([...Array(pageLimit).keys()].map(pageNumber => baseURL(pageNumber + 1)));
      const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox'],
      });
      const page = await browser.newPage();
      // await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A404 Safari/601.1')
      for (let pageLink of pageLinks) {
        try {
          await page.goto(pageLink, {
            waitUntil: 'networkidle2',
          });
          const getDetailPageLinks = await page.evaluate(() => {
            let hrefs = [];
            const anchorTags = Array.from(document.getElementsByTagName('a'));
            for (let anchorTag of anchorTags) {
              // if (anchorTag.className !== '¸¸¸ ') continue;
              hrefs.push({ link: anchorTag.href });
            }
            return hrefs.filter(href => href.link.indexOf('dc_cardetailview') > -1);
          });
          const detailPageLinks = getDetailPageLinks;
          for (let detailLink of detailPageLinks) {
            try {
              await page.goto(detailLink.link, {
                waitUntil: 'networkidle2' // or networkidle0
              });
              await sleep(1000);
              const getDetailImages = await page.evaluate(() => {
                let details: VehicleDetails = {
                  mileage: 0,
                  dealerSalesInProgress: 0,
                  dealerSold: 0,
                  price: 0,
                  inquiries: 0,
                  likes: 0,
                  colorCode: 0,
                  timestamp: 0,
                  inspectionPerformed: false,
                  title: '',
                  year: '',
                  fuel: '',
                  category: '',
                  displacement: '',
                  transmission: '',
                  color: '',
                  plateNumber: '',
                  dealerAddress: '',
                  encarNumber: '',
                  insurance: '',
                  optionsExtra: '',
                  insuranceReportDate: '',
                  vehicleDetails: '',
                  specialAccident: '',
                  insuranceForDamage: '',
                  insuranceForViolence: '',
                  inspectionLight: '',
                  '사고이력': '',
                  '단순수리': '',
                  '성능/상태점검자': '',
                  '자동차 용도변경이력': '',
                  dealerPhone: [],
                  options: [],
                  images: [],
                };
                const productNames = Array.from(document.getElementsByClassName('prod_name'));
                for (let productName of productNames) {
                  if ((productName as HTMLDivElement).innerText) {
                    details.title = (productName as HTMLDivElement).innerText;
                  }
                }
                // const h1s = Array.from(document.getElementsByTagName('h1'));
                // for (let h1 of h1s) {
                //   if (h1.className === 'name') {
                //     details.title = h1.innerHTML;
                //     details.title = details.title.replace('</span>', '').replace('</span>', '').replace('<span class="brand">', '').replace('<span class="detail">', '')
                //   }
                // }
                const listItems = document.getElementsByClassName('prod_infomain')[0].getElementsByTagName('li');
                const listItemsInner = Array.from(listItems).map(listItem => {
                  const val = listItem.innerHTML.split('<a')[0].replace('<span class="blind">', '').replace('</span>', '').replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '');
                  if (val.indexOf(':') > -1) return val.split(':')[1];
                  return val;
                });
                details.mileage = +listItemsInner[0].toLowerCase().replace('km', '').replace(/,/g, '').trim();
                details.year = listItemsInner[1];
                details.fuel = listItemsInner[2];
                details.category = listItemsInner[3];
                details.displacement = listItemsInner[4];
                details.transmission = listItemsInner[5];
                details.color = listItemsInner[6];

                // convert string color value into a numeric value (better for neural network)
                details.plateNumber = listItemsInner[7].replace('차량번호', '');
                const goods = Array.from(document.getElementsByClassName('goods')) as Array<HTMLDivElement>;
                const dealerText0 = goods[0].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '');
                details.dealerAddress = dealerText0.split('주소')[1];
                const dealerText = goods[1].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '');
                details.dealerSalesInProgress = +dealerText.split('|')[1].replace('판매중', '').trim();
                details.dealerSold = +dealerText.split('|')[2].replace('판매완료', '').trim();
                details.dealerPhone = Array.from(document.getElementsByClassName('ph')).map(sp => sp.innerHTML.replace('<em>', '').replace('</em>', '').replace('연락처:', ''));
                const priceDiv = document.getElementsByClassName('prod_price')[0];
                const span = priceDiv.getElementsByTagName('span')[1];
                details.price = +span.innerHTML.replace('<em>', '').replace('</em>', '').replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '').replace('만원', '').replace(/,/g, '').trim();
                const regItems = document.getElementsByClassName('reg')[0].getElementsByTagName('li');
                details.encarNumber = regItems[0].innerText.split('등록번호')[1].replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '').trim();
                details.inquiries = +regItems[1].innerText.split('조회수')[1].split('자세히보기')[0].replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '').trim();
                details.likes = +regItems[2].innerText.split('찜')[1].replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '').trim();
                details.options = Array.from(document.getElementsByTagName('dd')).filter(tag => tag.className === 'on').map(tag => tag.innerText);
                const optionsExtra = document.getElementsByClassName('etc');
                if (optionsExtra.length > 0) details.optionsExtra = (optionsExtra[0] as HTMLDivElement).innerText.trim();

                const galleryThumbnail = document.getElementById('galleryThumbnail');
                if (galleryThumbnail) {
                  details.images = Array
                    .from(galleryThumbnail.getElementsByTagName('img'))
                    .map(img => img.src)
                    .filter(src => src.indexOf('carpicture') > -1)
                    .map(src => src.split('.jpg')[0] + '.jpg');
                }

                details.insurance = '';
                const insurance = document.getElementsByClassName('ins_history');
                if (insurance.length > 0) details.insurance = (insurance[0] as HTMLDivElement).innerText.trim();
                details.insuranceReportDate = '';
                const insuranceReportDate = Array.from(document.getElementsByClassName('ins_notice'));
                if (insuranceReportDate.length > 0) details.insuranceReportDate = (insuranceReportDate[0] as HTMLDivElement).innerText.split('\n')[0].replace(/(\r\n|\n|\r)/gm, '').replace(/ /g, '');
                details.vehicleDetails = '';
                const vehicleDetails = document.getElementById('areaCardetail');
                if (vehicleDetails) details.vehicleDetails = vehicleDetails.innerText;
                const inspectionLinks = Array.from(document.getElementsByTagName('a')).filter(a => a.href.indexOf('javascript:inspectionPop(') > -1);
                details.inspectionPerformed = inspectionLinks.length > 0;
                const insuranceDetails = Array.from(Array.from(document.getElementsByClassName('ins_history'))[0].getElementsByTagName('dd')).map(dd => dd.innerText);
                details['자동차 용도변경이력'] = insuranceDetails[0];
                details.insuranceForDamage = insuranceDetails[1];
                details.specialAccident = insuranceDetails[2];
                details.insuranceForViolence = insuranceDetails[3];
                const inspectionLight = Array.from(Array.from(document.getElementsByClassName('detail_inspection_info'))[0].getElementsByTagName('dd')).map(dd => dd.innerText.replace(/\n/g, '').trim());
                details.inspectionLight = inspectionLight[0];
                details['사고이력'] = inspectionLight[1];
                details['단순수리'] = inspectionLight[2];
                details['성능/상태점검자'] = inspectionLight[3];
                return details;
              });
              let data: VehicleDetails = getDetailImages;


              /*
               * if the color has not yet be categorized by us,
               * save it to a database so we can categorize to asap
              */
              data.colorCode = colorToNumber(data.color);
              if (data.colorCode === 0) {
                const doc = collectionSortingRequired.findOne({ value: data.color })
                if (!doc) {
                  const payload = {
                    source: 'encar',
                    category: 'color',
                    value: data.color,
                    valueType: Object.prototype.toString.call(data.color),
                    timestamp: Math.floor(Date.now() / 1000),
                  };
                  collectionSortingRequired.insertOne(payload, (err: Error, res: any) => {
                    if (err) console.log(`MongoDB Error (sorting required): ${err}`);
                    else console.log(`Problematic color (${data.color}) saved`);
                  });
                }
              }

              data.images = _.uniq(data.images);

              if (data.inspectionPerformed) {
                const inspectionLink = `http://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid=${data.encarNumber}&wtClick_carview=015`;
                await page.goto(inspectionLink, {
                  waitUntil: 'networkidle2',
                });
                const getInspectionDetails = await page.evaluate(() => {
                  let inspect: Inspection = {
                    carInfo: '',
                    inspectionDate: '',
                    comments: '',
                    '중고자동차 성능 상태 점검자': '',
                    '중고자동차 성능 상태 고지자': '',
                    comprehensiveStatus: {},
                    repairStatus: {},
                    stateDetails: {},
                    visual: [],
                  };
                  inspect.carInfo = (Array.from(document.getElementsByClassName('inspec_carinfo'))[0] as HTMLDivElement).innerText;
                  const comprehensiveStatusLabels = ["주행거리 계기상태", "주행거리 상태", "차대번호 표기", "배출가스", "튜닝", "특별이력", "용도변경", "색상", "주요옵션"];
                  const comprehensiveStatus = Array.from(
                    document.getElementsByClassName('tbl_total')[0]
                      .getElementsByTagName('tr'))
                    .slice(1)
                    .map(tr => Array.from(tr.getElementsByTagName('span'))
                      .filter(span => {
                        const className = span.className;
                        return className.indexOf('on') > -1 || className.indexOf('active') > -1;
                      })).map(spanList => spanList.length > 0 ? spanList[0].innerText : null);
                  inspect.comprehensiveStatus = {}
                  for (let i = 0; i < comprehensiveStatusLabels.length; i++) {
                    inspect.comprehensiveStatus[comprehensiveStatusLabels[i]] = comprehensiveStatus[i];
                  }
                  const repairStatusLabels = [
                    '사고이력',
                    '단순수리',
                    '부위별 이상여부---1',
                    '부위별 이상여부---2',
                    '부위별 이상여부---3',
                  ];
                  const repairStatus = Array.from(
                    document.getElementsByClassName('tbl_repair')[0]
                      .getElementsByTagName('tr'))
                    .map(tr => Array.from(tr.getElementsByTagName('span'))
                      .filter(span => {
                        const className = span.className;
                        return className.indexOf('on') > -1 || className.indexOf('active') > -1;
                      })).map(spanList => spanList.length > 0 ? spanList[0].innerText : null);

                  inspect.repairStatus = {}
                  for (let i = 0; i < repairStatusLabels.length; i++) {
                    inspect.repairStatus[repairStatusLabels[i]] = repairStatus[i];
                  }
                  const visual = Array.from(document.getElementsByClassName('list_lank')).map(ul => Array.from(ul.getElementsByTagName('li')).map(li => li.innerText.replace(/(\r\n|\n|\r)/gm, ' ')).filter(litxt => litxt.indexOf('랭크') > -1));
                  inspect.visual = visual[0].concat(visual[1]);
                  inspect.stateDetails = {}
                  const stateDetailsLabels = [
                    '자기진단---원동기',
                    '자기진단---변속기',
                    '원동기---작동상태(공회전)',
                    '원동기---오일누유---로커암 커버',
                    '원동기---오일누유---실린더 헤드/가스켓',
                    '원동기---오일누유---오일펜',
                    '원동기---오일유량',
                    '원동기---냉각수누수---실린더 헤드/가스켓',
                    '원동기---냉각수누수---워터펌프',
                    '원동기---냉각수누수---라디에이터',
                    '원동기---냉각수누수---냉각수수량',
                    '원동기---고압펌프(커먼레일)-디젤엔진',
                    '변속기---자동변속기(A/T)---오일누유',
                    '변속기---자동변속기(A/T)---오일유량 및 상태',
                    '변속기---자동변속기(A/T)---작동상태(공회)',
                    '동력전달---클러치 어셈블리',
                    '동력전달---등속죠인트',
                    '동력전달---추진축 및 베어',
                    '조향---동력조향작동 오일 누유',
                    '조향---작동상태---스티어링기어',
                    '조향---작동상태---스티어링펌프',
                    '조향---작동상태---타이로드엔드 및 볼 죠인트',
                    '제동---브레이크 마스터 실린더오일 누유',
                    '제동---브레이크 오일 누유',
                    '제동---배력장치 상태',
                    '전기---발전기 출력',
                    '전기---시동 모터',
                    '전기---와이퍼 모터 기능',
                    '전기---실내송풍 모터',
                    '전기---라디에이터 팬 모터',
                    '전기---윈도우 모터',
                    '기타---연료누출(LP가스포함)',
                  ];
                  const stateDetails = Array.from(document.getElementsByClassName('tbl_detail')[0].getElementsByTagName('tr')).splice(1).map(tr => Array.from(tr.getElementsByTagName('span')).filter(span => span.className.indexOf('on') > -1 || span.className.indexOf('active') > -1)).map(spanList => spanList.length > 0 ? spanList[0].innerText : null);
                  for (let i = 0; i < stateDetailsLabels.length; i++) {
                    inspect.stateDetails[stateDetailsLabels[i]] = stateDetails[i];
                  }
                  const comments = document.getElementsByClassName('th_sub');
                  if (comments.length > 0) inspect.comments = (comments[0] as HTMLDivElement).innerText;
                  const sign = Array.from(document.getElementsByClassName('inspc_sign')[0].getElementsByTagName('p')).filter(p => p.className !== 'ckmss').map(p => p.innerText.replace(/(\r\n|\n|\r)/gm, ' ').split(':').reverse()[0]).map(s => s.trim());
                  inspect['중고자동차 성능 상태 점검자'] = sign[0];
                  inspect['중고자동차 성능 상태 고지자'] = sign[1];
                  inspect.inspectionDate = sign[2];
                  return inspect;
                });
                data = Object.assign(data, { inspection: getInspectionDetails });
              }
              data.timestamp = Math.floor(Date.now() / 1000);
              data.options = data.options.map((opt: string) => opt.trim());
              console.log(convertAndInsert(data));
              collectionEncar.insertOne(data, (err: Error, res: any) => {
                if (err) console.log(`MongoDB Error: ${err}`);
                else console.log('Document inserted successfully into MongoDB');
              });
            } catch (error) { console.log('Error navigating to detail page', error); }
          }
        } catch (error) { console.error('Error navigating to list page', error); }
      }
      await browser.close();
    };
    await scrapeEncar(scrapingPageLimit, scrapingLink);
    client.close();
  })();
});


