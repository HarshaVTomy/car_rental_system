function sendMessage() {
    let userMessage = document.getElementById("user-input").value;
    if (userMessage.trim() === "") return;

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p><strong>User:</strong> ${userMessage}</p>`;

    fetch('/chatbot/', {
        method: 'POST',
        body: JSON.stringify({ user_input: userMessage }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;
        document.getElementById("user-input").value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

// CSRF Token Function
function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            csrfToken = cookie.split('=')[1];
            break;
        }
    }
    return csrfToken;
}

// Send message when pressing Enter key
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
