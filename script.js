document.getElementById("navigateButton1").addEventListener("click", function() {
    window.location.href = "sleep_info.html";})

document.getElementById("navigateButton2").addEventListener("click", function() {
window.location.href = "webapp.html";})

document.getElementById('sendButton').onclick = function() {
    const userInput = document.getElementById('userInput').value;
    if (userInput) {
        addMessage(userInput, 'user');
        document.getElementById('userInput').value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage("Sorry, I couldn't process your request.", 'bot');
        });
    }
};

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;
    messageDiv.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + message;
    document.getElementById('messages').appendChild(messageDiv);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
}