# RestaurantAndHotel_bot - 幫你推薦在地美食的機器人

## **背景**
你是否開開心心規劃要到外縣市遊玩時，雖然有大概查過資料，但還是有些隱藏的在地小吃想要嘗試，卻不知道要從何下手?
即使聽過該餐廳，但對該店的評價及住址還是有所不確定，又不想花時間看網路上大量的評價是不是適合自己。
只要在Discord上加入RestaurantAndHotel_bot，就能以自然語言找尋你要的餐廳的資訊喔。

## **專案列表**
+ 目錄
+ 環境建立
+ 使用說明
+ 使用者輸入範例
+ 作者

## **目錄**
RestaurantAndHotel_bot的Repository包含以下內容：

1. Data
2. Discord
3. ref
4. RestaurantAndHotel_bot

## **環境建立**
### **註冊帳號**
1. 請到 [卓騰語言科技](https://api.droidtown.co/) 官方網站註冊帳號並登入頁面
2. 註冊會員

![](https://raw.githubusercontent.com/WuSiangRu/RestaurantAndHotel_bot/main/pic/001.JPG "001")
3. 註冊成功後登入會員

![](https://raw.githubusercontent.com/WuSiangRu/RestaurantAndHotel_bot/main/pic/002.JPG "002")
4. 登入會員之後，選擇在「服務資訊」區塊底下第四個圖示進入Loki應用

![](https://raw.githubusercontent.com/WuSiangRu/RestaurantAndHotel_bot/main/pic/003.JPG "003")

`使用本專案python環境建議版本3.6+`
1. 安裝該專案會使用的module
```
pip install ArticutAPI
```

## **使用說明**
### **Articut及Loki使用說明**
+ 登入帳號:[卓騰語言科技](https://api.droidtown.co/)
+ 複製Articut API金鑰
+ 選擇Loki應用後建立專案(英文名稱)
+ 複製Loki專案金鑰
+ 編輯`account.json`
    + username:輸入註冊帳號
    + articut_api_key:輸入複製的Articut API金鑰
    + loki_api_key:輸入複製的Loki專案金鑰

### **Discord使用說明**
#### **使用檔案**
1. intent
2. bot_for_loki
3. discord_bot
#### **環境設定**
+ python版本
    + python版本建議3.6+
+ 所需module
    + [Discord](https://pypi.org/project/discord.py/)
    
    `pip install -U discord.py`
#### **建立Discord bot**
如何建立Discord bot請參考 [How to Make a Discord Bot in Python](https://realpython.com/how-to-make-a-discord-bot-python/)
+ 使用Discord來使用RestaurantAndHotel_bot，請點選 Discord 資料夾以瀏覽詳細說明。
+ 要直接使用已建立好的Loki意圖，請點選 ref 資料夾瀏覽詳細說明。

