// webapp/script.js

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');
    const clearBtn = document.getElementById('clear-btn');
    const micBtn = document.getElementById('mic-btn');
    const apiBaseUrl = 'http://127.0.0.1:5000';

    // --- Voice Recognition Setup ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = (event) => {
            const speechResult = event.results[0][0].transcript;
            messageInput.value = speechResult;
            // Automatically submit the form with the recognized text
            messageForm.dispatchEvent(new Event('submit'));
        };

        recognition.onspeechend = () => {
            recognition.stop();
            micBtn.classList.remove('is-listening');
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            micBtn.classList.remove('is-listening');
        };
    } else {
        console.log("Speech recognition not supported in this browser.");
        micBtn.style.display = 'none';
    }

    // --- Event Listeners ---
    messageForm.addEventListener('submit', handleFormSubmit);
    clearBtn.addEventListener('click', handleClear);
    micBtn.addEventListener('click', handleMicClick);

    // --- Core Functions ---
    async function loadHistory() {
        try {
            const response = await fetch(`${apiBaseUrl}/history`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            chatBox.innerHTML = '';
            if (data.history && data.history.length > 0) {
                data.history.forEach(msg => addMessage(msg.content, msg.role));
            } else {
                addMessage("Hello! I am your AI assistant. How can I assist you today?", 'agent');
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    async function handleFormSubmit(event) {
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

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            removeTypingIndicator();
            addMessage(data.response, 'agent');

        } catch (error) {
            console.error('Error communicating with the agent:', error);
            removeTypingIndicator();
            addMessage('Sorry, I am having trouble connecting. Please try again.', 'agent');
        }
    }

    async function handleClear() {
        try {
            await fetch(`${apiBaseUrl}/clear_memory`, { method: 'POST' });
            chatBox.innerHTML = '';
            addMessage("Conversation history cleared.", 'agent');
        } catch (error) {
            console.error('Error clearing memory:', error);
        }
    }

    function handleMicClick() {
        if (!recognition) return;

        if (micBtn.classList.contains('is-listening')) {
            recognition.stop();
            micBtn.classList.remove('is-listening');
        } else {
            recognition.start();
            micBtn.classList.add('is-listening');
        }
    }

    // --- UI Helper Functions ---
    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        const senderClass = sender === 'user' ? 'user-message' : 'agent-message';
        messageElement.classList.add('message', senderClass);
        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.classList.add('message', 'agent-message', 'typing-indicator');
        indicator.innerHTML = '<p><span>.</span><span>.</span><span>.</span></p>';
        chatBox.appendChild(indicator);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = chatBox.querySelector('.typing-indicator');
        if (indicator) chatBox.removeChild(indicator);
    }

    // --- Initial Load ---
    loadHistory();
});
