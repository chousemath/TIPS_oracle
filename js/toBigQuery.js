"use strict";
const { BigQuery } = require('@google-cloud/bigquery');
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
const safeNum = (rawNum) => {
    if (rawNum) {
        return rawNum;
    }
    return 0;
};
const convert = (data) => {
    if (!data) {
        return null;
    }
    ;
    const dcp = data.comprehensiveStatus;
    const comprehensiveStatus = {
        distanceInstrumentationStatus: safeInnerStr(dcp, '주행거리 계기상태'),
        drivingDistanceCondition: safeInnerStr(dcp, '주행거리 상태'),
        vehicleNumberNotation: safeInnerStr(dcp, '차대번호 표기'),
        emissions: safeInnerStr(dcp, '배출가스'),
    };
    const inspection = {
        carInfo: safeStr(data.carInfo),
        comments: safeStr(data.comments),
        inspectionDate: safeStr(data.inspectionDate),
        usedCarPerformanceChecker: '',
        usedCarsPerformanceStatusStudy: '',
        comprehensiveStatus,
    };
    const koPerfCheck = '중고자동차 성능 상태 점검자';
    inspection.usedCarPerformanceChecker = safeStr(data[koPerfCheck]);
    const koPerfStudy = '중고자동차 성능 상태 고지자';
    inspection.usedCarsPerformanceStatusStudy = safeStr(data[koPerfStudy]);
    return {
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
        inspection,
    };
};
