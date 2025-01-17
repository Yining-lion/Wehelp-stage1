//  === Task 1 ===
const messages={
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Leslie":"I'm at home near Xiaobitan station.",
    "Vivian":"I'm at Xindian station waiting for you."
    }; 
    
function findAndPrint(messages, currentStation){

    const stations = ["Songshan", "Nanjing Sanmin","Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
        "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall",
        "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei",
        "Dapinglin", "Qizhang", "Xiaobitan", "Xindian City Hall", "Xindian"]

    const adjacency_list = {"Songshan":["Nanjing Sanmin"],"Nanjing Sanmin":["Songshan","Taipei Arena"],
            "Taipei Arena":["Nanjing Sanmin","Nanjing Fuxing"],"Nanjing Fuxing":["Taipei Arena","Songjiang Nanjing"],
            "Songjiang Nanjing":["Nanjing Fuxing","Zhongshan"], "Zhongshan":["Songjiang Nanjing","Beimen"],
            "Beimen":["Zhongshan","Ximen"],"Ximen":["Beimen","Xiaonanmen"],"Xiaonanmen":["Ximen","Chiang Kai-Shek Memorial Hall"],
            "Chiang Kai-Shek Memorial Hall":["Xiaonanmen","Guting"],"Guting":["Chiang Kai-Shek Memorial Hall","Taipower Building"],
            "Taipower Building":["Guting","Gongguan"],"Gongguan":["Taipower Building","Wanlong"],"Wanlong":["Gongguan","Jingmei"],
            "Jingmei":["Wanlong","Dapinglin"],"Dapinglin":["Jingmei","Qizhang"],"Qizhang":["Dapinglin","Xiaobitan","Xindian City Hall"],
            "Xiaobitan":["Qizhang"],"Xindian City Hall":["Qizhang","Xindian"],"Xindian":["Xindian City Hall"]}

    function two_point_distance(start, target){
        let queqe = [[start, 0]];
        let visited = new Set();

        while(queqe.length >0 ){
            let [ current, distance ] = queqe.shift();

            if(current === target){
                return distance;
            }

            if(!visited.has(current)){
                visited.add(current);

                let neighbors = adjacency_list[current];
                for(let neighbor of neighbors){
                    queqe.push([neighbor, distance + 1]);
                }
            }
        }
    }

    let closest_name = null;
    let min_distance = Infinity;
    for(let [name, message] of Object.entries(messages)){
        for(let station of stations){
            if(message.includes(station)){
                let distance = two_point_distance(station, currentStation);
                if(distance < min_distance){
                    min_distance = distance;
                    closest_name = name
                }
            }
        }
    }
    console.log(closest_name)

}

console.log("=== Task 1 ===") 
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian

//  === Task 2 ===
const consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
    ];

let schedules = {}; // ex: [{ Jenny: [ [15, 1], ...] }]

function book(consultants, hour, duration, criteria){
    if(criteria == "price"){
        consultants.sort((a,b) => {return a.price - b.price}) // 語法：arr.sort([compareFunction]) a-b是小排到大
    } else if(criteria == "rate"){
        consultants.sort((a,b) => {return b.rate - a.rate}) // b-a是大排到小
    };

// Array.from用於創造新陣列。想產生連續數字陣列的語法：Array.from({ length: N }, (v, i) => 回傳值)
    let selected_time = Array.from({length: duration + 1}, (v, i) => hour + i ); // ex: [15,16]

    for (let consultant of consultants) {

        // 初始化顧問的預約資料
        if (!schedules[consultant.name]) {
            schedules[consultant.name] = [];
        }

        // 檢查顧問是否有空
        let is_available = true;
        for (let schedule of schedules[consultant.name]) {

            let existing_time = Array.from({ length: schedule[1] + 1 }, (v, i) => schedule[0] + i);
            
            if (selected_time.some(time => existing_time.includes(time))) {
                is_available = false;
                break;
            }
        }

        // 若顧問有空，進行預約
        if (is_available) {
            schedules[consultant.name].push([hour, duration]);
            console.log(consultant.name);
            return;
        }
    }

    console.log("No Service");
}

console.log("=== Task 2 ===") 
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John
    
//  === Task 3 ===
function func(...data){
    let name_and_middle = [] //[{name: '彭大牆', middle: '大'}{name: '陳王明雅', middle: '明'}{name: '吳明', middle: '明'}
    let count_middle_num = [] //[大: 1, 明: 2]

    for(let i=0; i<data.length; i++){
        let name = data[i];
        let name_len = name.length;

        if(name_len <= 3){
            name_and_middle.push({
                name: name,
                middle: name[1]
            })
        } else{
            name_and_middle.push({
                name: name,
                middle: name[2]
            })
        }
    }

    name_and_middle.forEach(item => {
        let middle = item.middle
        count_middle_num[middle] = (count_middle_num[middle] || 0) + 1; //短路求值運算符：(||)運算時，如果第1個運算子為"falsy"時，回傳第2個運算子。否則，回傳第1個運算子
    })

    let unique_middles = [];
    name_and_middle.forEach(item => {
        let middle = item.middle
        if(count_middle_num[middle] == 1){
            unique_middles.push(item.name)
        }
    })
    
    if (unique_middles.length > 0) {
    console.log(String(unique_middles));
    } else {
        console.log("沒有");
    }
}

console.log("=== Task 3 ===") 
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安

//  === Task 4 ===
function getNumber(index){ 
    let list = [0];
   
    for(let i=1; i<=index; i++)
       if(i % 3 == 0 ){list.push(list[list.length -1 ] - 1)}
        else{list.push(list[list.length -1 ] + 4)};

    console.log(list[index]);
} 
    
console.log("=== Task 4 ===")   
getNumber(1); // print 4 
getNumber(5); // print 15 
getNumber(10); // print 25 
getNumber(30); // print 70