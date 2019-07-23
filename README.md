# TIPS Oracle

### Usage Instructions

* You need to get the `bigquery-key.json` file from your technical lead in order to access your BigQuery instance

```bash
# If you want to edit the encar scraper...
$ npm run watch # start the typescript auto compiler
# Edit src/encardata.ts
# If you want to run the encar data script
$ cd js
$ node encardata.js # for domestic vehicles
$ node encardata.js -c foreign # for foreign vehicles
```

```bash
# on your cloud server, install forever js
$ npm install forever -g
$ cd js
$ chmod +x scrape.sh # give execution permission to the scraping script
$ ./scrape.sh # run several instances of the scraping script
$ forever list # check to make sure your processes are ok
```
