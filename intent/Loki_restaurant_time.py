#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for restaurant_time

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""
import json
from ArticutAPI import ArticutAPI
with open(r"./account.info", encoding="UTF-8") as f:
    accountINFO = json.load(f)

USERNAME = accountINFO["username"]
Articut_key = accountINFO["articut_api_key"]
articut = ArticutAPI.Articut(username=USERNAME, apikey=Articut_key)

import dateparser
DEBUG_restaurant_time = True
userDefinedDICT = {"房間": ["房"], "旅館": ["青年旅館", "飯店", "休息處", "住宿處", "休息的地方"], "預定": ["預約", "訂位", "預訂"], "餐廳": ["餐館", "店家", "吃飯的地方", "吃飯處", "店"]}

def timeSTRConvert(inputSTR):
    resultDICT = {}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT

# def format_identifier(time_STR):
#     if dt.strftime("%p") == "PM":
#         time_STR = time_STR + "PM"
#         dt1 = dateparser.parse(time_STR)
#         time_STR = datetime.strftime(dt1, '%H:%M')
#         return time_STR
#     else:
#         return time_STR

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_restaurant_time:
        print("[restaurant_time] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[預定][上午十點半]":
        datetime = timeSTRConvert(args[1])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "[7]:[46][會]到":
        resultDICT['res_time'] = [args[0] + ":" + args[1]]
        pass

    if utterance == "[七點四十六分]的位子":
        datetime = timeSTRConvert(args[0])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "[我]要[預約][八點]的位子":
        datetime = timeSTRConvert(args[2])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "[預定][9]:[30]":
        resultDICT['res_time'] = [args[1] + ":" + args[2]]
        pass

    if utterance == "[預定][下午五點五十分]到":
        datetime = timeSTRConvert(args[1])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "預計[九點半]到":
        datetime = timeSTRConvert(args[0])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "[預定][大概][上午][11]:[25]到":
        resultDICT['res_time'] = [args[3] + ":" + args[4]]
        pass

    if utterance == "[預約][晚上][7]:[43]的位子":
        resultDICT['res_time'] = [args[2] + ":" + args[3]]
        pass

    if utterance == "[可能][晚上][6]:[35]到":
        resultDICT['res_time'] = [args[2] + ":" + args[3]]
        pass

    if utterance == "[大約][晚上八點]到":
        datetime = timeSTRConvert(args[1])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    if utterance == "大概[下午六點二十分]":
        datetime = timeSTRConvert(args[0])["time"]
        dt = datetime[0][0]["datetime"][-8:-3]
        resultDICT["res_time"] = dt
        pass

    return resultDICT