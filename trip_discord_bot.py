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

    try:
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
                mscDICT[client.user.id] = {"credit": {},
                                           "mortgage": {},
                                           "loan_type": "credit",
                                           "updatetime": datetime.now(),
                                           "completed": False}
            else:
                datetimeNow = datetime.now()  # 取得當下時間
                timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
                if timeDIFF.total_seconds() <= 300:  # 以秒為單位，5分鐘以內都算是舊對話
                    mscDICT[client.user.id]["updatetime"] = datetimeNow

            for k in lokiResultDICT:    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
                if k == "credit":
                    for c in lokiResultDICT["credit"]:
                        mscDICT[client.user.id]["credit"][c] = lokiResultDICT["credit"][c]
                        mscDICT[client.user.id]["mortgage"][c] = lokiResultDICT["credit"][c]
                elif k == "mortgage":
                    for m in lokiResultDICT["mortgage"]:
                        mscDICT[client.user.id]["mortgage"][m] = lokiResultDICT["mortgage"][m]
                elif k == "msg":
                    replySTR = lokiResultDICT[k]
                    if "loan_type" in lokiResultDICT:
                        mscDICT[client.user.id]["loan_type"] = lokiResultDICT["loan_type"]
                    if mscDICT[client.user.id]["credit"] == {} and mscDICT[client.user.id]["mortgage"] == {}:
                        replySTR += "\n請問您從事什麼工作呢？"
                    print("Loki msg:", replySTR, "\n")
                elif k == "confirm":
                    if lokiResultDICT["confirm"]:
                        replySTR = "好的，謝謝。"
                    else:
                        replySTR = "請問您的意思是？"

            if mscDICT[client.user.id]["loan_type"] == "credit" and replySTR == "":    # Credit 多輪對話的問句。
                if "job" not in mscDICT[client.user.id]["credit"]:
                    replySTR = "請問您從事什麼工作呢？"
                elif "job_year" not in mscDICT[client.user.id]["credit"]:
                    replySTR = "請問您從事 [{}] 多久了呢？".format(mscDICT[client.user.id]["credit"]["job"])
                elif "annual_income" not in mscDICT[client.user.id]["credit"]:
                    replySTR = "請問您個人的年收入大概是多少呢？"
                elif "education" not in mscDICT[client.user.id]["credit"]:
                    replySTR = "請問您的教育程度是？"

            if set(creditTemplate.keys()).difference(mscDICT[client.user.id]["credit"]) == set() and mscDICT[client.user.id]["loan_type"] == "credit":
                replySTR = """感謝您的幫忙。和您確認以下個人信貸的申請資料…
                              您從事的是 [{}]，已經有 [{}] 的經驗了，目前年收入約 [{}] 元。
                              如果以上正確的話，我們將在這兩天內與您聯絡。""".format(mscDICT[client.user.id]["credit"]["job"],
                                                                                     mscDICT[client.user.id]["credit"]["job_year"],
                                                                                     mscDICT[client.user.id]["credit"]["annual_income"]).replace("    ", "")
                mscDICT[client.user.id]["completed"] = True

            if mscDICT[client.user.id]["loan_type"] == "mortgage" and replySTR == "":    # Mortgage 多輪對話的問句。
                if "job" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您從事什麼工作呢？"
                elif "job_year" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您從事 [{}] 多久了呢？".format(mscDICT[client.user.id]["mortgage"]["job"])
                elif "annual_income" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您個人的年收入大概是多少呢？"
                elif "education" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您的教育程度是？"
                elif "address" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您的地址是？"
                elif "floor_size" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問房屋的坪數是？"
                elif "year" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問屋齡是幾年？"
                elif "type" not in mscDICT[client.user.id]["mortgage"]:
                    replySTR = "請問您的房屋的類型是？"

            if set(mortgageTemplate.keys()).difference(mscDICT[client.user.id]["mortgage"]) == set() and mscDICT[client.user.id]["loan_type"] == "mortgage":
                replySTR = """感謝您的幫忙。和您確認以下個人房貸的申請資料…
                              您從事的是 [{}]，已經有 [{}] 的經驗了，目前年收入約 [{}] 元;
                              房屋的地址是 [{}]、坪數為 [{}]，屋齡是 [{}]，房屋的類型是 [{}]。
                              如果以上正確的話，我們將在這兩天內與您聯絡。""".format(mscDICT[client.user.id]["mortgage"]["job"],
                                                                                     mscDICT[client.user.id]["mortgage"]["job_year"],
                                                                                     mscDICT[client.user.id]["mortgage"]["annual_income"],
                                                                                     mscDICT[client.user.id]["mortgage"]["address"],
                                                                                     mscDICT[client.user.id]["mortgage"]["floor_size"],
                                                                                     mscDICT[client.user.id]["mortgage"]["year"],
                                                                                     mscDICT[client.user.id]["mortgage"]["type"]).replace("    ", "")
                mscDICT[client.user.id]["completed"] = True

        print("mscDICT =")
        pprint(mscDICT)

        if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
            del mscDICT[client.user.id]

        if replySTR:    # 回應 User 訊息
            await message.reply(replySTR)
        return

    except Exception as e:
        logging.error("[MSG ERROR] {}".format(str(e)))
        print("[MSG ERROR] {}".format(str(e)))





if __name__ == "__main__":
    client.run(accountDICT["discord_token"])

    getLokiResult("我想辦房屋貸款，我是一位會計師")