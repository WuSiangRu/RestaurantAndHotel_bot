#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
import datetime

from RestaurantAndHotel_bot import runLoki
from pprint import pprint


logging.basicConfig(level=logging.CRITICAL)

# <取得多輪對話資訊>
client = discord.Client()

templateDICT = {"city": None,
                "area": None,
                "shop": {},
                }
"""
creditTemplate = {"annual_income": "",
                 "education": "",
                 "job": "",
                 "job_year": ""}

mortgageTemplate = {"annual_income": "",
                    "education": "",
                    "job": "",
                    "job_year": "",
                    "address": "",
                    "floor_size": "",
                    "year": "",
                    "type": ""}
"""
mscDICT = {
    # "userID": {templateDICT}
}
# </取得多輪對話資訊>

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))

with open(r"./data/restaurant_domain.json", encoding="UTF-8") as f:
    restaurantDICT = json.load(f)

punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Loki Result => {}".format(resultDICT))
    return resultDICT



@client.event
async def on_ready():
    logging.info("[READY INFO] {} has connected to Discord!".format(client.user))
    print("[READY INFO] {} has connected to Discord!".format(client.user))


@client.event
async def on_message(message):
    if message.channel.name != "bot_test":
        return

    if not re.search("<@[!&]{}> ?".format(client.user.id), message.content):    # 只有 @Bot 才會回應
        return

    if message.author == client.user:
        return


    print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
    msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
    print("msgSTR =", msgSTR)
    replySTR = ""    # Bot 回應訊息

    if re.search("(hi|hello|哈囉|嗨|[你您]好)", msgSTR.lower()):
        replySTR = "Hi 您好，請問需要什麼服務嗎？"
        await message.reply(replySTR)
        return

    elif re.search("(這附近有什麼[好可以]吃的|我想吃[東西晚餐午餐早餐])"):
        replySTR = "請問您在哪個縣市呢?"
        await message.reply(replySTR)
        return

    lokiResultDICT = getLokiResult(msgSTR)    # 取得 Loki 回傳結果

    if lokiResultDICT:
        if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
            mscDICT[client.user.id] = {"city": "",
                                       "area": "",
                                       "shop": {},
                                       "updatetime": datetime.now(),
                                       "completed": False}
        else:
            datetimeNow = datetime.now()  # 取得當下時間
            timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
            if timeDIFF.total_seconds() <= 300:  # 以秒為單位，5分鐘以內都算是舊對話
                mscDICT[client.user.id]["updatetime"] = datetimeNow
        confirm_city = ""
        confirm_area = ""
        for k in lokiResultDICT.keys():
            if k == "city":
                mscDICT[client.user.id]["city"] = lokiResultDICT["city"]
                confirm_city = lokiResultDICT["city"]
            elif k == "area":
                mscDICT[client.user.id]["area"] = lokiResultDICT["area"]
                confirm_area = lokiResultDICT["area"]
        if mscDICT[client.user.id]["city"] == "" and replySTR == "":
            replySTR = "請問你在哪個縣市呢?"

        elif mscDICT[client.user.id]["area"] == "" and replySTR == "":
            replySTR = "請問您在哪個地區呢?"

        elif mscDICT[client.user.id]["city"] != "" and mscDICT[client.user.id]["area"] != "" and replySTR == "":
            replySTR = """以下推薦[{}]家餐廳給您，
                        分別為:[{}]。
                        請問有您喜歡的店家嗎?""".format(len(restaurantDICT[confirm_city][confirm_area].keys()), restaurantDICT[confirm_city][confirm_area].keys())

            mscDICT[client.user.id]["completed"] = True
    print("mscDICT =")
    pprint(mscDICT)

    if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
        del mscDICT[client.user.id]

    if replySTR:    # 回應 User 訊息
        await message.reply(replySTR)
    return





if __name__ == "__main__":
    client.run(accountDICT["discord_token"])
    # getLokiResult("這附近有什麼吃的，我在台南市，在中西區")