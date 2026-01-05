import os
import logging
import json
from fastapi import FastAPI
from mcp.server import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from database_tools import DatabaseTools

logging.basicConfig(level=logging.INFO)

# ---------------- Database ----------------
DB_FILE = os.getenv("DB_FILE", "data.db")
db_tools = DatabaseTools(DB_FILE)
db_tools.init_database()

# ---------------- MCP ----------------
mcp = FastMCP(
    "mcp-database-server",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
        
)

# ---------------- MCP Tools ----------------
@mcp.tool()
def execute_query(sql: str) -> str:
    return json.dumps(db_tools.execute_query(sql), indent=2)

@mcp.tool()
def insert_user(name: str, email: str) -> str:
    return json.dumps(db_tools.insert_user(name, email))

@mcp.tool()
def insert_product(name: str, price: float, stock: int = 0) -> str:
    return json.dumps(db_tools.insert_product(name, price, stock))

@mcp.tool()
def update_user(user_id: int, name: str = None, email: str = None) -> str:
    return json.dumps(db_tools.update_user(user_id, name, email))

@mcp.tool()
def delete_user(user_id: int) -> str:
    return json.dumps(db_tools.delete_user(user_id))

@mcp.tool()
def get_all_users() -> str:
    return json.dumps(db_tools.get_all_users(), indent=2)

@mcp.tool()
def get_all_products() -> str:
    return json.dumps(db_tools.get_all_products(), indent=2)

@mcp.tool()
def get_database_info() -> str:
    return json.dumps(db_tools.get_database_info(), indent=2)

# ---------------- MCP APP ----------------
# ⚠️ MCP MUST be at root
app = mcp.streamable_http_app()
