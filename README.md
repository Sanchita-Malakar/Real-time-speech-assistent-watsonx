# Real-time-speech-assistent-watsonx
AI Voice Assistant (IBM Watsonx) A real-time voice assistant that converts speech to text, processes it using a Watsonx Agent, and responds with synthesized speech using IBM Cloud STT and TTS services.

# 🎤 Real-Time Voice Assistant with IBM WatsonX

A Python-based voice assistant that uses IBM Watson services for real-time speech-to-text (STT), AI-powered responses via WatsonX, and text-to-speech (TTS) conversion. Speak naturally in Indian English and get intelligent voice responses!

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![IBM Watson](https://img.shields.io/badge/IBM-Watson-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 🎙️ **Real-time Speech Recognition** - Captures live audio from your microphone
- 🧠 **AI-Powered Responses** - Uses IBM WatsonX AI Agent for intelligent conversations
- 🔊 **Natural Voice Output** - Converts AI responses to speech
- 🌏 **Indian English Support** - Optimized for Indian accent recognition
- 💬 **Conversational Interface** - Natural back-and-forth dialogue
- 🔄 **Continuous Listening** - Keeps listening until you say "exit"

---

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- Microphone and speakers
- Stable internet connection
- Windows/Linux/MacOS

### IBM Cloud Account
You'll need an IBM Cloud account with:
- IBM Watson Speech to Text service
- IBM Watson Text to Speech service  
- IBM WatsonX.ai deployment

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/watsonx-voice-assistant.git
cd watsonx-voice-assistant
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
sounddevice==0.4.6
numpy==1.24.3
ibm-watson==7.0.1
ibm-cloud-sdk-core==3.16.7
requests==2.31.0
pygame==2.5.2
```

---

## ⚙️ Configuration

### 1. Get IBM Watson Credentials

#### Speech to Text (STT):
1. Go to: https://cloud.ibm.com/catalog/services/speech-to-text
2. Create a service instance
3. Copy your **API Key** and **Service URL**

#### Text to Speech (TTS):
1. Go to: https://cloud.ibm.com/catalog/services/text-to-speech
2. Create a service instance
3. Copy your **API Key** and **Service URL**

#### WatsonX AI:
1. Go to: https://cloud.ibm.com/catalog/services/watsonx-ai
2. Create a deployment
3. Copy your **API Key** and **Deployment ID**

### 2. Create config.py

Create a `config.py` file in the root directory:

```python
# IBM Watson Speech to Text
STT_API_KEY = "your-stt-api-key"
STT_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com"

# IBM Watson Text to Speech
TTS_API_KEY = "your-tts-api-key"
TTS_URL = "https://api.us-south.text-to-speech.watson.cloud.ibm.com"

# IBM WatsonX AI
WATSONX_API_KEY = "your-watsonx-api-key"
WATSONX_DEPLOYMENT_ID = "your-deployment-id"
```

⚠️ **Never commit `config.py` to version control!** Add it to `.gitignore`

---

## 🎮 Usage

### Start the Voice Assistant
```bash
python main.py
```

### Interaction Flow
1. **Speak** when you see: `🎤 Speak now (clearly)...`
2. **Wait** for transcription: `🧑 You said: [your text]`
3. **Listen** to AI response: `🔊 Speaking: [response]`
4. **Continue** the conversation or say **"exit"** to quit

### Example Conversation
```
🤖 Watsonx Voice Assistant Started
🎤 Speak something... (say 'exit' to stop)

🎤 Speak now (clearly)...
🧑 You said: hello how are you
🤔 Thinking...
🤖 Agent reply: Hello! I'm doing well, thank you for asking. How can I help you today?
🔊 Speaking: Hello! I'm doing well...

🎤 Speak now (clearly)...
🧑 You said: what is artificial intelligence
🤔 Thinking...
🤖 Agent reply: Artificial intelligence is...
```

### Exit Commands
Say any of these to stop:
- "exit"
- "quit"
- "stop"
- "goodbye"

Or press `Ctrl+C` to interrupt

---

## 📁 Project Structure

```
watsonx-voice-assistant/
│
├── main.py              # Main application loop
├── stt.py               # Speech-to-Text module
├── tts.py               # Text-to-Speech module
├── agent.py             # WatsonX AI Agent integration
├── config.py            # API credentials (DO NOT COMMIT)
├── check_limit.py       # Quota checker utility
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

### Module Details

#### `main.py`
- Main application loop
- Coordinates STT, Agent, and TTS
- Handles user interaction flow

#### `stt.py`
- Captures live audio from microphone
- Converts speech to text using IBM Watson STT
- Optimized for Indian English accent

#### `tts.py`
- Converts text responses to speech
- Plays audio using pygame
- Uses IBM Watson TTS

#### `agent.py`
- Communicates with IBM WatsonX AI
- Manages authentication tokens
- Handles AI responses

#### `check_limit.py`
- Checks API quota and usage
- Diagnoses quota issues
- Provides upgrade guidance

### Having Issues?

1. **Check Troubleshooting section** above
2. **Run diagnostics**: `python check_limit.py`
3. **Review IBM Cloud console** for service status
4. **Open an issue** on GitHub with error details

## ⭐ Show Your Support

If this project helped you, please give it a ⭐️!

---

**Made with ❤️ using IBM Watson and WatsonX**

*Last Updated: January 2026*
