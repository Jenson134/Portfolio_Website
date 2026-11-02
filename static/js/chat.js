const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const sendButton = chatForm.querySelector("button[type='submit']");

const ERROR_REPLY = "Something went wrong. Please try again in a moment.";

let pending = false;

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = userInput.value.trim();
    if (!message || pending) return;

    addMessage("user", message);
    userInput.value = "";
    setPending(true);

    const typingIndicator = showTypingIndicator();
    let reply = ERROR_REPLY;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (response.ok || response.status === 429) {
            const data = await response.json();
            if (typeof data.reply === "string" && data.reply) {
                reply = data.reply;
            }
        }
    } catch (error) {
        reply = ERROR_REPLY;
    }

    removeTypingIndicator(typingIndicator);
    addMessage("bot", reply);
    setPending(false);
});

function setPending(state) {
    pending = state;
    sendButton.disabled = state;
    chatForm.setAttribute("aria-busy", String(state));
}

function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.textContent = text;
    chatWindow.appendChild(msg);
    scrollToLatest();
}

function showTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "typing-indicator";
    indicator.setAttribute("aria-hidden", "true");
    for (let i = 0; i < 3; i++) {
        indicator.appendChild(document.createElement("span"));
    }
    chatWindow.appendChild(indicator);
    scrollToLatest();
    return indicator;
}

function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode) {
        indicator.parentNode.removeChild(indicator);
    }
}

function scrollToLatest() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
