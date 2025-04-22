# 🧠 NeuroMentor: A GenAI-powered Mental Wellness Companion

> *"Transforming mental wellness through compassionate AI."* 🌟

---

## 📋 Overview

**NeuroMentor** is an AI-powered mental wellness companion designed for students, professionals, and job-seekers facing stress and emotional challenges.  
It blends **Generative AI (Gemini 1.5 Pro, Gemini Pro Vision)**, **LangChain**, and **custom agents** to offer private, supportive, and empathetic interactions.

Built during the **Google x Kaggle Gen AI Intensive 2025**, NeuroMentor showcases real-world GenAI applications like RAG, Few-Shot Agents, Emotional Chatbots, Document Insights, and Voice-enabled Conversations.

---

## 🚀 Features

| Feature | Description |
|:--------|:------------|
| 🧠 Emotion-aware Journaling | Structured output prompts for emotional check-ins |
| 📚 Personal Document Analysis | Upload documents/images for emotional insights |
| 🎙️ Voice Lounge | Speak naturally; AI responds empathetically |
| 🌐 Real-time Web Search | Live, grounded information with web references |
| 🧩 Adaptive Agents | Personalized few-shot prompting and agent-based emotional support |
| 📈 Mood Analytics | Track mood over sessions with visualizations |
| 🔒 Secure & Private | Local session storage; no external sharing |

---

## 🎯 Problem Statement

> Mental health is a growing concern in fast-paced environments.  
> NeuroMentor offers a private, intelligent, always-available companion to guide, motivate, and support mental well-being.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Gemini 1.5 Pro APIs (Text & Vision)
- **Agent Framework**: LangChain
- **Voice Tech**: SoundDevice, SpeechRecognition, Pyttsx3
- **Vector Search**: Chroma VectorDB
- **Others**: HuggingFace Transformers, Serper.dev for Web Search

---

## 🛠️ Key Features
**🎤 Voice Lounge:** Speak freely, NeuroMentor listens and responds supportively.

**💬 ChatterBox:** Emotion-aware text chat, with positive psychology techniques.

**📄 Docs & Images:** Upload documents, analyze emotions, and ask questions.

**🌐 Search Solutions:** Live web search for mental health topics.

**📊 History & Insights:** Visualize your emotional journey across sessions.

---

## 📚 GenAI Capabilities Demonstrated

- ✅ Structured Output / JSON Mode
- ✅ Few-Shot Prompting
- ✅ Document Understanding
- ✅ Image Understanding
- ✅ Agents
- ✅ Retrieval Augmented Generation (RAG)
- ✅ Embeddings + Vector Search
- ✅ Audio Understanding (STT and TTS)

---

## 🛡️ Security & Data Privacy

- All user data (chats, voice sessions) are saved **locally** in `data/chat_sessions/` by username.
- No personal data is sent to external servers except when querying Gemini or Serper.dev APIs.
- No user authentication tokens are hardcoded; sensitive keys are managed securely via `.env` file.
- TTS (Text-to-Speech) and STT (Speech-to-Text) processing is done locally where possible.

---

## 🎨 Innovation
Unlike a standard chatbot, NeuroMentor offers:

- Natural conversational tone (WhatsApp-like)
- Private journaling and reflection insights
- Continuous emotional memory and history
- Cross-modal support (voice + text + documents)

It brings real-world impact by empowering users to take charge of their emotional health using AI.

---

## 📦 Installation & Setup

**1. Clone the Repository**

    ```bash
    git clone https://github.com/your-username/neuromentor.git
    cd neuromentor

**2. Install Dependencies**

    ```bash
    pip install -r requirements.txt

**3. Configure Environment Variables**

Create a .env file:

    ```bash
    GOOGLE_API_KEY=your_google_generativeai_key
    SERPER_API_KEY=your_serper_dev_key

✅ Important: Never expose your API keys publicly!

**4. Run the Application**

    ```bash
    streamlit run app.py

---

## 📁 Folder Structure
 neuromentor/
├── app.py                  # Main Streamlit app
├── requirements.txt         # Required Python packages
├── .env                     # Environment variables (keep secret)
├── assets/                  # Logos, style.css
├── components/              # Streamlit UI components (home, chat, voice, etc.)
├── utils/                   # Utilities (voice_utils, vision_utils, llm, etc.)
├── services/                # User auth and session management
├── agent/                   # NeuroMentor agent and tools
├── data/                    # User-specific chat history storage
└── README.md                # This file

---

## 🎥 Demo Video
**Demo:** [YouTube Demo Link Here] (https://youtu.be/kuIdqiiyhxM)

---

## ✍️ Blog Post
**Blog:** [Medium Blog Link] (https://medium.com/@ayesha24banu/neuromentor-a-genai-powered-mental-wellness-companion-58e01548b2a2)

---
## 📹 video Execution
**Demo:**


https://github.com/user-attachments/assets/bcb3cb03-05df-4361-ac1b-34e201e7eb78


---

## 👩‍💻 Contribution
Contributions are welcome! Feel free to fork the repo and submit a pull request 🚀.

---

## 📜 License
This project is licensed under the MIT License — free for personal and educational use.

---

## 💬 Acknowledgements

- Google Cloud Gen AI APIs
- Kaggle x Google Gen AI Intensive Course
- HuggingFace Transformers
- Streamlit Community
- Serper.dev API

---

## 🏆 Conclusion
Through Generative AI and a caring design philosophy, NeuroMentor represents a meaningful step forward in AI-assisted mental wellness.

I’m excited to keep evolving it — making AI not just smart, but emotionally supportive and empowering. 🌟

---

## 📞 Contact Information

If you have any questions, suggestions, or collaboration ideas, feel free to reach out:

- **Name:** Ayesha Banu
- **Email:** ayesha24banu@gmail.com
- **Kaggle:** [kaggle.com/ayesha990](https://www.kaggle.com/ayesha990)
- **LinkedIn:** [linkedin.com/in/ayesha-banu-cs](https://www.linkedin.com/in/ayesha-banu-cs/)
- **GitHub:** [github.com/Ayesha24banu](https://github.com/Ayesha24banu)

---

🔔 _Feel free to connect for project discussions, hiring, collaborations, or mentorship opportunities!_


