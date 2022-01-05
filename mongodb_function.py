import pymongo
import re
import datetime


client = pymongo.MongoClient("mongodb+srv://Eddie:Eddie29888788@cluster0.4rjpi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#第一個db的建立
db = client['MongoClient']
col = db['Database']

print(client.database_names())#列出client中的資料庫名稱
print(db.collection_names())#列出db中的集合名稱
print(col.count_documents({}))#計算col中的文檔(資料)數量


#判斷key是否在指定的dictionary當中，若有則return True
def dicMemberCheck(key, dicObj):
    if key in dicObj:
        return True
    else:
        return False

#寫入資料 data是dictionary
def write_one_data(data):
    if dicMemberCheck('events', data):
        if dicMemberCheck('message', data['events'][0]):
            if dicMemberCheck('text', data['events'][0]['message']):
                if re.match('\d\d\d\d-\d\d-\d\d \w', data['events'][0]['message']['text']):
                    col.insert_one(data)

#寫入多筆資料，data是一個由dictionary組成的list
def write_many_datas(data):
    col.insert_many(data)

#讀取所有LINE的webhook event紀錄資料
def read_many_datas():
    data_list = []
    for data in col.find():
        data_list.append(str(data))

    print(data_list)
    return data_list

# 讀取LINE的對話紀錄資料
def read_chat_records():
    data_list = []
    for data in col.find():
        print(data['events'][0]['message']['text'])
        data_list.append(data['events'][0]['message']['text'])

    print(data_list)
    return data_list

# #刪除所有資料
# def delete_all_data():
#     data_list = []
#     for x in col.find():
#         data_list.append(x)
#
#     datas_len = len(data_list)
#
#     col.delete_many({})
#
#     if len(data_list)!=0:
#         return f"資料刪除完畢，共{datas_len}筆"
#     else:
#         return "資料刪除出錯"


#對比日期
def date_alarm():

    d=str(datetime.date.today())
    food_list=[]

    for data in col.find():
        date=data['events'][0]['message']['text']
        date_check=date.split(' ')
        if date_check[0] == d:
            food_list.append(date_check[1])

    food_text = '\n'.join(food_list)

    return food_text

# 刪除指定食品資訊
def delete_one_data(msg):
    data_list = []
    for data in col.find():
        if msg[3:] == data['events'][0]['message']['text']:
            data_list.append(msg[3:])
            col.delete_one(data)

    print(data_list)

    if len(data_list)!=0:
        return data_list[0] + " 已成功刪除!"
    else:
        return "資料錯誤，請檢查輸入的訊息是否有誤!"

#提前提醒日期
def date_adv():

    d=str(datetime.date.today() + datetime.timedelta(days=3))
    adv_list=[]

    for data in col.find():
        date=data['events'][0]['message']['text']
        date_check=date.split(' ')
        if date_check[0] == d:
            adv_list.append(date_check[1])

    adv_text = '\n'.join(adv_list)

    print(adv_text)

    return adv_text

# 查看指定日期資訊
def date_check(msg):

    ck_date=[]

    for data in col.find():
        inf = data['events'][0]['message']['text']
        split = inf.split(' ')
        if msg == split[0]:
            ck_date.append(split[1])

    ful_date='\n'.join(ck_date)

    return ful_date