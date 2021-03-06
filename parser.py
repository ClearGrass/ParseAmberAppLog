#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import requests
import re
from vars import *

def test() :
	print "TEST"

def parse(fileName):
    outFileName = fileName[:-3] + "csv"
    infile = file(fileName)
    i = 0

    results = {}
    timeList = []
    lastTime = 0
    while 1:
        i = i + 1
        line = infile.readline()
        if not line:
            break
        if (i == 1) :
            continue;
        
        row = line.strip().split(',')
        rowData = (time, data, flag, appVersion, supportApp, firmware, unixTime)= (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        unixTime = int(unixTime)
        if abs(lastTime - unixTime) < 2 :
            unixTime = lastTime
        else :
            lastTime = unixTime
        parsed = parseMainData(data)
        valueUnderTime = results.get(unixTime, {})
        if parsed:

            valueUnderTime.update(parsed)
            valueUnderTime["时间"] = time
            pass

        results[unixTime] = valueUnderTime
        if len(timeList) == 0 or timeList[len(timeList) - 1] != lastTime :
            timeList.append(lastTime)

        # print a
        # return
        pass # do nothing

    infile.close()    
    # return 
    toFile = file(outFileName, "w")
    toFile.write(u"时间".encode("gbk"))
    for k in orders:
        toFile.write(",")
        toFile.write(k.encode("gbk"))
    toFile.write("\n")
    for time in timeList :
        toFile.write(results.get(time).get("时间"))
        for k in orders:
            toFile.write(",")
            row = results.get(time)
            # print k

            # for k in row :
            #     print k, row.get(k)
            # toFile.write("0")
            value = row.get(k)
            toFile.write(str(value))
        toFile.write("\n")
    toFile.close()
    return outFileName
    pass

def main():

    pass


def parseMainData(data) :
    data = re.sub(r"\W", "", data) 
    flag = int(getFlag(data), 16)
    mapRes = dataToMap(data, flag)
    return mapRes

def getFlag(data):
    return  data[0:2]

def dataToMap(data, flag) :
    maper = getMaperByFlag(flag)
    mapRes = getMapByMaper(data, maper)
    return mapRes
    pass

def getMapByMaper(data, maper):
    res = {}
    # print data
    if maper:
        for k, r in maper.iteritems() :
            slict = data[r.start: r.end]
            value = r.value(slict)
            res[k] = value
        return res
        pass
    
    pass

def dealFinalValue(value):
    return value
    pass



def MakeRange(p1, p2, negative = False, multiple = 1, hexv = False, func = None) :
    return Range(p1, p2, negative, multiple, hexv, func)

def getMaperByFlag(flag) :
    # print "flag", flag, 0xd0, 0xd1, 0xd2
    if flag == 1 :
        return {
            kAmberStatus: MakeRange(5, 1 , func = createFunctionBy([
                (0, "待机".decode("utf-8").encode("gbk"))
                , (2, "充电".decode("utf-8").encode("gbk"))
                , (3, "放电".decode("utf-8").encode("gbk"))
                , (4, "充放电".decode("utf-8").encode("gbk"))
                ])),
            kAmberVoltage: MakeRange(6, 2, multiple= 0.001),
            kAmberCapacity: MakeRange(8, 2),
            kAmberPower: MakeRange(10, 1),
            kAmberHealth: MakeRange(11, 1),
            kAmberTemperature: MakeRange(12, 2, negative = True, multiple= 0.1),
            kAmberRecycle: MakeRange(14, 2),
            kAmberWatchCurrent: MakeRange(16, 2),
            kAmberPhoneCurrent: MakeRange(18, 2),        
            kAmberWaiting: MakeRange(1, 1),
            kAmberWhatchFull: MakeRange(2, 1),
        }
        pass
    elif flag == 0xd0 :
        batteryFlag = MakeRange(5, 2)
        batteryFlag.hex = True
        return {
            kTemperature: MakeRange(1, 2, negative = True, multiple = 0.1),
            kVoltage: MakeRange(3, 2, multiple = 0.001),
            kBatteryFlag: batteryFlag,
            kNACapacity: MakeRange(7, 2),
            kFACapacity: MakeRange(9, 2),
            kRCapacity: MakeRange(11, 2),
            kFCCapacity: MakeRange(13, 2),
            kAverageCurrent: MakeRange(15, 2, negative = True),
            kStaticCurrent: MakeRange(17, 2, negative = True),
            kPowerLevel: MakeRange(19, 1),
        }
        pass
    elif flag == 0xd1 :
        return {
            kHealth: MakeRange(1, 1),
            kMaxCurrent: MakeRange(2, 2, negative = True),
            kAvarageWatchCurrent: MakeRange(4, 2),
            kAvaragePhoneCurrent: MakeRange(6, 2),
            kWatchCurrent: MakeRange(8, 2),
            kPhoneCurrent: MakeRange(10, 2),
            kAmberOpen: MakeRange(15, 1),
            kHeatAlert: MakeRange(16, 1),
            kIceAlert: MakeRange(17, 1),
            kBatteryFull: MakeRange(18, 1),
            kBatteryDischarge: MakeRange(19, 1),
        }
        pass
    elif flag == 0xd2 :
        return {
            kSystemStatusRegister : MakeRange(1, 1, hexv = True),
            kVbusS : MakeRange(2, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Unknown")
                , ("0x01", "USB host")
                , ("0x02", "Adapter port")
                , ("0x03", "OTG")
                ])),
            kChrgS : MakeRange(3, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Not Charging")
                , ("0x01", "Pre-charge")
                , ("0x02", "Fast Charging")
                , ("0x03", "Charge Termination Done")
                ])),
            kDpmS : MakeRange(4, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Not DPM")
                , ("0x01", "VINDPM or IINDPM")
                ])),
            kPgS : MakeRange(5, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Not Power Good")
                , ("0x01", "Power Good")
                ])),
            kThermS : MakeRange(6, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Normal")
                , ("0x01", "In Thermal Regulation")
                ])),
            kVsysS : MakeRange(7, 1, hexv = True, func = createFunctionBy([
                ("0x00", "BAT>VSYSMIN")
                , ("0x01", "BAT<VSYSMIN")
                ])),
            kFaultRegister : MakeRange(8, 1, hexv = True),
            kWatchgodFault : MakeRange(9, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Normal")
                , ("0x01", "Watchdog timer expiration")
                ])),
            kChrgFault : MakeRange(10, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Normal")
                , ("0x01", "Input fault")
                , ("0x02", "Thermal shutdown")
                , ("0x03", "Charge Safety Timer Expiration")
                ])),
            kBatFault : MakeRange(11, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Normal")
                , ("0x01", "BATOVP")
                ])),
            kNtcFualt : MakeRange(12, 1, hexv = True, func = createFunctionBy([
                ("0x00", "Normal")
                , ("0x01", "Cold")
                , ("0x02", "Hot")
                ])),
            kSystemError : MakeRange(13, 4, hexv = True),
            # kAmberRecycle: MakeRange(17, 2),
        }
        pass
    else :
        pass
    pass
