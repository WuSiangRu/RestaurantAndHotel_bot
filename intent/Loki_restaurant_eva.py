#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for restaurant_eva

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_restaurant_eva = True
userDefinedDICT = {"地區": ["忠孝復興站", "忠孝敦化站", "國父紀念館站", "沙鹿區", "北屯區", "西屯區", "中西區", "東區", "南區"], "房間": ["房"], "新北": ["新北市"], "旅館": ["青年旅館", "飯店", "休息處", "住宿處", "休息的地方"], "臺中": ["台中市", "臺中市", "台中"], "臺北": ["臺北市", "台北", "台北市"], "臺南": ["台南市", "臺南市", "台南"], "預定": ["預約", "訂位"], "餐廳": ["餐館", "店家", "吃飯的地方", "吃飯處", "店"], "高雄": ["高雄市"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_restaurant_eva:
        print("[restaurant_eva] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "這[店家]好嗎":
        # write your code here
        pass

    if utterance == "這家好吃嗎":
        # write your code here
        pass

    if utterance == "這間[食物][好吃]嗎":
        # write your code here
        pass

    if utterance == "這間[餐廳]評價如何":
        # write your code here
        pass

    if utterance == "那這家[餐廳]評價如何啊":
        # write your code here
        pass

    return resultDICT