# 🌍 City Intelligence AI

**City Intelligence AI** is an AI-powered city information assistant built using **LangChain, Groq, Tavily, and Streamlit**. It helps users retrieve real-time weather information and the latest city news through natural language conversations.

The application uses LangChain tool calling to allow the LLM to decide when to invoke external tools. It also implements a **Human-in-the-Loop (HITL)** mechanism, where users can approve or deny tool execution before the requested action takes place.

## 🚀 Features

- **Weather Information:** Get current weather details for any city using the OpenWeatherMap API.
- **Latest City News:** Retrieve the latest news about a city using the Tavily Search API.
- **AI-Powered Conversations:** Interact with the assistant using natural language.
- **LangChain Tool Calling:** Dynamically selects and invokes tools based on user queries.
- **Human-in-the-Loop:** Approve or deny tool execution before the agent executes it.
- **Agent Loop:** Handles LLM responses, tool calls, and tool results.
- **Interactive UI:** Clean and modern chat interface built with Streamlit.
- **Conversation History:** Maintains chat messages using Streamlit Session State.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent and tool orchestration |
| Groq | LLM inference |
| GPT-OSS-120B | Language model |
| Tavily | Latest news search |
| OpenWeatherMap API | Weather information |
| Streamlit | Frontend user interface |
| python-dotenv | Environment variable management |
| Requests | HTTP API requests |

## 🏗️ Project Architecture

The application follows a tool-calling agent workflow.

```text
                User
                  |
                  v
          Streamlit Chat UI
                  |
                  v
              Groq LLM
                  |
                  v
          LangChain Tool Calling
                  |
          +-------+-------+
          |               |
          v               v
      Get Weather      Get News
          |               |
          v               v
   OpenWeatherMap       Tavily
          |               |
          +-------+-------+
                  |
                  v
          Human Approval
                  |
                  v
          Execute Selected Tool
                  |
                  v
           Tool Response
                  |
                  v
              Groq LLM
                  |
                  v
            Final Answer
                  |
                  v
             User Interface
```

## 📂 Project Structure

```text
City-Intelligence-AI/
│
├── main.py
│
├── .env
│
├── .gitignore
│
├── requirements.txt
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/City-Intelligence-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd City-Intelligence-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file in the root directory and add the following API keys:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Get API Keys:**

- Groq: https://console.groq.com/
- OpenWeatherMap: https://openweathermap.org/api
- Tavily: https://tavily.com/

### 6. Run the Application

```bash
streamlit run main.py
```

The application will start locally. Open the URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 🤖 How It Works

1. The user enters a question through the Streamlit chat interface.
2. The Groq LLM processes the question.
3. LangChain tool calling determines whether an external tool is required.
4. If a tool is required, the application displays an approval request.
5. The user can approve or deny the tool execution.
6. If approved, the selected tool executes and retrieves the requested information.
7. The tool response is added to the conversation messages.
8. The LLM processes the tool response and generates the final answer.

## 📚 Concepts Implemented

Through this project, I gained practical experience with:

- Generative AI and Large Language Models (LLMs).
- LangChain framework.
- Custom tool creation using `@tool`.
- LLM tool binding using `bind_tools()`.
- Function and tool calling.
- Agent execution loops.
- Human-in-the-Loop (HITL).
- Message management using `HumanMessage` and `ToolMessage`.
- Integrating external APIs with AI applications.
- Building interactive AI applications using Streamlit.

## 👨‍💻 Author

**Divakar B**

MCA Graduate | Python | Java | Generative AI | LangChain | Agentic AI | Full Stack Developer

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback!