def createFunctionBy(couples):
    def theFunction(thevalue):
        for (value, string) in couples:
            if thevalue == value :
                return "%s(%s)" % (string, value)
            pass
        return thevalue
        pass
    return theFunction

class Range(object):
    """docstring for Range"""

    def __init__(self, start, length, negative = False, multiple = 1, hexv = False, func = None):
        super(Range, self).__init__()
        self.start = start * 2
        self.length = length
        self.end = self.start + length * 2
        self.negative = negative
        self.multiple = multiple
        self.hex = hexv
        self.func = func
    def value(self, hexV):
        if self.hex:
            thevalue = "0x" + hexV
        else :
            INT8_MAX   =       0x7F
            UINT8_MAX  =       0xff
            INT16_MAX  =     0x7fff
            UINT16_MAX =     0xffff
            INT32_MAX  = 0x7fffffff
            UINT32_MAX = 0xffffffff
            INT64_MAX  = 0x7fffffffffffffff
            v = int(hexV, 16)
            length = self.length
            if self.negative : 
                maxV = INT8_MAX if length == 1 else (INT16_MAX if length == 2 else (INT32_MAX if length == 4 else INT64_MAX))
                if v > maxV :
                    x = UINT8_MAX + 1 if length == 1 else (UINT16_MAX + 1 if length == 2 else (UINT32_MAX + 1 if length == 4 else  0))
                    v = int(v - x)
            thevalue = v * self.multiple
        if self.func != None :
            thevalue = self.func(thevalue)
        return thevalue
        
if __name__ == "__main__":
    # main()
    parse("9AF136749073_04-23/9AF136749073.txt")
    pass
