import { questions } from "./data/questions.js"

let html = "";

questions.forEach((question) => {
    html +=
    `
      <div class="message" data-msg-id="${question.id}"  
      style="transform: rotate(${question.deg1}deg) translate(350px) 
                        rotate(${question.deg2}deg) translate(-50%, -50%);">
      ${question.question}</div>`
})

document.querySelector(".message-circle").innerHTML = html
