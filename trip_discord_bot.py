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

command_templateDICT = {"city": None,
                "area": None,
                "shop": {},
                "updatetime": datetime.datetime.now(),
                "completed": False
                }

reservation_templateDICT = {"people": None,
                "time": None,
                "restaurant_name": {}, #2個值:餐廳name, 能否預約
                "updatetime": datetime.datetime.now(),
                "completed": False
                }

mscDICT = {
    # "userID": {command_templateDICT}
}
# </取得多輪對話資訊>

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))

with open(r"./data/restaurant_domain.json", encoding="UTF-8") as f:
    restaurantDICT = json.load(f)

#增加函式:將json檔內的所有餐廳集中為List
def get_restaurantLIST(jsonfile):
    res_LIST = []
    for city in jsonfile.keys():
        for area in jsonfile[city].keys():
            for name in jsonfile[city][area].keys():
                res_LIST.append(name)
    return res_LIST

#增加函式:取得該餐廳是否能預約
def get_reservation(jsonfile, msgSTR):
    for city in jsonfile.keys():
        for area in jsonfile[city].keys():
            for name in jsonfile[city][area]:
                if name == msgSTR:
                    return (jsonfile[city][area][msgSTR]["預約"])


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
    # if message.channel.name != "bot_test":  這是為了測試用的，不註解掉會無法紀錄及回覆訊息
    #     return

    if not re.search("<@[!&]{}> ?".format(client.user.id), message.content):    # 只有 @Bot 才會回應
        return

    if message.author == client.user:
        return


    print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
    msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
    print("msgSTR =", msgSTR)
    replySTR = ""    # Bot 回應訊息

    RestaurantLIST = get_restaurantLIST(restaurantDICT)   # 這邊透過get_restaurantLIST函式得到包含所有餐廳的list
    lokiResultDICT = getLokiResult(msgSTR)  # 取得 Loki 回傳結果
    if re.search("(hi|hello|哈囉|嗨|[你您]好)", msgSTR.lower()):
        replySTR = "Hi 您好，請問需要什麼服務嗎？"
        await message.reply(replySTR)
        return

    elif re.search("(這附近有什麼(好|可以?)吃的|我想吃(東西|[晚午早]餐))", msgSTR):
        replySTR = "請問您在哪個縣市呢?"
        await message.reply(replySTR)
        return

    ####elif msgSTR in LIST:
    elif msgSTR in RestaurantLIST:
        # if mscDICT[client.user.id] in 更新內容
        mscDICT[client.user.id] = {"people": None,
                                   "time": None,
                                   "restaurant_name": {},  # 2個值:餐廳name, 能否預約
                                   "updatetime": datetime.datetime.now(),
                                   "completed": False
                                   }
        replySTR = "好的您選擇的店家是:[{}]，請問還需要其他服務嗎?".format(msgSTR)
        mscDICT[client.user.id]["restaurant_name"]["name"] = msgSTR
        if get_reservation(jsonfile=restaurantDICT, msgSTR=msgSTR) == "是":  # 判斷該餐廳是否能預約
            mscDICT[client.user.id]["restaurant_name"]["預約"] = "yes"
        else:
            mscDICT[client.user.id]["restaurant_name"]["預約"] = "no"

    elif re.search("(我想要(訂位|預約))", msgSTR):
        if mscDICT[client.user.id]["restaurant_name"]["預約"] == "yes":
            replySTR = "好的,請問幾位?"
        else:
            replySTR = "不好意思，該店家不提供預約服務，請以現場情狀為準。"
            mscDICT[client.user.id]["restaurant_name"] = {}

    elif lokiResultDICT:
        for k in lokiResultDICT.keys():
            if k == "res_person":
                mscDICT[client.user.id]["people"] = lokiResultDICT["res_person"]
                replySTR = "請問大概幾點會到呢?"

##########################################
    # lokiResultDICT = getLokiResult(msgSTR)    # 取得 Loki 回傳結果

    if lokiResultDICT:
        if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
            mscDICT[client.user.id] = {"city": "",
                                       "area": "",
                                       "shop": {},
                                       "updatetime": datetime.datetime.now(),
                                       "completed": False
                                       }
        else:
            datetimeNow = datetime.datetime.now()  # 取得當下時間
            timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
            if timeDIFF.total_seconds() <= 300:  # 以秒為單位，5分鐘以內都算是舊對話
                mscDICT[client.user.id]["updatetime"] = datetimeNow

        for k in lokiResultDICT.keys():
            if k == "city":
                mscDICT[client.user.id]["city"] = lokiResultDICT["city"]
                # confirm_city = lokiResultDICT["city"]
            elif k == "area":
                mscDICT[client.user.id]["area"] = lokiResultDICT["area"]
                # confirm_area = lokiResultDICT["area"]

            # elif k == "res_person":
            #     mscDICT[client.user.id]["people"] = lokiResultDICT["res_person"]

        if mscDICT[client.user.id]["city"] == "" and replySTR == "":
            replySTR = "請問你在哪個縣市呢?"

        elif mscDICT[client.user.id]["area"] == "" and replySTR == "":
            replySTR = "請問您在哪個地區呢?"

        elif mscDICT[client.user.id]["city"] != "" and mscDICT[client.user.id]["area"] != "" and replySTR == "":
            print(restaurantDICT[mscDICT[client.user.id]["city"]][mscDICT[client.user.id]["area"]])
            replySTR = """以下推薦[{}]家餐廳給您，分別為:[{}]。請問有您喜歡的店家嗎?""".format(len(restaurantDICT[mscDICT[client.user.id]["city"]][mscDICT[client.user.id]["area"]].keys()),
                                                                       [i for i in restaurantDICT[mscDICT[client.user.id]["city"]][mscDICT[client.user.id]["area"]].keys()])

        # elif mscDICT[client.user.id]["people"] != None and mscDICT[client.user.id]["time"] == None:
        #     replySTR = "請問大概幾點會到呢?"
    # elif msgSTR in RestaurantLIST:
    #     mscDICT[client.user.id] = {"people": None,
    #                                "time": None,
    #                                "restaurant_name": {},  # 2個值:餐廳name, 能否預約
    #                                "updatetime": datetime.datetime.now(),
    #                                "completed": False
    #                                }
    #     replySTR = "好的您選擇的店家是:[{}]，請問還需要其他服務嗎?".format(msgSTR)
    #     mscDICT[client.user.id]["restaurant_name"]["name"] = msgSTR
        # if restaurantDICT[mscDICT[client.user.id]["city"]][mscDICT[client.user.id]["area"]][msgSTR]["預約"] == "是":
        #     mscDICT[client.user.id]["restaurant_name"]["預約"] = "yes"
        # else:
        #     mscDICT[client.user.id]["restaurant_name"]["預約"] = "no"

    # elif re.search("(我想要(訂位|預約))", msgSTR):


    mscDICT[client.user.id]["completed"] = True
    print("mscDICT =", end=" ")
    pprint(mscDICT)

    # if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
    #     del mscDICT[client.user.id]

    if replySTR:    # 回應 User 訊息
        await message.reply(replySTR)
    return





if __name__ == "__main__":
    client.run(accountDICT["discord_token"])
    # getLokiResult("這附近有什麼吃的，我在台南市，在中西區")