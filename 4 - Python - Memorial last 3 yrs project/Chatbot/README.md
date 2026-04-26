# 🤖 Voice-Controlled OpenAI Chatbot

## Project Overview

This project demonstrates a simple yet interactive voice-controlled chatbot built using Python. It leverages OpenAI's language models for generating responses, `pyttsx3` for text-to-speech output, and `speech_recognition` for processing voice commands. The chatbot provides a conversational experience, allowing users to interact with an AI through spoken language.

## ✨ Features

*   **Voice Input:** Recognizes spoken commands and questions using `speech_recognition`.
*   **AI-Powered Responses:** Generates intelligent and contextually relevant replies using OpenAI's API.
*   **Text-to-Speech Output:** Speaks out the AI's responses using `pyttsx3`.
*   **Conversational Memory:** Maintains a basic conversation history to provide more coherent interactions.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **`openai` library:** For interacting with OpenAI's language models.
*   **`pyttsx3`:** A cross-platform text-to-speech conversion library.
*   **`speech_recognition`:** For performing speech recognition with various engines and APIs.
*   **`api_secrets.py`:** A local file to securely store your OpenAI API key.

## 🚀 How It Works

1.  **API Key Setup:** The project requires an OpenAI API key, which is loaded from `api_secrets.py`.
2.  **Speech Recognition:** The `speech_recognition` library listens for user input through a microphone.
3.  **OpenAI Interaction:** The recognized speech is sent to OpenAI's API as a prompt, along with the ongoing conversation history.
4.  **Response Generation:** OpenAI generates a text response based on the prompt.
5.  **Text-to-Speech:** The generated text response is then converted into speech using `pyttsx3` and played back to the user.
6.  **Conversation Loop:** The process repeats, allowing for continuous interaction.

## 📊 Project Structure

```
Chatbot/
├── chatbot.py       # Main script for the voice-controlled chatbot
├── api_secrets.py   # (You need to create this file) Stores your OpenAI API key
└── README.md        # Project documentation
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   An OpenAI API Key.
*   A working microphone.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Python/Chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install openai pyttsx3 SpeechRecognition
    ```

3.  **Create `api_secrets.py`:**
    Create a file named `api_secrets.py` in the `Chatbot` directory and add your OpenAI API key:
    ```python
    API_KEY = "YOUR_OPENAI_API_KEY"
    ```
    Replace `"YOUR_OPENAI_API_KEY"` with your actual OpenAI API key.

### Running the Application

```bash
python chatbot.py
```

**Note:** You might need to adjust the `device_index` for your microphone in `chatbot.py` (line 12) if the default doesn't work. You can uncomment `print(sr.Microphone.list_microphone_names())` to see available microphone devices.

## 💡 Future Enhancements

*   **Advanced Conversation Management:** Implement more sophisticated conversation flow and context handling.
*   **Error Handling:** Improve error handling for API calls and speech recognition failures.
*   **Customizable Voice:** Allow users to choose different voices or speaking styles.
*   **Integration with Other Services:** Connect the chatbot to other APIs for fetching real-time information (e.g., weather, news).
*   **GUI Interface:** Develop a graphical user interface for a more visually appealing interaction.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
