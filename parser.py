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
    toFile.write(u"时间".encode("utf8"))
    for k in orders:
        toFile.write(",")
        toFile.write(k.encode("utf8"))
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
            # print k , slict, value, r.start, r.end
            res[k] = value
        return res
        pass
    
    pass




def MakeRange(p1, p2, negative = False, multiple = 1, hexv = False) :
    return Range(p1, p2, negative, multiple, hexv)

def getMaperByFlag(flag) :
    # print "flag", flag, 0xd0, 0xd1, 0xd2
    if flag == 1 :
        return {
            kAmberStatus: MakeRange(5, 1),
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
            kAmberState: MakeRange(14, 1),
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
            kVbusS : MakeRange(2, 1, hexv = True),
            kChrgS : MakeRange(3, 1, hexv = True),
            kDpmS : MakeRange(4, 1, hexv = True),
            kPgS : MakeRange(5, 1, hexv = True),
            kThermS : MakeRange(6, 1, hexv = True),
            kVsysS : MakeRange(7, 1, hexv = True),
            kFaultRegister : MakeRange(8, 1, hexv = True),
            kWatchgodFault : MakeRange(9, 1, hexv = True),
            kChrgFault : MakeRange(10, 1, hexv = True),
            kBatFault : MakeRange(11, 1, hexv = True),
            kNtcFualt : MakeRange(12, 1, hexv = True),
            kSystemError : MakeRange(13, 4, hexv = True),
            kAmberRecycle: MakeRange(17, 2, hexv = True),
        }
        pass
    else :
        pass
    pass


class Range(object):
    """docstring for Range"""

    def __init__(self, start, length, negative = False, multiple = 1, hexv = False):
        super(Range, self).__init__()
        self.start = start * 2
        self.length = length
        self.end = self.start + length * 2
        self.negative = negative
        self.multiple = multiple
        self.hex = hexv
    def value(self, hexV):
        if self.hex:
            return "0x" + hexV
        INT8_MAX =         0x7F
        UINT8_MAX =        0xff
        INT16_MAX =      0x7fff
        UINT16_MAX =     0xffff
        INT32_MAX =  0x7fffffff
        UINT32_MAX = 0xffffffff
        INT64_MAX = 0x7fffffffffffffff
        v = int(hexV, 16)
        length = self.length
        if self.negative : 
            maxV = INT8_MAX if length == 1 else (INT16_MAX if length == 2 else (INT32_MAX if length == 4 else INT64_MAX))
            if v > maxV :
                x = UINT8_MAX + 1 if length == 1 else (UINT16_MAX + 1 if length == 2 else (UINT32_MAX + 1 if length == 4 else  0))
                v = int(v - x)
        return v * self.multiple
        
if __name__ == "__main__":
    # main()
    parse("8DC738557637_03-19/8DC738557637.txt")
    pass
