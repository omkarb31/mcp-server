"""
Database Tools for MCP Database Server
Defines all database operations and MCP tools
"""

import sqlite3
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DatabaseTools:
    """Database tools for MCP server"""
    
    def __init__(self, db_file: str):
        """Initialize database tools with database file path"""
        self.db_file = db_file
    
    def get_db_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_file)
    
    def init_database(self):
        """Initialize the database with sample tables"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at: {self.db_file}")
    
    def execute_query(self, sql: str) -> dict[str, Any]:
        """
        Execute a SELECT query on the database.
        
        Args:
            sql: The SELECT SQL query to execute
            
        Returns:
            Dictionary with query results and row count
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Only allow SELECT queries for safety
            if not sql.strip().upper().startswith('SELECT'):
                return {
                    "success": False,
                    "error": "Only SELECT queries are allowed"
                }
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert rows to list of dicts
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            
            return {
                "success": True,
                "columns": columns,
                "rows": results,
                "row_count": len(results)
            }
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def insert_user(self, name: str, email: str) -> dict[str, Any]:
        """
        Insert a new user into the users table.
        
        Args:
            name: User's name
            email: User's email address
            
        Returns:
            Dictionary with operation result and new user ID
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            conn.commit()
            
            user_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"User inserted: ID={user_id}, name={name}, email={email}")
            
            return {
                "success": True,
                "user_id": user_id,
                "message": f"User '{name}' inserted successfully"
            }
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return {
                "success": False,
                "error": f"Integrity error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Insert error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def insert_product(self, name: str, price: float, stock: int = 0) -> dict[str, Any]:
        """
        Insert a new product into the products table.
        
        Args:
            name: Product name
            price: Product price
            stock: Product stock quantity (default: 0)
            
        Returns:
            Dictionary with operation result and new product ID
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', 
                          (name, price, stock))
            conn.commit()
            
            product_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Product inserted: ID={product_id}, name={name}, price={price}")
            
            return {
                "success": True,
                "product_id": product_id,
                "message": f"Product '{name}' inserted successfully"
            }
        except Exception as e:
            logger.error(f"Product insert error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> dict[str, Any]:
        """
        Update an existing user.
        
        Args:
            user_id: ID of the user to update
            name: New name (optional)
            email: New email (optional)
            
        Returns:
            Dictionary with operation result
        """
        try:
            if not name and not email:
                return {
                    "success": False,
                    "error": "At least one field (name or email) must be provided"
                }
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if name and email:
                cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', 
                              (name, email, user_id))
            elif name:
                cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
            else:
                cursor.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            logger.info(f"User updated: ID={user_id}, affected_rows={affected}")
            
            return {
                "success": True,
                "affected_rows": affected,
                "message": f"User {user_id} updated successfully"
            }
        except Exception as e:
            logger.error(f"Update error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_user(self, user_id: int) -> dict[str, Any]:
        """
        Delete a user from the database.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            Dictionary with operation result
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            
            affected = cursor.rowcount
            conn.close()
            
            logger.info(f"User deleted: ID={user_id}, affected_rows={affected}")
            
            return {
                "success": True,
                "affected_rows": affected,
                "message": f"User {user_id} deleted successfully"
            }
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_users(self) -> dict[str, Any]:
        """
        Retrieve all users from the database.
        
        Returns:
            Dictionary with all users
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                users.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "created_at": row[3]
                })
            
            conn.close()
            
            return {
                "success": True,
                "users": users,
                "count": len(users)
            }
        except Exception as e:
            logger.error(f"Get users error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_products(self) -> dict[str, Any]:
        """
        Retrieve all products from the database.
        
        Returns:
            Dictionary with all products
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, name, price, stock, created_at FROM products ORDER BY id')
            rows = cursor.fetchall()
            
            products = []
            for row in rows:
                products.append({
                    "id": row[0],
                    "name": row[1],
                    "price": row[2],
                    "stock": row[3],
                    "created_at": row[4]
                })
            
            conn.close()
            
            return {
                "success": True,
                "products": products,
                "count": len(products)
            }
        except Exception as e:
            logger.error(f"Get products error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_database_info(self) -> dict[str, Any]:
        """
        Get information about the database tables and their schemas.
        
        Returns:
            Dictionary with database schema information
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            schema_info = {}
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                schema_info[table] = [
                    {
                        "name": col[1],
                        "type": col[2],
                        "notnull": col[3],
                        "default": col[4],
                        "pk": col[5]
                    }
                    for col in columns
                ]
            
            conn.close()
            
            return {
                "success": True,
                "tables": tables,
                "schema": schema_info,
                "database_file": self.db_file
            }
        except Exception as e:
            logger.error(f"Get database info error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
