const {BigQuery} = require('@google-cloud/bigquery');
const safeStr = (rawStr: string): string => {
  if (rawStr) {
    return rawStr;
  }
  return '';
};
const safeInnerStr = (data: any, attrName: string): string => {
  if (data && attrName && data[attrName]) {
    return data[attrName];
  } 
  return '';
};
const safeStrArr = (rawArr: Array<string>): Array<string> => {
  if (rawArr) {
    return rawArr;
  }
  return [];
};
const safeNum = (rawNum: number): number => {
  if (rawNum) {
    return rawNum;
  }
  return 0;
};
interface BQObj {
  // default (most shallow)
  title: string;
  mileage: number;
  year: string;
  fuel: string;
  category: string;
  displacement: string;
  transmission: string;
  color: string;
  plateNumber: string;
  dealerAddress: string;
  dealerSalesInProgress: number;
  dealerSold: number;
  dealerPhoneNumber: string;
  price: number;
  encarNumber: string;
  inquiries: number;
  likes: number;
  inspectionPerformed: boolean;
  scrapedAt: number;
  insuranceReportDate: string;
  vehicleDetails: string;
  options: Array<string>;
  images: Array<string>;
  // inspection
  carInfo: string;
  comments: string;
  usedCarPerformanceChecker: string;
  usedCarsPerformanceStatusStudy: string;
  inspectionDate: string;
  visual: Array<string>;
  // inspection/repairStatus
  accidentHistory: string;
  simpleRepairs: string;
  abnormalConditionBySite1: string
  abnormalConditionBySite2: string
  abnormalConditionBySite3: string
  // inspection/stateDetails
  selfDiagnosisCircuit: string;
  selfDiagnosisTransmission: string;
  motivatorsOperatingStateIdle: string;
  copperOilRockerArmCover: string;
  motorOilCylinderHeadGasket: string;
  motivatorsOilPens: string;
  motivatorOilFlowRate: string;
  driversCooledWaterLeakCylinderHeadGasket: string;
  motorCooledWaterLeakWaterPump: string;
  actuatorCooledWaterLeakRadiator: string;
  driversCooledWaterLeakCooledWaterVolume: string;
  motivatorsHighPressurePumpsCommonRailDieselEngines: string;
  transmissionAutomaticTransmissionATOil: string;
  automaticTransmissionATOilFlowRateAndCondition: string;
  automaticTransmissionATOperatingStatePublic: string;
  powerTransferClutchAssembly: string;
  powerTransferEquivalentJunction: string;
  powerTransferPreshaftAndBear: string;
  steeringPowerHandlingOilLeakage: string;
  steeringOperatingStateSteeringGear: string;
  steeringOperationConditionsSteeringPump: string;
  steeringOperatingStateTierodEndAndBallJoint: string;
  brakeMasterCylinderOilLeakage: string;
  brakeFluidLeak: string;
  brakingDrainageStatus: string;
  electricalGeneratorOutput: string;
  electricalStartMotor: string;
  electricalWipeMotorFunction: string;
  electricsInteriorsTransmissionMotor: string;
  electricalRadiatorFanMotor: string;
  electricalWindowsMotor: string;
  // inspection/comprehensiveStatus
  distanceInstrumentationStatus: string;
  drivingDistanceCondition: string;
  vehicleNumberNotation: string;
  emissions: string;
  tuning: string;
  specialHistory: string;
  reuseChange: string;
  mainOption: string;
}
const convert = (data: any): BQObj | null => {
  if (!data) {
    return null;
  };
  const dcp = data.comprehensiveStatus;
  const drs = data.repairStatus;
  const dsd = data.stateDetails;
  const koPerfCheck = '중고자동차 성능 상태 점검자';
  const koPerfStudy = '중고자동차 성능 상태 고지자';

  const result = {
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
    carInfo: safeStr(data.carInfo),
    comments: safeStr(data.comments),
    inspectionDate: safeStr(data.inspectionDate),
    visual: safeStrArr(data.visual),
    usedCarPerformanceChecker: safeStr(data[koPerfCheck]),
    usedCarsPerformanceStatusStudy: safeStr(data[koPerfStudy]),
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
    accidentHistory: '',
    simpleRepairs: '',
    abnormalConditionBySite1: '',
    abnormalConditionBySite2: '',
    abnormalConditionBySite3: '',
    selfDiagnosisCircuit: '',
    selfDiagnosisTransmission: '',
    motivatorsOperatingStateIdle: '',
    copperOilRockerArmCover: '',
    motorOilCylinderHeadGasket: '',
    motivatorsOilPens: '',
    motivatorOilFlowRate: '',
    driversCooledWaterLeakCylinderHeadGasket: '',
    motorCooledWaterLeakWaterPump: '',
    actuatorCooledWaterLeakRadiator: '',
    driversCooledWaterLeakCooledWaterVolume: '',
    motivatorsHighPressurePumpsCommonRailDieselEngines: '',
    transmissionAutomaticTransmissionATOil: '',
    automaticTransmissionATOilFlowRateAndCondition: '',
    automaticTransmissionATOperatingStatePublic: '',
    powerTransferClutchAssembly: '',
    powerTransferEquivalentJunction: '',
    powerTransferPreshaftAndBear: '',
    steeringPowerHandlingOilLeakage: '',
    steeringOperatingStateSteeringGear: '',
    steeringOperationConditionsSteeringPump: '',
    steeringOperatingStateTierodEndAndBallJoint: '',
    brakeMasterCylinderOilLeakage: '',
    brakeFluidLeak: '',
    brakingDrainageStatus: '',
    electricalGeneratorOutput: '',
    electricalStartMotor: '',
    electricalWipeMotorFunction: '',
    electricsInteriorsTransmissionMotor: '',
    electricalRadiatorFanMotor: '',
    electricalWindowsMotor: '',
  };
  return result;
};
