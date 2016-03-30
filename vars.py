#!/usr/local/bin/python
# -*- coding: utf-8 -*-

kAmberStatus = u"状态"   # // 0 待机 1 放电 2 充电
kAmberVoltage = u"电压"
kAmberCapacity = u"容量"
kAmberPower = u"电量百分比"
kAmberHealth = u"健康状态"
kAmberTemperature = u"温度"
kAmberRecycle = u"放电循环"
kAmberWatchCurrent = u"手表电流"
kAmberPhoneCurrent = u"手机电流"

kTemperature = u"温度"
kVoltage = u"电压"
kBatteryFlag = u"Flag"
kBatteryFull = u"电池充满"
kBatteryDischarge = u"电池放电"
kNACapacity = u"Nominal_Available_Capacity"
kFACapacity = u"Full_Available_Capacity"
kRCapacity = u"Remaining_Capacity"
kFCCapacity = u"Full_Charge_Capacity"
kAverageCurrent = u"平均电流"
kStaticCurrent = u"静态电流"
kPowerLevel = u"电量百分比"

kHealth = u"健康状态"
kMaxCurrent = u"最大负载电流"
kAvarageWatchCurrent = u"Watch 平均电流"
kAvaragePhoneCurrent = u"Phone 平均电流"
kWatchCurrent = u"Watch 瞬间电流"
kPhoneCurrent = u"Phone 瞬间电流"
kAmberState = u"状态"
kAmberOpen = u"盖子打开"
kHeatAlert = u"高温警报"
kIceAlert = u"低温警报"
kBatteryFull = u"电池满电"
kBatteryDischarge = u"电池放电"


kSystemStatusRegister = u"System_Status_Register"
kVbusS = u"VBUS_STAT"
kChrgS = u"CHRG_STAT"
kDpmS = u"DPM_STAT"
kPgS = u"PG_STAT"
kThermS = u"THERM_STAT"
kVsysS = u"VSYS_STAT"
kFaultRegister = u"Fault_Register"
kWatchgodFault = u"WATCHDOG_FAULT"
kChrgFault = u"CHRG_FAULT"
kBatFault = u"BAT_FAULT"
kNtcFualt = u"NTC_FUALT"
kSystemError = u"System_Err"

kAmberWhatchFull = u"是否充满"
kAmberWaiting = u"是否在等待" 


orders = [
    # kAmberStatus, # "状态"   # // 0 待机 1 放电 2 充电
    kAmberState,

    kAmberVoltage, # "电压"
    # kAmberCapacity, # "容量"
    kAmberPower, # "电量百分比"
    kAmberHealth, # "健康状态"
    kAmberTemperature, # "温度"
    kAmberRecycle, # "放电循环"
    
    
    kAvarageWatchCurrent, # "Watch 平均电流"
    kAvaragePhoneCurrent, # "Phone 平均电流"
    kWatchCurrent, # "Watch 瞬间电流"
    kPhoneCurrent, # "Phone 瞬间电流"
    # kAmberWatchCurrent, # "手表电流"
    # kAmberPhoneCurrent, # "手机电流"

    kAverageCurrent, # "平均电流"
    kStaticCurrent, # "静态电流"
    kMaxCurrent, # "最大负载电流"

    kBatteryFlag, # "Flag"
    kAmberOpen, # "盖子打开"
    kHeatAlert, # "高温警报"
    kIceAlert, # "低温警报"
    kBatteryFull, # "电池满电"
    kBatteryDischarge, # "电池放电"
    kAmberWhatchFull, # "是否充满"
    kAmberWaiting, # "是否在等待" 

    kNACapacity, # "Nominal_Available_Capacity"
    kFACapacity, # "Full_Available_Capacity"
    kRCapacity, # "Remaining_Capacity"
    kFCCapacity, # "Full_Charge_Capacity"


    kSystemStatusRegister, # "System_Status_Register"
    kVbusS, # "VBUS_STAT"
    kChrgS, # "CHRG_STAT"
    kDpmS, # "DPM_STAT"
    kPgS, # "PG_STAT"
    kThermS, # "THERM_STAT"
    kVsysS, # "VSYS_STAT"
    kFaultRegister, # "Fault_Register"
    kWatchgodFault, # "WATCHDOG_FAULT"
    kChrgFault, # "CHRG_FAULT"
    kBatFault, # "BAT_FAULT"
    kNtcFualt, # "NTC_FUALT"
    kSystemError, # "System_Err"
    
]