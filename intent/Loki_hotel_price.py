#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for hotel_price

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_hotel_price = True
userDefinedDICT = {"房間": ["房"], "新北": ["新北市"], "旅館": ["青年旅館", "飯店", "休息處", "住宿處", "休息的地方"], "臺中": ["台中市", "臺中市", "台中"], "臺北": ["臺北市", "台北", "台北市"], "臺南": ["台南市", "臺南市", "台南"], "預定": ["預約", "訂位"], "餐廳": ["餐館", "店家", "吃飯的地方", "吃飯處", "店"], "高雄": ["高雄市"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_hotel_price:
        print("[hotel_price] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "住[1個][晚上]要多少":
        # write your code here
        pass

    if utterance == "住[2天]要花多少":
        # write your code here
        pass

    if utterance == "住[一][晚]要多少":
        # write your code here
        pass

    if utterance == "住[一][晚]要多少錢":
        # write your code here
        pass

    if utterance == "這間[旅館][一][晚]要多少":
        # write your code here
        pass

    if utterance == "這間[旅館]住[兩][晚]要多少錢":
        # write your code here
        pass

    return resultDICT