// webapp/script.js

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');
    const apiBaseUrl = 'http://127.0.0.1:5000';

    /**
     * Fetches and displays the conversation history on page load.
     */
    async function loadHistory() {
        try {
            const response = await fetch(`${apiBaseUrl}/history`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            // Clear the initial "Hello" message
            chatBox.innerHTML = '';
            if (data.history && data.history.length > 0) {
                data.history.forEach(message => {
                    const sender = message.role === 'user' ? 'user' : 'agent';
                    addMessage(message.content, sender);
                });
            } else {
                addMessage("Hello! I am your AI assistant. How can I assist you today?", 'agent');
            }
        } catch (error) {
            console.error('Error loading history:', error);
            // Don't clear the box, just show the error in console
        }
    }

    messageForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userMessage = messageInput.value.trim();
        if (userMessage === '') return;

        addMessage(userMessage, 'user');
        messageInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch(`${apiBaseUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            removeTypingIndicator();
            addMessage(data.response, 'agent');

        } catch (error) {
            console.error('Error communicating with the agent:', error);
            removeTypingIndicator();
            addMessage('Sorry, I am having trouble connecting. Please try again.', 'agent');
        }
    });

    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'agent-message', 'typing-indicator');
        typingIndicator.innerHTML = '<p><span>.</span><span>.</span><span>.</span></p>';
        chatBox.appendChild(typingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = chatBox.querySelector('.typing-indicator');
        if (typingIndicator) {
            chatBox.removeChild(typingIndicator);
        }
    }

    // Load the chat history when the page is ready
    loadHistory();
});
