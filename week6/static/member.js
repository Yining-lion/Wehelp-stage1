const $ = (selector) => document.querySelector(selector);

$("#deleteMsgForm").addEventListener("submit", e => {
    if (!confirm("確定要刪除留言嗎？")) {
        e.preventDefault(); 
    }
})