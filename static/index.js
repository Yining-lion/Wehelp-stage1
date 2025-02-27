const $ = (selector) => document.querySelector(selector);

$("#signupForm").addEventListener("submit", e => {
    let name = $(".name").value.trim();
    let username = $(".signupUsername").value.trim();
    let password = $(".signupPassword").value.trim();

    if(name == "" || username == "" || password == ""){
        e.preventDefault();
        alert("請輸入姓名、帳號、密碼");
    }
})

$("#signinForm").addEventListener("submit", e => {
    let username = $(".signinUsername").value.trim();
    let password = $(".signinPassword").value.trim();
    if(username == "" || password == ""){
        e.preventDefault();
        alert("請輸入帳號、密碼");
    }
})