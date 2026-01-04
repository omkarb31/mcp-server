# MCP Database Server

A Model Context Protocol (MCP) server for managing local SQLite database operations using **FastMCP** with an HTTP (streamable) transport.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```


### 2. Run the Server

```bash
python main_app.py
```

---

### 3. Access the Server

* **MCP HTTP Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **FastAPI Docs (if mounted)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

> ⚠️ Note: MCP must be mounted at the **root path** using `mcp.streamable_http_app()`.

---

## Features

* **Model Context Protocol (MCP)** server
* **FastMCP** with streamable HTTP transport
* **SQLite** local database
* **8 Database Tools** exposed to MCP clients
* **Safe Transport Configuration** (DNS rebinding configurable)
* **Structured JSON responses**
* **Simple local deployment**

---

## Environment Variables

Configure the server using environment variables:

```bash
# SQLite database file (default: data.db)
DB_FILE=data.db

# Optional FastAPI server settings
HOST=127.0.0.1
PORT=8000
```

### Example (PowerShell)

```powershell
$env:DB_FILE = "C:\path\to\database.db"
$env:PORT = "9000"
python main_app.py
```

---

## MCP Configuration (Claude Desktop)

Add the server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["/path/to/main_app.py"],
      "env": {
        "DB_FILE": "/path/to/data.db",
        "HOST": "127.0.0.1",
        "PORT": "8000"
      }
    }
  }
}
```

---

## Database Schema

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

## Available MCP Tools

The following tools are exposed via MCP:

1. **execute_query** – Execute SQL SELECT queries
2. **insert_user** – Insert a new user
3. **insert_product** – Insert a new product
4. **update_user** – Update user name or email
5. **delete_user** – Delete a user by ID
6. **get_all_users** – Retrieve all users
7. **get_all_products** – Retrieve all products
8. **get_database_info** – View database schema information

All responses are returned as formatted JSON strings.

---

## Project Structure

```text
.
├── main_app.py
├── database_tools.py
├── requirements.txt
├── data.db
└── README.md
```

---

## Example
<img width="1302" height="360" alt="image" src="https://github.com/user-attachments/assets/4c9ccb57-88f9-4c11-b616-fefa5cd2f6e2" />


## Testing

### MCP HTTP

Run the server and connect using any MCP-compatible client (e.g., Claude Desktop).


## Security Notes

* DNS rebinding protection is **disabled by default** for local development:

```python
TransportSecuritySettings(enable_dns_rebinding_protection=False)
```

Enable this for production deployments.

---
