"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const { BigQuery } = require('@google-cloud/bigquery');
const bigquery = new BigQuery();
const dotenv_1 = require("dotenv");
dotenv_1.config();
const bqDataSetID = process.env.BQ_DATA_SET_ID;
const bqTableID = process.env.BQ_TABLE_ID;
const safeStr = (rawStr) => {
    if (rawStr) {
        return rawStr;
    }
    return '';
};
const safeInnerStr = (data, attrName) => {
    if (data && attrName && data[attrName]) {
        return data[attrName];
    }
    return '';
};
const safeStrArr = (rawArr) => {
    if (rawArr) {
        return rawArr;
    }
    return [];
};
const safeNum = (rawNum) => {
    if (rawNum) {
        return rawNum;
    }
    return 0;
};
const insertRowsAsStream = async (data) => {
    if (!data) {
        console.log('Object is null');
        return;
    }
    console.log('Inserting into big query..');
    await bigquery
        .dataset(bqDataSetID)
        .table(bqTableID)
        .insert([data]);
    console.log('Finished inserting into big query!');
};
const convert = (data) => {
    if (!data) {
        return null;
    }
    ;
    const insp = data.inspection;
    const dcp = insp ? insp.comprehensiveStatus : null;
    const drs = insp ? insp.repairStatus : null;
    const dsd = insp ? insp.stateDetails : null;
    const koPerfCheck = '중고자동차 성능 상태 점검자';
    const koPerfStudy = '중고자동차 성능 상태 고지자';
    const result = {
        _id: Math.floor(Math.random() * 1000000).toString() + (new Date()).getTime().toString(),
        title: data.title,
        mileage: data.mileage,
        year: data.year,
        fuel: data.fuel,
        category: data.category,
        displacement: data.displacement,
        transmission: data.transmission,
        color: data.color,
        plateNumber: data.plateNumber,
        dealerAddress: data.dealerAddress,
        dealerSalesInProgress: data.dealerSalesInProgress,
        dealerSold: data.dealerSold,
        dealerPhoneNumber: data.dealerPhone.length > 0 ? data.dealerPhone[0] : '',
        price: data.price,
        encarNumber: data.encarNumber,
        inquiries: data.inquiries,
        likes: data.likes,
        inspectionPerformed: data.inspectionPerformed,
        scrapedAt: Math.floor(Date.now() / 1000),
        insuranceReportDate: data.insuranceReportDate,
        vehicleDetails: data.vehicleDetails,
        options: data.options,
        images: data.images,
        // inspection
        carInfo: safeStr(insp.carInfo),
        comments: safeStr(insp.comments),
        inspectionDate: safeStr(insp.inspectionDate),
        visual: safeStrArr(insp.visual),
        usedCarPerformanceChecker: safeStr(insp[koPerfCheck]),
        usedCarsPerformanceStatusStudy: safeStr(insp[koPerfStudy]),
        // inspection/comprehensiveStatus
        distanceInstrumentationStatus: safeInnerStr(dcp, '주행거리 계기상태'),
        drivingDistanceCondition: safeInnerStr(dcp, '주행거리 상태'),
        vehicleNumberNotation: safeInnerStr(dcp, '차대번호 표기'),
        emissions: safeInnerStr(dcp, '배출가스'),
        tuning: safeInnerStr(dcp, '튜닝'),
        specialHistory: safeInnerStr(dcp, '특별이력'),
        reuseChange: safeInnerStr(dcp, '용도변경'),
        mainOption: safeInnerStr(dcp, '주요옵션'),
        // inspection/repairStatus
        accidentHistory: safeInnerStr(drs, '사고이력'),
        simpleRepairs: safeInnerStr(drs, '단순수리'),
        abnormalConditionBySite1: safeInnerStr(drs, '부위별 이상여부---1'),
        abnormalConditionBySite2: safeInnerStr(drs, '부위별 이상여부---2'),
        abnormalConditionBySite3: safeInnerStr(drs, '부위별 이상여부---3'),
        // inspection/stateDetails
        selfDiagnosisCircuit: safeInnerStr(dsd, '자기진단---원동기'),
        selfDiagnosisTransmission: safeInnerStr(dsd, '자기진단---변속기'),
        motivatorsOperatingStateIdle: safeInnerStr(dsd, '원동기---작동상태(공회전)'),
        copperOilRockerArmCover: safeInnerStr(dsd, '원동기---오일누유---로커암 커버'),
        motorOilCylinderHeadGasket: safeInnerStr(dsd, '원동기---오일누유---실린더 헤드/가스켓'),
        motivatorsOilPens: safeInnerStr(dsd, '원동기---오일누유---오일펜'),
        motivatorOilFlowRate: safeInnerStr(dsd, '원동기---오일유량'),
        driversCooledWaterLeakCylinderHeadGasket: safeInnerStr(dsd, '원동기---냉각수누수---실린더 헤드/가스켓'),
        motorCooledWaterLeakWaterPump: safeInnerStr(dsd, '원동기---냉각수누수---워터펌프'),
        actuatorCooledWaterLeakRadiator: safeInnerStr(dsd, '원동기---냉각수누수---라디에이터'),
        driversCooledWaterLeakCooledWaterVolume: safeInnerStr(dsd, '원동기---냉각수누수---냉각수수량'),
        motivatorsHighPressurePumpsCommonRailDieselEngines: safeInnerStr(dsd, '원동기---고압펌프(커먼레일)-디젤엔진'),
        transmissionAutomaticTransmissionATOil: safeInnerStr(dsd, '변속기---자동변속기(A/T)---오일누유'),
        automaticTransmissionATOilFlowRateAndCondition: safeInnerStr(dsd, '변속기---자동변속기(A/T)---오일유량 및 상태'),
        automaticTransmissionATOperatingStatePublic: safeInnerStr(dsd, '변속기---자동변속기(A/T)---작동상태(공회)'),
        powerTransferClutchAssembly: safeInnerStr(dsd, '동력전달---클러치 어셈블리'),
        powerTransferEquivalentJunction: safeInnerStr(dsd, '동력전달---등속죠인트'),
        powerTransferPreshaftAndBear: safeInnerStr(dsd, '동력전달---추진축 및 베어'),
        steeringPowerHandlingOilLeakage: safeInnerStr(dsd, '조향---동력조향작동 오일 누유'),
        steeringOperatingStateSteeringGear: safeInnerStr(dsd, '조향---작동상태---스티어링기어'),
        steeringOperationConditionsSteeringPump: safeInnerStr(dsd, '조향---작동상태---스티어링펌프'),
        steeringOperatingStateTierodEndAndBallJoint: safeInnerStr(dsd, '조향---작동상태---타이로드엔드 및 볼 죠인트'),
        brakeMasterCylinderOilLeakage: safeInnerStr(dsd, '제동---브레이크 마스터 실린더오일 누유'),
        brakeFluidLeak: safeInnerStr(dsd, '제동---브레이크 오일 누유'),
        brakingDrainageStatus: safeInnerStr(dsd, '제동---배력장치 상태'),
        electricalGeneratorOutput: safeInnerStr(dsd, '전기---발전기 출력'),
        electricalStartMotor: safeInnerStr(dsd, '전기---시동 모터'),
        electricalWipeMotorFunction: safeInnerStr(dsd, '전기---와이퍼 모터 기능'),
        electricsInteriorsTransmissionMotor: safeInnerStr(dsd, '전기---실내송풍 모터'),
        electricalRadiatorFanMotor: safeInnerStr(dsd, '전기---라디에이터 팬 모터'),
        electricalWindowsMotor: safeInnerStr(dsd, '전기---윈도우 모터'),
    };
    return result;
};
const convertAndInsert = async (data) => {
    if (!data) {
        return;
    }
    try {
        await insertRowsAsStream(convert(data));
    }
    catch (e) {
        console.log('BigQuery Error:', e.message);
    }
};
module.exports = {
    convertAndInsert,
};
