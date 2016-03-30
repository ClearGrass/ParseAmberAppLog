#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import requests
import re
import json
from parser import parse
from avcloud import AVHeaders
import os

MAX_COUNT = 20
proxyList = [
    "http://52.35.0.16:80",
    "http://165.138.66.247:8080",
    "htpp://130.211.152.162:80",
    "http://198.46.149.175:8080"
]    
currentProxy = 0
            
def main():
    print "-" * 40
    print "You can input following values:"
    print "  1. A serial number of Amber"
    print "  2. A txt Log file name you downloaded"
    print "  3. Input Nothing and press <Enter> will fetch all logs' list"
    print "  4. \"Exti\" for exit the program"
    serialNumber = raw_input("")
    if serialNumber :
        if serialNumber.lower() == "exit":
            print "Exit app"
            exit(0)
        elif not serialNumber.endswith(".txt"):
            print "Look for logs by serial number: " + serialNumber
        else :
            print "parsing ", serialNumber
            parsedFile = parse(serialNumber)
            print "parsed as ", parsedFile
            return
    else :
        print "Listing a logs(max count: %d)" % MAX_COUNT
    logs = getBySerials(serialNumber)
    if logs.get("count") == 0:
    	print "-" * 40
        print "No logs found."
        main()
        return
    print "%d/%d newest logs:" % (len(logs.get("results")), logs.get("count"))
    TITLE = ("#", "Serial Number", "MAC Add", "App Version", "File Size", "Date", "Comment")
    # ROW = "%s\t% 14s\t% 17s\t%s\t%s\t% 24s\t%s"
    ROW = "{:>3} | {:^13} | {:^17} | {:^10} | {:^10} | {:^24} | {:}"
    # print ROW % TITLE
    # print ROW.format("#", "序列号", "MAC 地址", "App 版本", "文件大小", "上传时间", "留言")
    title = ROW.format("#", "Serial No.", "MAC Add", "App Ver", "Size", "Date", "Comment")
    print title
    print "-"*(len(title) + 20)
    for i in range(1, len(logs.get("results")) + 1):
         row = logs.get("results")[i - 1]
         rawFile = row.get("raw_data")
         # print rawFile
         fileSize = rawFile.get("metaData").get("size")
         # print rawFile.get("metaData").get("size")/1024
         # rowInfo = ("%d" % i, row.get("device_sn"), row.get("device_mac"), row.get("device_version"), "%d KB" % (fileSize/1024), row.get("createdAt"), row.get("comment"))
         # print ROW % rowInfo
         print ROW.format("%d" % i, row.get("device_sn"), row.get("device_mac"), row.get("device_version"), "%d KB" % (fileSize/1000), row.get("createdAt"), row.get("comment").encode("utf8"))
     
    print "-"*(len(title) + 20)

    while 1:
        rowNumber = raw_input("Input row number or <Empty>/\"exit\" for exit: ")
        if rowNumber.isdigit() : 
            rowNumber = int(rowNumber)
            if rowNumber == 0:
                break
            try:
            	row = logs.get("results")[rowNumber - 1]
            except Exception, e:
            	continue
            dealRow(row)
        else :
            if rowNumber == "" or rowNumber.lower() == "exit":
                break
            else:
                continue
        pass
    pass


def dealRow(row):
    date = row.get("createdAt")[5: 10]
    rawFile = row.get("raw_data")
    url = rawFile.get("url")
    serial = row.get("device_sn")
    comment = row.get("comment").encode("utf8")
    info = row.get("device_info")

    basePath = serial + "_" + date
    add = 0
    while os.path.exists(basePath + ("" if add == 0 else "_%d" % add)):
        add = add + 1
    basePath  = basePath + ("/" if add == 0 else ("_%d/" % add))
    os.makedirs(basePath)


    print "User said:"
    print comment, "\n"

    cf = open(basePath + serial+"_comment.txt", "w")
    cf.write(comment)
    cf.write("\r\n\r\n\r\n")
    print "Device Info"
    for x in info :
        line = "%s: %s" % (x, info[x])
        print line
        cf.write(line.encode("utf8"))
        cf.write("\r\n")
        pass
    cf.close()

    # return 
    outfile = download(url, basePath + serial+".txt")
    if outfile:
        print "parsing ", outfile
        parsedFile = parse(outfile)
        print "parsed as ", parsedFile
        
    pass

def nextProxyPos():
    global currentProxy
    pos = currentProxy + 1
    if pos >= len(proxyList) :
        pos = 0
    currentProxy = pos

def download(url, fileName):
    global currentProxy
    print "downloading to %s from " % fileName
    print url
    i = len(proxyList) + 1
    while i:
        i = i - 1
        pass
        print "using proxy ", proxyList[currentProxy]
        proxies = {
            "https": proxyList[currentProxy] # "http://165.138.66.247:8080",
        }
        try:
            a = requests.get(url, proxies = proxies)
            with open(fileName, "wb") as downloaded:
                downloaded.write(a.content)
                downloaded.close()
            return fileName
            pass
        except Exception, e:
            print "!!! Try other donwload proxy"
            nextProxyPos()
            continue
        else:
            pass
        
        break
        return
    pass

def getBySerials(serialNumber):
    global AVHeaders
    params = {"count":1, "limit": MAX_COUNT, "order": "-createdAt"}
    if serialNumber :
        params["where"] = json.dumps({"device_sn": '%s'  % serialNumber })
        
    a = requests.get(
        "https://us-api.leancloud.cn/1.1/classes/AppLog",
        headers= AVHeaders,
        params = params
        # params={"skip": 494, "order":"createdAt","count": "1"},   # 282
        # params={"order":"-createdAt", "limit": 3,
        #     "where" : "{\"createdAt\":{\"$gte\":\"2016-01-27 11:18:00\"}}"
        # },
        # json=data
    )
    jsonres = a.json()
    print a.url
    # print json.dumps(jsonres)
    return jsonres
    pass


if __name__ == "__main__":
    # download("https://s3.amazonaws.com/avos-cloud-1azcx2eh1hb9/BGuxf5UNPCJjWF30uexhzIMlSajpE5I1xyxcxvVL.txt", "ttt.txt")

    # exit(0)
    # nextProxyPos()

    # print os.getcwd()

    # date = "2016-02-23T12:41:11.113Z"
    # print date[5: 10]

    # exit(0)

    while  1:
        main()
        pass

    # test()
    pass