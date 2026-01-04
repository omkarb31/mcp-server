import asyncio
from mcp.client.streamable_http import streamable_http_client
from mcp.client.session import ClientSession

async def main():
    url = "http://localhost:8000/mcp"
    
    try:
        async with streamable_http_client(url) as (read_stream, write_stream, get_session_id):
            print("✓ Transport created successfully")
            
            async with ClientSession(read_stream, write_stream) as session:
                print("✓ Session created")
                
                # Initialize the connection
                init_result = await session.initialize()
                print(f"✓ Initialized: {init_result}")
                
                # List available tools
                tools = await session.list_tools()
                print(f"✓ Tools: {tools}")
                
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(main())