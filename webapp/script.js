// webapp/script.js

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');

    messageForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the form from reloading the page

        const userMessage = messageInput.value.trim();
        if (userMessage === '') {
            return; // Don't send empty messages
        }

        // 1. Display the user's message in the chat box
        addMessage(userMessage, 'user');
        messageInput.value = ''; // Clear the input field

        try {
            // 2. Send the message to the backend server
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const agentMessage = data.response;

            // 3. Display the agent's response
            addMessage(agentMessage, 'agent');

        } catch (error) {
            console.error('Error communicating with the agent:', error);
            addMessage('Sorry, I am having trouble connecting to the server. Please try again later.', 'agent');
        }
    });

    /**
     * Adds a new message to the chat box.
     * @param {string} text - The message text to display.
     * @param {string} sender - 'user' or 'agent'.
     */
    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);

        chatBox.appendChild(messageElement);

        // Scroll to the bottom of the chat box to show the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
