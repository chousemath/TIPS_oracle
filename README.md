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

### MongoDB to BigQuery Mappings for `inspection`

* `중고자동차 성능 상태 점검자` => `usedCarPerformanceChecker`
* `중고자동차 성능 상태 고지자` => `usedCarsPerformanceStatusStudy`

### MongoDB to BigQuery Mappings for `inspection/comprehensiveStatus`

* `주행거리 계기상태` => `distanceInstrumentationStatus`
* `주행거리 상태` => `drivingDistanceCondition`
* `차대번호 표기` => `vehicleNumberNotation`
* `배출가스` => `emissions`
* `튜닝` => `tuning`
* `특별이력` => `specialHistory`
* `용도변경` => `reuseChange`
* `색상` => `color`
* `주요옵션` => `mainOption`

### MongoDB to BigQuery Mappings for `inspections/repairStatus`

* `사고이력` => `accidentHistory`
* `단순수리` => `simpleRepairs`
* `부위별 이상여부---1` => `abnormalConditionBySite1`
* `부위별 이상여부---2` => `abnormalConditionBySite2`
* `부위별 이상여부---3` => `abnormalConditionBySite3`

### MongoDB to BigQuery Mappings for `inspections/stateDetails`

* `자기진단---원동기` => `selfDiagnosisCircuit`
* `자기진단---변속기` => `selfDiagnosisTransmission`
* `원동기---작동상태(공회전)` => `motivatorsOperatingStateIdle`
* `원동기---오일누유---로커암 커버` => `copperOilRockerArmCover`
* `원동기---오일누유---실린더 헤드/가스켓` => `motorOilCylinderHeadGasket`
* `원동기---오일누유---오일펜` => `motivatorsOilPens`
* `원동기---오일유량` => `motivatorOilFlowRate`
* `원동기---냉각수누수---실린더 헤드/가스켓` => `driversCooledWaterLeakCylinderHeadGasket`
* `원동기---냉각수누수---워터펌프` => `motorCooledWaterLeakWaterPump`
* `원동기---냉각수누수---라디에이터` => `actuatorCooledWaterLeakRadiator`
* `원동기---냉각수누수---냉각수수량` => `driversCooledWaterLeakCooledWaterVolume`
* `원동기---고압펌프(커먼레일)-디젤엔진` => `motivatorsHighPressurePumpsCommonRailDieselEngines`
* `변속기---자동변속기(A/T)---오일누유` => `transmissionAutomaticTransmissionATOil`
* `변속기---자동변속기(A/T)---오일유량 및 상태` => `automaticTransmissionATOilFlowRateAndCondition`
* `변속기---자동변속기(A/T)---작동상태(공회)` => `automaticTransmissionATOperatingStatePublic`
* `동력전달---클러치 어셈블리` => `powerTransferClutchAssembly`
* `동력전달---등속죠인트` => `powerTransferEquivalentJunction`
* `동력전달---추진축 및 베어` => `powerTransferPreshaftAndBear`
* `조향---동력조향작동 오일 누유` => `steeringPowerHandlingOilLeakage`
* `조향---작동상태---스티어링기어` => `steeringOperatingStateSteeringGear`
* `조향---작동상태---스티어링펌프` => `steeringOperationConditionsSteeringPump`
* `조향---작동상태---타이로드엔드 및 볼 죠인트` => `steeringOperatingStateTierodEndAndBallJoint`
* `제동---브레이크 마스터 실린더오일 누유` => `brakeMasterCylinderOilLeakage`
* `제동---브레이크 오일 누유` => `brakeFluidLeak`
* `제동---배력장치 상태` => `brakingDrainageStatus`
* `전기---발전기 출력` => `electricalGeneratorOutput`
* `전기---시동 모터` => `electricalStartMotor`
* `전기---와이퍼 모터 기능` => `electricalWipeMotorFunction`
* `전기---실내송풍 모터` => `electricsInteriorsTransmissionMotor`
* `전기---라디에이터 팬 모터` => `electricalRadiatorFanMotor`
* `전기---윈도우 모터` => `electricalWindowsMotor`


















 

















