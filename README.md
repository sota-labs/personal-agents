# Personal Agent

A sophisticated AI assistant system built with FastAPI and LLM integration, designed to help users with queries and tasks through natural language interaction, specifically optimized for cryptocurrency trading assistance.

## 🌟 Key Features

- **Multi-LLM Integration**
  - Google Gemini Pro
  - Anthropic Claude
  - DeepSeek
  - Customizable model selection

- **Advanced Trading Tools**
  - Real-time wallet balance tracking
  - Token search and analysis
  - Trending pairs monitoring
  - Position management
  - Price alerts

- **Intelligent Processing**
  - Context-aware conversations
  - Asynchronous message handling
  - Webhook integration
  - Persistent chat history
  - Stream response support

- **Security & Performance**
  - JWT authentication
  - Rate limiting
  - Error handling
  - Request validation
  - Logging system

## 🏗 Architecture

### Agent Runner (Orchestrator)
- Task state management
- Memory buffer handling
- Request scheduling
- API endpoint routing
- Webhook processing

### Agent Worker (Executor)
- Reasoning engine
- Tool selection logic
- Decision making
- Response formulation
- Context management

## 📁 Project Structure

```
personal-agents/
├── LLM/                    # LLM Integration
│   ├── llm_settings_manager.py
│   └── __init__.py
├── auth/                   # Authentication
│   ├── authorization.py
│   └── jwt_generator.py
├── commons/                # Shared Utilities
│   └── send_telegram.py
├── config/                 # Configuration
│   ├── settings.py
│   └── __init__.py
├── prompts/                # System Prompts
│   ├── react.py
│   └── __init__.py
├── routes/                 # API Routes
│   └── chat_agent.py
├── tools/                  # Trading Tools
│   ├── get_wallet_balance.py
│   ├── search_token.py
│   └── get_trending_pairs.py
├── utils/                  # Helpers
│   ├── chat_session.py
│   └── output_parser.py
├── app.py                  # Main Application
├── agents.py              # Core Agent Logic
└── docker-compose.yml     # Docker Config
```

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Docker (optional)
- API keys for LLM services

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal-agents.git
cd personal-agents
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the server:
```bash
bash runserver.sh
```

### Docker Setup

```bash
docker compose up --build -d
```

## ⚙️ Configuration

### Required Environment Variables

```env
# API Keys
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key

# Security
SECRET_KEY=your_jwt_secret_key

# API URLs
RAIDENX_API_COMMON_URL=https://api.example.com
RAIDENX_API_INSIGHT_URL=https://insight.example.com
RAIDENX_API_ORDERS_URL=https://orders.example.com
RAIDENX_API_WALLETS_URL=https://wallets.example.com
```

## 🔌 API Endpoints

### Chat Endpoints

#### Synchronous Chat
```http
POST /v1/chat/threads/messages/sync
```

#### Asynchronous Chat with Webhook
```http
POST /v1/chat/threads/messages
```

### Response Format
```json
{
  "message": "Bot response message",
  "timestamp": "2024-03-20 10:30:45",
  "user": "username",
  "chat_id": "thread_123"
}
```

## 🛠 Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- Email: hung.dang@sotatek.com
- Issue Tracker: [GitHub Issues](https://github.com/yourusername/personal-agents/issues)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Anthropic Claude](https://www.anthropic.com/claude)
