// webapp/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element References ---
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-btn');
    const micBtn = document.getElementById('mic-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    // Advanced Feature Elements
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-input');
    const autonomousToggle = document.getElementById('autonomous-toggle');
    const deepThinkingCheckbox = document.getElementById('deep-thinking-checkbox');

    let autonomousStatusInterval = null;

    // --- Core Functions ---

    /**
     * Appends a message to the chat box.
     * @param {string} message - The message content.
     * @param {string} sender - 'user' or 'ai'.
     */
    const appendMessage = (message, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'ai-message');
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    /**
     * Shows or hides the typing indicator.
     * @param {boolean} show - Whether to show the indicator.
     */
    const showTypingIndicator = (show) => {
        typingIndicator.classList.toggle('hidden', !show);
        if (show) chatBox.scrollTop = chatBox.scrollHeight;
    };

    /**
     * Sends a message to the backend and displays the response.
     */
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        userInput.value = '';
        showTypingIndicator(true);

        try {
            // Toggle deep thinking mode for this specific request if checked
            const deepThinking = deepThinkingCheckbox.checked;
            await fetch('/deep_thinking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled: deepThinking }),
            });

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            appendMessage(data.response, 'ai');

        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage('Sorry, I seem to be having trouble connecting. Please try again later.', 'ai');
        } finally {
            showTypingIndicator(false);
            // Reset deep thinking mode after the request
            deepThinkingCheckbox.checked = false;
            await fetch('/deep_thinking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled: false }),
            });
        }
    };

    /**
     * Loads the initial chat history from the server.
     */
    const loadHistory = async () => {
        try {
            const response = await fetch('/history');
            const data = await response.json();
            chatBox.innerHTML = '';
            data.history.forEach(item => {
                appendMessage(item.content, item.role === 'user' ? 'user' : 'ai');
            });
        } catch (error) {
            console.error('Error loading history:', error);
        }
    };

    /**
     * Clears the chat history on the server and UI.
     */
    const clearHistory = async () => {
        try {
            await fetch('/clear_memory', { method: 'POST' });
            loadHistory();
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    };

    // --- Advanced Feature Functions ---

    /**
     * Handles file upload.
     */
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        showTypingIndicator(true);
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) throw new Error('File upload failed.');

            const data = await response.json();
            appendMessage(`File '${file.name}' uploaded successfully.`, 'user');
            appendMessage(data.response, 'ai');
        } catch (error) {
            console.error('Error uploading file:', error);
            appendMessage('Sorry, there was an error uploading your file.', 'ai');
        } finally {
            showTypingIndicator(false);
            // Reset the file input so the same file can be uploaded again
            fileInput.value = '';
        }
    };

    /**
     * Starts or stops the autonomous agent.
     */
    const toggleAutonomousMode = async () => {
        if (autonomousToggle.checked) {
            // Start autonomous mode
            const goal = prompt("Please enter the goal for the autonomous agent:");
            if (goal) {
                try {
                    const response = await fetch('/autonomous/start', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ goal: goal }),
                    });
                    const data = await response.json();
                    appendMessage(`Autonomous mode started. Goal: ${goal}`, 'ai');
                    startStatusPolling();
                } catch (error) {
                    console.error('Error starting autonomous mode:', error);
                    appendMessage('Failed to start autonomous mode.', 'ai');
                    autonomousToggle.checked = false;
                }
            } else {
                autonomousToggle.checked = false; // User cancelled
            }
        } else {
            // Stop autonomous mode
            try {
                await fetch('/autonomous/stop', { method: 'POST' });
                appendMessage('Autonomous mode stopped by user.', 'ai');
                stopStatusPolling();
            } catch (error) {
                console.error('Error stopping autonomous mode:', error);
            }
        }
    };

    /**
     * Polls the autonomous agent's status.
     */
    const checkAutonomousStatus = async () => {
        try {
            const response = await fetch('/autonomous/status');
            const data = await response.json();

            // Display updates in the chat
            if (data.task_log && data.task_log.length > 0) {
                const lastLog = data.task_log[data.task_log.length - 1];
                const logMessage = `[Autonomous Agent]: ${lastLog.step} - ${lastLog.details || lastLog.status}`;
                // Avoid duplicating messages
                if (chatBox.lastChild.textContent !== logMessage) {
                    appendMessage(logMessage, 'ai');
                }
            }

            if (!data.is_running) {
                stopStatusPolling();
                appendMessage('Autonomous agent has completed its goal.', 'ai');
                autonomousToggle.checked = false;
            }
        } catch (error) {
            console.error('Error checking autonomous status:', error);
            stopStatusPolling();
        }
    };

    const startStatusPolling = () => {
        if (!autonomousStatusInterval) {
            autonomousStatusInterval = setInterval(checkAutonomousStatus, 3000); // Poll every 3 seconds
        }
    };

    const stopStatusPolling = () => {
        clearInterval(autonomousStatusInterval);
        autonomousStatusInterval = null;
    };


    // --- Event Listeners ---
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    clearBtn.addEventListener('click', clearHistory);
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    autonomousToggle.addEventListener('change', toggleAutonomousMode);

    // --- Voice Recognition (Browser API) ---
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    micBtn.addEventListener('click', () => {
        micBtn.classList.add('active'); // Style the button to show it's listening
        recognition.start();
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage();
    };

    recognition.onend = () => {
        micBtn.classList.remove('active');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        micBtn.classList.remove('active');
    };

    // --- Initial Load ---
    loadHistory();
});
