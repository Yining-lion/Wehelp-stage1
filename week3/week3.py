import urllib.request as req
import json
import csv
import re

# === Task 1 ===
NumDistrictMRTLists = [] # [('2011051800000646', '內湖區', '文德'), ('2011051800000096', '中正區', '中正紀念堂'), ...]
SpotLists = [] # [['新北投溫泉區', '北投區', '121.508447', '25.137077', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpg'], ...]
MRTSpotLists = [] # [('新北投', '新北投溫泉區'), ('雙連', '大稻埕碼頭'), ('士林', '士林官邸'), ...]
MRTDicts = {} # {'新北投': ['新北投', '新北投溫泉區', '北投圖書館', '地熱谷', '梅庭', '北投溫泉博物館', '北投公園'], '雙連': ['雙連', '大稻埕碼頭', '新店溪、大漢溪與淡水河自行車道'], ...}

src1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with req.urlopen(src2) as response:
    file = json.load(response)
    for data in file["data"]:
        SERIAL_NO = data["SERIAL_NO"]
        MRT = data["MRT"]
        NumDistrictMRTLists.append((SERIAL_NO, data["address"][5:8], MRT))
        
with req.urlopen(src1) as response:
    file = json.load(response)
    for result in file["data"]["results"]:
        SpotTitle = result["stitle"]

        SERIAL_NO = result["SERIAL_NO"]
        for num_district_list in NumDistrictMRTLists:
            if num_district_list[0] == SERIAL_NO:
                District = num_district_list[1]
                StationName = num_district_list[2]
                MRTSpotLists.append((StationName, SpotTitle))
            
        Longitude = result["longitude"]
        Latitude = result["latitude"]
        FileList = result["filelist"] # FileList 有很多jpg檔，使用「正則表達式」尋找第一個jpg檔
        # 字串前的 r 表示這是一個「原始字串」，這樣就不會對反斜線 \ 進行轉義處理，例如不會把 \n 轉義成換行，而是會保留 \n 字面值
        # \S：匹配非空白字符； +：比對符合1次或多次； ?：比對符合0次或1次； +?：比對到符合的就停止，不貪婪
        # \.：若要比對"."，需在前面加上 \ ，因為"."在正則中是特殊字符，需使用 \ 進行轉義
        # 使用 re.search()後會回傳一個 Match Object (裡面包含匹配到的字串、其位置等資訊)，因此需再使用 group() 方法從 Match Object 中提取匹配到的字串內容
        ImageURL = re.search(r'http\S+?\.jpg', FileList, re.IGNORECASE).group()
        SpotLists.append([SpotTitle, District, Longitude, Latitude, ImageURL])

    for mrt, spot in MRTSpotLists:
        if mrt not in MRTDicts:
            MRTDicts[mrt] = [mrt] # 初始化字典，以 mrt 為開頭
        MRTDicts[mrt].append(spot)

with open("./task1-2_csv/spot.csv", mode="w", newline="", encoding="utf-8") as file:
    file = csv.writer(file)
    for SpotList in SpotLists:
        file.writerow(SpotList)

with open("./task1-2_csv/mrt.csv", mode="w", newline="", encoding="utf-8") as file:
    file = csv.writer(file)
    for MRTList in MRTDicts.values():
        file.writerow(MRTList)

# === Task 2 ===
from bs4 import BeautifulSoup

articles = {} # {'[報牌] 蛇燦年發539': ['[報牌] 蛇燦年發539', '3', 'Wed Jan 22 10:32:44 2025'], 
            # '[報牌] 539老朋友、34星': ['[報牌] 539老朋友、34星', '3', 'Tue Jan 21 19:43:44 2025'], ...] 

# 附加 Request Headers 資訊
def GetData(url):
    def GetRoot(url):
        request = req.Request(url, headers={
        "cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        return BeautifulSoup(data, "html.parser")
    
    root = GetRoot(url)

    titles = root.find_all("div", class_="title")
    like_dislike_count_lists = root.find_all("div", class_="nrec")

    # enumerate(iterable)會返回(索引值, 元素值)
    for index, title in enumerate(titles): 
        if title.a != None:
            article_title = title.a.string # 抓取文章標題
            
            # 抓取文章時間
            article_url = "https://www.ptt.cc" + title.a["href"]
            article_info = GetRoot(article_url).find_all("span", class_="article-meta-value") # 抓出[作者, 看版, 標題, 時間]
            if article_info == []:
                publish_time = ""
            else:    
                time = article_info[3].string
                publish_time = time

            # 抓取讚數
            count = like_dislike_count_lists[index].string
            if count == None:
                like_dislike_count = 0
            else:
                like_dislike_count = count

            # 將資訊存入 articles 字典
            articles[article_title] = [article_title, like_dislike_count, publish_time]          
    
    previous_page = GetRoot(page_url).find("a", string="‹ 上頁")
    return previous_page["href"]

page_url = "https://www.ptt.cc/bbs/Lottery/index.html"

#  抓 3 頁
page = 0
while page < 3:
    page_url = "https://www.ptt.cc" + GetData(page_url)
    page += 1

with open("./task1-2_csv/article.csv", mode="w", newline="", encoding="utf-8") as file:
    file = csv.writer(file)
    for article in articles.values():
        file.writerow(article)