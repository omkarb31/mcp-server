# MCP Database Server

A **Model Context Protocol (MCP)** server for managing a local SQLite database using **FastMCP** with a **streamable HTTP transport**, plus an **LLM-powered MCP client** that can reason about user questions and automatically decide which database tools to call.

---

## 🌟 Overview

This project demonstrates:

- ✅ An MCP-compliant database server
- ✅ SQLite-backed CRUD operations exposed as MCP tools
- ✅ HTTP (streamable) MCP transport
- ✅ A Python client using **LangChain + Ollama**
- ✅ Real LLM-driven decision-making over MCP tools

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the MCP Server

```bash
python main_app.py
```

### 3. Server Endpoints

* **MCP Endpoint**: http://127.0.0.1:8000/mcp
* **Health Check**: http://127.0.0.1:8000/health
* **FastAPI Docs**: http://127.0.0.1:8000/docs
* **ReDoc**: http://127.0.0.1:8000/redoc

> ⚠️ MCP must be mounted at the **root path** using `mcp.streamable_http_app()`.

---

## ✨ Features

### MCP Server

* 🔌 Model Context Protocol (MCP) compliant
* ⚡ FastMCP with streamable HTTP transport
* 💾 SQLite local database
* 🛠️ 8 structured database tools
* 📊 JSON-formatted responses
* 🏠 Simple local deployment

### MCP Client / LLM Agent

* 🌐 Streamable HTTP MCP client
* 🔍 Automatic tool discovery
* 🔗 LangChain `StructuredTool` integration
* 🤖 Ollama-powered local LLM
* 🧠 Multi-step tool execution and reasoning loop

---

## ⚙️ Environment Variables

```bash
DB_FILE=data.db
HOST=127.0.0.1
PORT=8000
```

### Example (PowerShell)

```powershell
$env:DB_FILE="C:\path\to\data.db"
$env:PORT="8000"
python server.py
```

---

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛠️ Available MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `execute_query` | Execute SQL SELECT queries |
| `insert_user` | Insert a new user |
| `insert_product` | Insert a new product |
| `update_user` | Update user name or email |
| `delete_user` | Delete a user by ID |
| `get_all_users` | Retrieve all users |
| `get_all_products` | Retrieve all products |
| `get_database_info` | View database schema information |

All tools return formatted JSON strings.

---

## 🤖 LLM-Powered MCP Client

The client (`client.py`) connects to the MCP server and allows an LLM to:

1. 🔍 Discover available MCP tools
2. 💬 Analyze natural-language questions
3. 🎯 Decide which tools to call
4. ⚙️ Execute tools automatically
5. ✅ Produce a final response

---

### Requirements (Client)

**Install Ollama:**
- Download from [ollama.ai](https://ollama.ai)
- Pull a model:

```bash
ollama pull llama3.2:1b
# or for better tool calling:
ollama pull llama3.2:3b
```

**Install Python dependencies:**

```bash
pip install langchain-ollama langchain-core mcp
```

---

### Running the Client

**Start the MCP server first:**

```bash
python main_app.py
```

**Then run the client:**

```bash
python client.py
```

---

### Example Queries

The LLM dynamically selects and executes the correct MCP tools:

```text
✅ "Show me all users in the database"
✅ "Add a new user named Charlie Brown with email charlie@peanuts.com"
✅ "What's the structure of the database?"
✅ "List all products available"
✅ "Insert a product called Laptop with price 999.99"
```
<img width="1302" height="360" alt="image" src="https://github.com/user-attachments/assets/4c9ccb57-88f9-4c11-b616-fefa5cd2f6e2" />
---

## 📁 Project Structure

```text
.
├── main_app.py            # MCP server (FastMCP)
├── database_tools.py    # Database CRUD operations
├── client.py            # LLM-powered MCP client
├── requirements.txt     # Python dependencies
├── data.db              # SQLite database (auto-created)
└── README.md            # This file
```

---

## 🧪 Testing

Test the MCP server with:

1. **Claude Desktop** (MCP integration)
2. **Custom Python client** (`client.py`)
3. **Any MCP-compatible client**

### Manual Tool Testing

```bash
python test_fastmcp.py
```

---

## 🔒 Security Notes

⚠️ DNS rebinding protection is **disabled by default** for local development:

```python
TransportSecuritySettings(enable_dns_rebinding_protection=False)
```

**Enable this for production deployments.**

---

## 📦 requirements.txt

```txt
fastapi
uvicorn[standard]
mcp
langchain-ollama
langchain-core
```

---

## 🎯 How It Works

### Server Flow

```
User Query → MCP Client → HTTP Request → FastMCP Server → Database Tools → SQLite
                                                                          ↓
User Answer ← LLM Processing ← Tool Results ← JSON Response ← Database Query
```

### Client Flow

```
1. Connect to MCP server via streamable HTTP
2. Discover available tools
3. Convert MCP tools to LangChain tools
4. Bind tools to LLM (Ollama)
5. User asks question in natural language
6. LLM analyzes question and decides which tools to call
7. Execute tools via MCP
8. LLM formulates final answer
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🙏 Acknowledgments

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.ai/)

---

## 📞 Support

If you encounter issues:

1. Check that Ollama is running: `ollama list`
2. Verify server is running: `curl http://127.0.0.1:8000/health`
3. Check server logs for errors
4. Try a larger model: `ollama pull llama3.2:3b`

---
