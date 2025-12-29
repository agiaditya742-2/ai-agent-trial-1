
document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const fileInput = document.getElementById('file-input');
    const uploadButton = document.getElementById('upload-button');

    // --- Core Chat Functionality ---

    const addMessage = (sender, message) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        chatInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            addMessage('agent', data.response);
        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('agent', 'Sorry, I encountered an error.');
        }
    };

    // --- Event Listeners ---

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // --- File Upload Functionality ---

    const uploadFile = async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            addMessage('agent', data.response || data.error);
        } catch (error) {
            console.error('Error uploading file:', error);
            addMessage('agent', 'Sorry, I encountered an error during file upload.');
        }
    };

    uploadButton.addEventListener('click', uploadFile);

    // --- Load Chat History ---
    const loadHistory = async () => {
        try {
            const response = await fetch('/history');
            const history = await response.json();
            history.forEach(item => {
                const sender = item.role === 'user' ? 'user' : 'agent';
                addMessage(sender, item.content);
            });
        } catch (error) {
            console.error('Error loading history:', error);
        }
    };

    // Initial load
    loadHistory();
});
