let burger = document.querySelector(".burger");
let burgerMenu = document.querySelector(".burger-menu");
burger.addEventListener("click", ()=>{
    burgerMenu.style = "overflow: visible"
    burgerMenu.style = "height: 100%"
})

let cross = document.querySelector(".cross");
cross.addEventListener("click", () => {
    burgerMenu.style = "overflow: hidden"
    burgerMenu.style = "height: 0"
})