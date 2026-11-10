# 🎙️ Multilingual AI Voice Assistant

An AI-powered voice assistant that allows users to communicate naturally in **Telugu, Hindi, and English**. It converts speech into text, generates intelligent responses, and converts the responses back into speech.

## 🚀 Features

- 🎤 Voice recording through microphone
- 🌐 Supports Telugu, Hindi, and English
- 📝 Speech-to-Text using Gnani AI Prisma
- 🧠 Intelligent responses using Groq LLM
- 🔊 Text-to-Speech using Gnani AI Timbre
- 💬 Conversation history
- ▶️ AI-generated audio playback
- 📥 Audio download
- 🖥️ Interactive Streamlit interface

## 🛠️ Technologies Used

- Python
- Streamlit
- Gnani AI (Prisma STT and Timbre TTS)
- Groq API
- Python Requests
- Python-dotenv

## ⚙️ Project Architecture

1. User selects a language.
2. User records audio through the microphone.
3. Gnani AI Prisma converts speech into text.
4. Groq LLM generates an intelligent response.
5. Gnani AI Timbre converts the response into speech.
6. The application displays the answer and plays the generated audio.

## 📁 Project Structure

```text
Multilingual-AI-Voice-Assistant/
│
├── app.py
├── config.py
├── stt.py
├── llm.py
├── tts.py
├── requirements.txt
├── test_llm.py
├── test_tts.py
├── .gitignore
├── README.md
├── LICENSE
└── .env (create locally; do not upload)
```

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/teja0077-hari/Multilingual-AI-Voice-Assistant.git
```

### 2. Open the project folder

```bash
cd Multilingual-AI-Voice-Assistant
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project folder and add your API keys:

```env
GNANI_API_KEY_ID=your_gnani_api_key
GROQ_API_KEY=your_groq_api_key
```

**Important:** Never share or upload your API keys.

### 5. Run the application

```bash
streamlit run app.py
```

## 🌍 Supported Languages

- Telugu
- Hindi
- English

## 🎯 Project Objective

To develop a multilingual voice-based AI assistant that makes human-computer interaction easier through speech recognition, intelligent response generation, and speech synthesis.
## 🎥 Project Demo Video

[Watch the Multilingual AI Voice Assistant Demo](https://drive.google.com/file/d/1Gl-vO88MoADVucGWntNSx4HgxlTrJ5C5/view?usp=sharing)



## 👨‍💻 Author

**Hariteja Kodhaari**

- GitHub: https://github.com/teja0077-hari
- LinkedIn: https://www.linkedin.com/in/hariteja-kodhaari

---

*Developed as part of the Gnani AI Great Indian AI Internship Challenge.*
