const url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"

fetch(url)
    .then( response => response.json() )
    .then( data => {
        const result_list = data.data.results;
        // 給class = title編號用，result_list_len = [1, 2, 3, ...]
        const result_list_len = Array.from({length: result_list.length-3},(v, i) =>  i + 1 );
        let currentIndex = 0;

        renderPromotion(result_list.slice(0,3));
        renderTitle(result_list.slice(3,13), result_list_len, currentIndex);
        loadMore(result_list, result_list_len, currentIndex);
        window.addEventListener("resize", updateGrid)
    });

function renderPromotion(result_list){
    result_list.forEach((result) => {

        const contentContainer = document.querySelector(".content");

        // 創建框架
        const promotion_div = document.createElement("div");
        if(result._id <= 3){
            promotion_div.className = `promotion${result._id}`;
        }

        const img = document.createElement("img");
        img.className = "promotion-photo";
        img.src = getFirstImg(result.filelist)

        const p = document.createElement("p");
        p.textContent = result.stitle;

        promotion_div.appendChild(img);
        promotion_div.appendChild(p);
        contentContainer.appendChild(promotion_div);
    });
};

function renderTitle(result_list, result_list_len, currentIndex){
    result_list.forEach((result) => {

        const contentContainer = document.querySelector(".content");

        // 創建框架
        const title_div = document.createElement("div");
        title_div.className = `title title${result_list_len[currentIndex]}`;
        currentIndex += 1;
        title_div.style.backgroundImage = `url(${getFirstImg(result.filelist)})`;

        const img = document.createElement("img");
        img.className = "icon";
        img.src = "./data/star-icon.png";

        const p = document.createElement("p");
        p.className = "title-text";
        p.textContent = result.stitle.length > 7 ? `${result.stitle.substring(0,7)}...` : result.stitle;

        title_div.appendChild(img);
        title_div.appendChild(p);
        contentContainer.appendChild(title_div);
    });
};

function getFirstImg(filelist){
   return filelist.match(/https:.+?\.jpg/i)[0];
};

function loadMore(result_list, result_list_len, currentIndex){
    const btnLoad = document.querySelector(".btnLoad");

    let start = 13;
    btnLoad.addEventListener("click", () => {

        let end = start + 10;
        currentIndex += 10;
        renderTitle(result_list.slice(start,end), result_list_len, currentIndex);
        updateGrid();
        start += 10;

        if(end > result_list.length){
            end = result_list.length + 1
            renderTitle(result_list.slice(start,end))
            btnLoad.style = "display: none"
        }
    })
}

function updateGrid(){
    const gridContainer = document.querySelector(".content");
    const titles = document.querySelectorAll(".title");
    const title_num_list = [];

    // 螢幕寬度 > 1200px 時：
    if(window.innerWidth > 1200){
        titles.forEach(title => {
            const title_num = title.className.match(/\d+/)[0];
            if(title_num % 5 == 1){
                title_num_list.push(`title${title_num}`)
                title_num_list.push(`title${title_num}`)
            }else{
                title_num_list.push(`title${title_num}`)
            }
        })
    
        const title_rows = [];
        for(let i=0; i<title_num_list.length; i+=6){
            const row = title_num_list.slice(i, i+6)
            while (row.length < 6) {
                row.push(".");
            }
            title_rows.push(row);
        }
        let gridTemplate = `"promotion1 promotion1 promotion2 promotion2 promotion3 promotion3"\n`;
        title_rows.forEach(title_row => {
            const title_row_string = title_row.join(" ")
            gridTemplate += `"${title_row_string}"\n`
            gridContainer.style.gridTemplateAreas = gridTemplate;
        })
    }else if(window.innerWidth > 600){
        titles.forEach(title => {
            const title_num = title.className.match(/\d+/)[0];
            if(title_num % 10 == 9 || title_num % 10 == 0){
                title_num_list.push(`title${title_num}`)
                title_num_list.push(`title${title_num}`)
            }else{
                title_num_list.push(`title${title_num}`)
            }
        })
    
        const title_rows = [];
        for(let i=0; i<title_num_list.length; i+=4){
            const row = title_num_list.slice(i, i+4)
            while (row.length < 4) {
                row.push(".");
            }
            title_rows.push(row);
        }
        let gridTemplate = `"promotion1 promotion1 promotion2 promotion2"\n 
                            "promotion3 promotion3 promotion3 promotion3"\n`;
        title_rows.forEach(title_row => {
            const title_row_string = title_row.join(" ")
            gridTemplate += `"${title_row_string}"\n`
            gridContainer.style.gridTemplateAreas = gridTemplate;
        })
    }else{
        titles.forEach(title => {
            const title_num = title.className.match(/\d+/)[0];
            title_num_list.push(`title${title_num}`)
        })
        
        const title_rows = [];
        for(let i=0; i<title_num_list.length; i+=1){
            title_rows.push(title_num_list.slice(i, i+1))
        }
        let gridTemplate = `"promotion1"\n
                            "promotion2"\n 
                            "promotion3"\n`;
        title_rows.forEach(title_row => {
            const title_row_string = title_row.join(" ")
            gridTemplate += `"${title_row_string}"\n`
            gridContainer.style.gridTemplateAreas = gridTemplate;
        })
    }
    
    addCSSRules(title_num_list)
}

function addCSSRules(titles) {
    const styleSheet = document.styleSheets[0]; // 選擇 CSSStyleSheet
    titles.forEach(title => {
        const rule = `.${title} { grid-area: ${title}; }`;
        styleSheet.insertRule(rule);
    });
}

