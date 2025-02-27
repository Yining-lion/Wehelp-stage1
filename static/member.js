const $ = (selector) => document.querySelector(selector);

$("#deleteMsgForm").addEventListener("submit", e => {
    if (!confirm("確定要刪除留言嗎？")) {
        e.preventDefault(); 
    }
})

$("#searchMember").addEventListener("submit", async (e) => {
    e.preventDefault();

    let formData = new FormData(e.target);
    // 查看取得的 form 資料 ex： username: c
    // for (let [key, value] of formData.entries()) {  
    //     console.log(`${key}: ${value}`);
    // }
    let queryParams = new URLSearchParams(formData).toString(); // ex： username=c

    try{
        let res = await fetch(`/api/member?${queryParams}`, {
            method: "GET",
        })
        let data = await res.json() // data: {id: 4, name: 'c', username: 'c'} 或是 {data: null}

        if(!data.data){
            $(".searchResult").textContent = "無此會員";
        } else {
            $(".searchResult").textContent = `${data.data.name} (${data.data.username})`;
        }
    }
    catch(error){
        console.error("錯誤:", error);
        $(".searchResult").textContent = "發生錯誤，請稍後再試";
    }
})

$("#updateName").addEventListener("submit", async (e) => {
    e.preventDefault();
    let newName = $(".update").value.trim();

    if(!newName){
        $(".updateResult").textContent = "請輸入名稱";
        return
    }
    
    try{
        let res = await fetch("/api/member", {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: newName})
        })
        let data = await res.json() // {ok: true} 或 {error: true}

        if(data.ok){
            $(".updateResult").textContent = "更新成功";
            $(".welcomText").textContent = `${newName}，歡迎登入系統`
        } else {
            $(".updateResult").textContent = "更新失敗";
        }
    }
    catch(error){
        console.error("錯誤:", error);
        $(".updateResult").textContent = "發生錯誤，請稍後再試";
    }
})