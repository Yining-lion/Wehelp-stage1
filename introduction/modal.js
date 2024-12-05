import { questions } from "./data/questions.js"

document.querySelectorAll(".message").forEach(message => {
    message.addEventListener("click", () => {
        let msgId = message.dataset.msgId;
        let questionData = questions.find(question => question.id == msgId);
        
        if(questionData){
            let html =
            `
            <div class="modal-dialog">
            <div class="modal-content">
    
                <!-- header -->
                <div class="modal-header">
                    <h5 class="modal-title">${questionData.question}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
    
                <!-- body -->
                <div class="modal-body">
                    ${questionData.answer}
                </div>
                
            </div>
            </div>`

        let modal = document.querySelector(".modal");
        modal.innerHTML = html;

        const newModal = new bootstrap.Modal(modal);
        newModal.show();
        }
        })
})







