from collections import deque

# === Task 1 ===
messages = {
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}

def find_and_print(messages, current_station):

    stations = {"Songshan", "Nanjing Sanmin","Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
                "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
                "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei",
                "Dapinglin", "Qizhang", "Xiaobitan", "Xindian City Hall", "Xindian"}
    # 鄰接表
    adjacency_list = {"Songshan":["Nanjing Sanmin"],"Nanjing Sanmin":["Songshan","Taipei Arena"],
                    "Taipei Arena":["Nanjing Sanmin","Nanjing Fuxing"],"Nanjing Fuxing":["Taipei Arena","Songjiang Nanjing"],
                    "Songjiang Nanjing":["Nanjing Fuxing","Zhongshan"], "Zhongshan":["Songjiang Nanjing","Beimen"],
                    "Beimen":["Zhongshan","Ximen"],"Ximen":["Beimen","Xiaonanmen"],"Xiaonanmen":["Ximen","Chiang Kai-Shek Memorial Hall"],
                    "Chiang Kai-Shek Memorial Hall":["Xiaonanmen","Guting"],"Guting":["Chiang Kai-Shek Memorial Hall","Taipower Building"],
                    "Taipower Building":["Guting","Gongguan"],"Gongguan":["Taipower Building","Wanlong"],"Wanlong":["Gongguan","Jingmei"],
                    "Jingmei":["Wanlong","Dapinglin"],"Dapinglin":["Jingmei","Qizhang"],"Qizhang":["Dapinglin","Xiaobitan","Xindian City Hall"],
                    "Xiaobitan":["Qizhang"],"Xindian City Hall":["Qizhang","Xindian"],"Xindian":["Xindian City Hall"]}

    # 先計算兩點距離
    def two_point_distance(start, target):
        queqe = deque([(start, 0)]) # deque裡面放可迭代資料，這邊放 Tuple
        visited = set() # 建立集合放置已訪問的點
        while queqe:
            (current, distance) = queqe.popleft() #先提取第一個 Tuple 資料並分別放入 current 和 distance 變數中

            if current == target:
                return distance # 若找到目標，返回距離
            
            if current not in visited: # 若尚未訪問，標記為已訪問
                visited.add(current)

                for neighbor in adjacency_list[current]:  # 將未訪問的相鄰節點加入佇列
                    if neighbor not in visited:
                        queqe.append((neighbor, distance + 1))

    closest_name = None
    min_distance = float("inf")
    for (name, message) in messages.items(): # 將字典中的每對 key 和 value 組成 Tuple，並將他們分別放入 name 和  message 變數中
        for station in stations:
            if station in message: # 取得訊息裡的MRT關鍵字
                distance = two_point_distance(station, current_station)  # 取得訊息裡MRT及 current_station 的距離
                if distance < min_distance: # 不斷更新目前最小距離及名字
                    min_distance = distance
                    closest_name = name

    print(closest_name)

print("=== Task 1 ===")
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

# === Task 2 ===
consultants = [
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]

schedules = {consultant["name"]: [] for consultant in consultants} # 用來存放已預約時間

def book(consultants, hour, duration, criteria):

    if criteria == "price":
        sorted_consultants = sorted(consultants, key=lambda x: x["price"]) # 讓 consultants 依 price 由低到高排列
    elif criteria == "rate":
        sorted_consultants = sorted(consultants, key=lambda x: -x["rate"]) # 讓 consultants 依 rate 由高到低排列

    selected_time = set(range(hour, hour+duration)) # 選擇的時間以集合做資料處理，準備等一下做集合的交集判斷

    for consultant in sorted_consultants:
        name = consultant["name"]

        # 要先判斷 schedules[name] 是否有資料的原因是，若沒有資料會導致 for (start, dur) in schedules[name] 無法進行
        if not schedules[name]: # 若 schedules[name] 沒有資料，直接預約並append進原本的空陣列裡
            schedules[name].append((hour, duration))
            print(name)
            return
        
         # 若 schedules[name] 有資料：
        is_available = True  # 先假設顧問有空
        for (start, dur) in schedules[name]: # 將字典中的每對 key 和 value 組成 Tuple
            existing_time = set(range(start, start + dur)) # 已預約過的時間以集合做資料處理

            # 若有時間衝突，跳過該顧問，嘗試下一位
            if selected_time & existing_time:
                is_available = False
                break  

        # 如果該顧問有空，則執行預約
        if is_available:
            schedules[name].append((hour, duration))
            print(name)
            return  

    print("No service")

print("=== Task 2 ===")
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

# === Task 3 ===
def func(*data):
    
    data_num_list = list(range(0, len(data))) # 計算data傳入了幾個參數並 list
    name_to_middle = [ ] #建立列表 ex: [(彭大牆, 大), (陳王明雅, 明), (吳明, 明)]
    count_val_num = { } # 計算middle name 出現的次數，會呈現 ex: {'大': 1, '明': 2}

    for n in data_num_list:
        name = str(data[n])
        name_len = len(name) # 每個名字的長度

        if name_len <= 3:
            middle = name[1]
            name_to_middle.append((name, middle))
            
        else:
            middle = name[2]
            name_to_middle.append((name, middle))
    
        
        count_val_num[middle] = count_val_num.get(middle, 0) + 1
    
    # 以下寫法可以改成 List Comprehension (列表推導式)較為簡潔
    # no_intersection_keys = [ key for key, val in name_to_middle.items() if count_val_num[val] == 1]
    unique_middles =[]
    for name, middle in name_to_middle:
        if count_val_num[middle] == 1:
            unique_middles.append(name)

    if unique_middles:
        for name in unique_middles:
            print(name)
    else:
        print("沒有")

print("=== Task 3 ===")
func("彭大牆", "陳王明雅", "吳明",) # print 彭大牆
func("吳明", "吳明","吳明")
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

# === Task 4 ===
def get_number(index): 
    list = [0]
    
    for i in range(1, index + 1):
        if i % 3 == 0:
            list.append(list[-1] - 1 ) # list[-1] 表示 list 的最後一位，以此類推，list[-2] 表示倒數第二位
        else:
            list.append(list[-1] + 4 )

    print(list[index])

print("=== Task 4 ===")
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70