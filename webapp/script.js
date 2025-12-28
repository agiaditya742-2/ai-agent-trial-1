// webapp/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element References ---
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const menuBtn = document.getElementById('menu-btn');
    const menuDropdown = document.getElementById('menu-dropdown');
    const feedAgentBtn = document.getElementById('feed-agent-btn');
    const setWakeWordBtn = document.getElementById('set-wake-word-btn');
    const modal = document.getElementById('settings-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModalBtn = document.querySelector('.close-btn');
    const listeningIndicator = document.getElementById('listening-indicator');
    const autonomousToggle = document.getElementById('autonomous-toggle');
    const deepThinkingCheckbox = document.getElementById('deep-thinking-checkbox');

    // --- State Management ---
    let wakeWord = localStorage.getItem('agentWakeWord') || 'agent';
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;

    // --- Core Chat Functions ---
    const appendMessage = (message, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;
        appendMessage(message, 'user');
        userInput.value = '';
        // Typing indicator logic here if desired
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            appendMessage(data.response, 'ai');
        } catch (error) {
            console.error('Chat error:', error);
            appendMessage('Error: Could not connect to the server.', 'ai');
        }
    };

    const loadHistory = async () => {
        try {
            const response = await fetch('/history');
            if (!response.ok) throw new Error('Failed to fetch history.');
            const data = await response.json();
            chatBox.innerHTML = ''; // Clear the box before loading
            data.history.forEach(item => {
                appendMessage(item.content, item.role === 'user' ? 'user' : 'ai');
            });
        } catch (error) {
            console.error('Error loading history:', error);
            appendMessage('Could not load chat history.', 'ai');
        }
    };

    // --- Modal & Menu Logic ---
    const openModal = (content) => {
        modalBody.innerHTML = content;
        modal.style.display = 'block';
    };

    const closeModal = () => {
        modal.style.display = 'none';
    };

    menuBtn.addEventListener('click', () => {
        menuDropdown.classList.toggle('show');
    });

    window.addEventListener('click', (event) => {
        if (!event.target.matches('#menu-btn, #menu-btn *')) {
            if (menuDropdown.classList.contains('show')) {
                menuDropdown.classList.remove('show');
            }
        }
    });

    closeModalBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            closeModal();
        }
    });

    // --- Feature-Specific Modal Content ---
    setWakeWordBtn.addEventListener('click', () => {
        openModal(`
            <h2>Set Wake Word</h2>
            <p>Set a custom wake word to activate the agent via voice. The current wake word is: <strong>${wakeWord}</strong></p>
            <input type="text" id="wake-word-input" placeholder="Enter new wake word" />
            <button id="save-wake-word">Save</button>
        `);
        document.getElementById('save-wake-word').addEventListener('click', () => {
            const newWakeWord = document.getElementById('wake-word-input').value.trim().toLowerCase();
            if (newWakeWord) {
                wakeWord = newWakeWord;
                localStorage.setItem('agentWakeWord', wakeWord);
                alert(`Wake word updated to "${wakeWord}". Restarting listener.`);
                stopPersistentListening();
                startPersistentListening();
                closeModal();
            }
        });
    });

    feedAgentBtn.addEventListener('click', () => {
        openModal(`
            <h2>Feed Agent Data</h2>
            <p>Provide the agent with new knowledge via text or by uploading a PDF.</p>
            <textarea id="text-feed-input" rows="5" placeholder="Paste text here..."></textarea>
            <input type="file" id="pdf-feed-input" accept=".pdf" />
            <button id="submit-feed">Feed Agent</button>
        `);
        document.getElementById('submit-feed').addEventListener('click', async () => {
            const textData = document.getElementById('text-feed-input').value;
            const file = document.getElementById('pdf-feed-input').files[0];
            const formData = new FormData();

            if (textData) formData.append('text', textData);
            if (file) formData.append('file', file);

            if (!textData && !file) {
                alert("Please provide text or a file.");
                return;
            }

            try {
                const response = await fetch('/feed', { method: 'POST', body: formData });
                const result = await response.json();
                alert(result.message);
                closeModal();
            } catch (error) {
                console.error("Feed error:", error);
                alert("Error feeding agent.");
            }
        });
    });

    // --- Autonomous & Deep Thinking Logic ---
    const handleAutonomousModeToggle = async () => {
        if (autonomousToggle.checked) {
            const goal = prompt("Please provide the high-level goal for the autonomous agent:");
            if (goal) {
                try {
                    await fetch('/autonomous/start', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ goal }),
                    });
                    appendMessage(`Autonomous mode initiated with goal: "${goal}"`, 'ai');
                } catch (error) {
                    console.error('Error starting autonomous mode:', error);
                    appendMessage('There was an error starting autonomous mode.', 'ai');
                    autonomousToggle.checked = false;
                }
            } else {
                autonomousToggle.checked = false; // User cancelled prompt
            }
        } else {
            try {
                await fetch('/autonomous/stop', { method: 'POST' });
                appendMessage('Autonomous mode has been stopped.', 'ai');
            } catch (error) {
                console.error('Error stopping autonomous mode:', error);
            }
        }
    };

    const handleDeepThinkingToggle = async () => {
        try {
            await fetch('/deep_thinking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled: deepThinkingCheckbox.checked }),
            });
        } catch (error) {
            console.error('Error toggling deep thinking mode:', error);
        }
    };

    autonomousToggle.addEventListener('change', handleAutonomousModeToggle);
    deepThinkingCheckbox.addEventListener('change', handleDeepThinkingToggle);


    // --- Wake Word & Speech Recognition ---
    if (SpeechRecognition) {
        const startPersistentListening = () => {
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = () => {
                console.log("Persistent listener started.");
            };

            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0])
                    .map(result => result.transcript)
                    .join('')
                    .toLowerCase();

                if (transcript.includes(wakeWord)) {
                    console.log(`Wake word "${wakeWord}" detected!`);
                    recognition.stop();
                    activateFullRecognition();
                }
            };

            recognition.onerror = (event) => {
                console.error("Speech recognition error:", event.error);
                if (event.error === 'not-allowed') {
                    alert("Microphone access was denied. Please allow it to use voice features.");
                }
            };

            recognition.onend = () => {
                 // The listener can sometimes stop on its own, so we restart it.
                 // This ensures it's always listening in the background.
                if (!isActivatingFullRecognition) {
                    recognition.start();
                }
            };

            recognition.start();
        };

        let isActivatingFullRecognition = false;

        const activateFullRecognition = () => {
            isActivatingFullRecognition = true;
            listeningIndicator.classList.remove('hidden');

            const fullRecognition = new SpeechRecognition();
            fullRecognition.continuous = false;
            fullRecognition.interimResults = false;

            fullRecognition.onresult = (event) => {
                const command = event.results[0][0].transcript;
                userInput.value = command;
                sendMessage();
            };

            fullRecognition.onend = () => {
                listeningIndicator.classList.add('hidden');
                // Restart the persistent listener
                isActivatingFullRecognition = false;
                startPersistentListening();
            };

            fullRecognition.start();
        };

        const stopPersistentListening = () => {
            if (recognition) {
                recognition.stop();
            }
        };

        startPersistentListening(); // Start on page load

    } else {
        console.warn("Speech Recognition API not supported in this browser.");
    }

    // --- Initializers ---
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Load initial chat history or greeting
    loadHistory();
});
