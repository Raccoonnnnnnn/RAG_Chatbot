window.onbeforeunload = function() {
    console.log("Page is about to refresh");
    return "Do you want to leave this page?";
};

document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendButton");
    const userInput = document.getElementById("userInput");
    const messages = document.getElementById("messages");

    if (!sendButton || !userInput || !messages) {
        console.error("Required elements not found!");
        return;
    }

    loadChatHistory();

    sendButton.addEventListener("click", function (e) {
        e.preventDefault();
        sendMessage();
    });

    userInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.keyCode === 13) {
            e.preventDefault();
            sendMessage();
        }
    });

    if (!document.querySelector(".new-chat-button")) {
        const newChatButton = document.createElement("button");
        newChatButton.className = "new-chat-button";
        newChatButton.innerHTML = `
            <svg class="new-chat-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="white" stroke-width="2">
                <path d="M10 4V4C8.13623 4 7.20435 4 6.46927 4.30448C5.48915 4.71046 4.71046 5.48915 4.30448 6.46927C4 7.20435 4 8.13623 4 10V13.6C4 15.8402 4 16.9603 4.43597 17.816C4.81947 18.5686 5.43139 19.1805 6.18404 19.564C7.03968 20 8.15979 20 10.4 20H14C15.8638 20 16.7956 20 17.5307 19.6955C18.5108 19.2895 19.2895 18.5108 19.6955 17.5307C20 16.7956 20 15.8638 20 14V14" stroke="currentColor" stroke-linecap="square"></path>
                <path d="M12.4393 14.5607L19.5 7.5C20.3284 6.67157 20.3284 5.32843 19.5 4.5C18.6716 3.67157 17.3284 3.67157 16.5 4.5L9.43934 11.5607C9.15804 11.842 9 12.2235 9 12.6213V15H11.3787C11.7765 15 12.158 14.842 12.4393 14.5607Z" stroke="currentColor" stroke-linecap="square"></path>
            </svg>
            <span class="new-chat-text">New Chat</span>`;
        newChatButton.addEventListener("click", clearChat);
        document.querySelector(".chat-container").prepend(newChatButton);
    }

    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === "") return;

        appendMessage(messageText, "message user-message");

        // Loại bỏ delay, phản hồi ngay lập tức
        appendMessage("Chatbot: This is a simulated response!", "message bot-message");

        userInput.value = "";
        saveChatHistory();
    }

    function appendMessage(text, className) {
        const messageDiv = document.createElement("div");
        className.split(" ").forEach(cls => messageDiv.classList.add(cls));
        messageDiv.textContent = text;
        messages.appendChild(messageDiv);
    
        // Kiểm tra nếu user đang ở cuối, thì auto-scroll
        const isAtBottom = messages.scrollHeight - messages.clientHeight <= messages.scrollTop + 10;
        if (isAtBottom) {
            messageDiv.scrollIntoView({ behavior: "smooth", block: "end" });
            window.scrollTo({
                        top: document.body.scrollHeight,
                        behavior: "smooth"
                    });
        }
    }
    
    function saveChatHistory() {
        try {
            const chatMessages = Array.from(messages.children).map(msg => ({
                text: msg.textContent,
                class: msg.className
            }));
            localStorage.setItem("chatHistory", JSON.stringify(chatMessages));
        } catch (error) {
            console.error("Error saving chat history:", error);
        }
    }

    function loadChatHistory() {
        try {
            const savedMessages = localStorage.getItem("chatHistory");
            if (savedMessages) {
                const chatMessages = JSON.parse(savedMessages);
                chatMessages.forEach(msg => {
                    const messageDiv = document.createElement("div");
                    msg.class.split(" ").forEach(cls => messageDiv.classList.add(cls));
                    messageDiv.textContent = msg.text;
                    messages.appendChild(messageDiv);
                });
            }
        } catch (error) {
            console.error("Error loading chat history:", error);
            localStorage.removeItem("chatHistory");
        }
    }

    function clearChat(e) {
        if (e) e.preventDefault();
        localStorage.removeItem("chatHistory");
        messages.innerHTML = "";
        console.log("Chat history cleared");
    }
});