import streamlit as st
from streamlit.components.v1 import html
import time


# Streamlit page config and optional content
st.set_page_config(page_title="Finance AI Chatbot", layout="wide")

# Simulated bot response - replace with your actual API call
def get_bot_response(user_input):
    # Here, call your FastAPI /chat endpoint instead of this dummy response
    time.sleep(0.5)
    return f"🤖 You said: {user_input}"

# Inject CSS for floating button and chatbot panel
st.markdown(
    """
    <style>
    /* Floating chat button */
    #chatbot-btn {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #0072C6;
        color: white;
        font-size: 30px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: background-color 0.3s ease;
    }
    #chatbot-btn:hover {
        background-color: #005a9e;
    }

    /* Chat window panel */
    #chatbot-panel {
        position: fixed;
        bottom: 100px;
        right: 25px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        display: none;
        flex-direction: column;
        z-index: 9998;
        overflow: hidden;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    #chatbot-panel.open {
        display: flex;
        animation: slideIn 0.3s forwards;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px);}
        to { opacity: 1; transform: translateY(0);}
    }

    /* Chat header */
    #chatbot-header {
        background-color: #0072C6;
        color: white;
        padding: 15px;
        font-weight: 600;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    #chatbot-close {
        cursor: pointer;
        font-weight: bold;
        font-size: 22px;
        user-select: none;
    }

    /* Chat messages area */
    #chatbot-messages {
        flex-grow: 1;
        padding: 15px;
        overflow-y: auto;
        background-color: #f8f9fa;
    }

    /* User message */
    .message.user {
        background-color: #0072C6;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        max-width: 75%;
        margin: 6px 0;
        align-self: flex-end;
        font-size: 14px;
        white-space: pre-wrap;
    }

    /* Bot message */
    .message.bot {
        background-color: #e2e3e5;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        max-width: 75%;
        margin: 6px 0;
        align-self: flex-start;
        font-size: 14px;
        white-space: pre-wrap;
    }

    /* Chat input area */
    #chatbot-input-area {
        display: flex;
        border-top: 1px solid #ddd;
    }

    #chatbot-input {
        flex-grow: 1;
        border: none;
        padding: 12px 15px;
        font-size: 14px;
        outline: none;
        border-radius: 0 0 0 10px;
    }

    #chatbot-send-btn {
        background-color: #0072C6;
        border: none;
        color: white;
        padding: 0 20px;
        cursor: pointer;
        font-size: 16px;
        border-radius: 0 0 10px 0;
        transition: background-color 0.3s ease;
    }

    #chatbot-send-btn:hover {
        background-color: #005a9e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inject chatbot HTML and JS
chatbot_html = """
<div id="chatbot-btn" title="Chat with Finance AI">💬</div>

<div id="chatbot-panel" aria-label="Finance AI Chatbot">
  <div id="chatbot-header">
    Finance AI Chatbot
    <div id="chatbot-close" title="Close Chat">×</div>
  </div>
  <div id="chatbot-messages" role="log" aria-live="polite" aria-relevant="additions"></div>
  <div id="chatbot-input-area">
    <input id="chatbot-input" type="text" aria-label="Type your message" placeholder="Type your message here..." />
    <button id="chatbot-send-btn" aria-label="Send message">Send</button>
  </div>
</div>

<script>
const chatbotBtn = document.getElementById('chatbot-btn');
const chatbotPanel = document.getElementById('chatbot-panel');
const chatbotClose = document.getElementById('chatbot-close');
const messagesContainer = document.getElementById('chatbot-messages');
const inputBox = document.getElementById('chatbot-input');
const sendBtn = document.getElementById('chatbot-send-btn');

let isOpen = false;

// Toggle chatbot panel
chatbotBtn.onclick = () => {
  isOpen = !isOpen;
  chatbotPanel.classList.toggle('open', isOpen);
  if (isOpen) {
    inputBox.focus();
  }
};

// Close button closes panel
chatbotClose.onclick = () => {
  isOpen = false;
  chatbotPanel.classList.remove('open');
  chatbotBtn.focus();
};

// Append message
function appendMessage(from, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', from);
  msgDiv.textContent = text;
  messagesContainer.appendChild(msgDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Handle sending message
async function sendMessage() {
  const userText = inputBox.value.trim();
  if (!userText) return;
  appendMessage('user', userText);
  inputBox.value = '';
  inputBox.disabled = true;
  sendBtn.disabled = true;

  // Call Streamlit backend via Streamlit's JS-to-Python bridge:
  // Here we use Streamlit's custom event handler
  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: "streamlit_user", message: userText })
  });
  const data = await response.json();

  appendMessage('bot', data.response || "Sorry, no response.");
  inputBox.disabled = false;
  sendBtn.disabled = false;
  inputBox.focus();
}

// Send button click
sendBtn.onclick = sendMessage;

// Send on Enter key
inputBox.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});
</script>
"""

# Place chatbot UI on page using components.html with height enough for hidden panel
html(chatbot_html, height=600)



st.markdown(
    """
    # Welcome to the Finance AI Dashboard
    Use the chat widget at the bottom-right to ask questions or analyze transactions.
    """
)
