let signinForm = document.getElementById("signinForm");
signinForm.addEventListener("submit", e => {
    let username = document.querySelector(".username").value;
    let password = document.querySelector(".password").value;
    let agree = document.querySelector(".agree").checked;

    if(!agree){
        e.preventDefault();
        alert("Please check the checkbox first.");
    }

    let formData = new FormData();
    formData.append("username", username)
    formData.append("password", password)
    formData.append("agree", agree)

    async function connectPOST(){
        let res = await fetch("/signin",{
            method: "POST",
            body: formData
        })
    }
    connectPOST();
})

let squareForm = document.getElementById("squareForm")
squareForm.addEventListener("submit", e => {
    e.preventDefault();
    let num = document.querySelector(".square").value
    num = parseInt(num)

    if(Number.isInteger(num) && num > 0){
       location.href = `/square/${num}`;
    }else{
        e.preventDefault();
        alert("Please enter a positive number.")
    }
})