# client.py - Enhanced with real LLM decision-making
import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import StructuredTool

async def run_simple_test():
    """Simple test using streamable HTTP client"""
    try:
        async with streamable_http_client(url="http://127.0.0.1:8000/mcp") as (read, write, id):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # List tools
                tools = await session.list_tools()
                print("\n📋 Available Tools:")
                for tool in tools.tools:
                    print(f"  • {tool.name}: {tool.description}")
                
                # Test 1: Get all users
                print("\n" + "="*60)
                print("Test 1: Get all users")
                print("="*60)
                result = await session.call_tool("get_all_users", {})
                print(f"Result: {result.content}")
                
                # Test 2: Insert user
                print("\n" + "="*60)
                print("Test 2: Insert user")
                print("="*60)
                result = await session.call_tool("insert_user", {
                    "name": "Alice",
                    "email": "alice@example.com"
                })
                print(f"Result: {result.content}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

async def run_llm_agent():
    """Run LLM agent that decides which tools to call based on user questions"""
    
    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    
    try:
        async with streamable_http_client(url="http://127.0.0.1:8000/mcp") as (read, write, id):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get MCP tools
                tools_response = await session.list_tools()
                print(f"\n✅ Connected! Found {len(tools_response.tools)} tools\n")
                
                # Convert MCP tools to LangChain tools
                lc_tools = []
                
                # Store tool names for closure
                tool_map = {}
                for mcp_tool in tools_response.tools:
                    tool_name = mcp_tool.name
                    tool_desc = mcp_tool.description or f"Tool: {tool_name}"
                    tool_map[tool_name] = tool_name
                    
                    # Create wrapper function for each tool
                    def make_tool_func(name):
                        async def tool_func(**kwargs):
                            print(f"  🔧 Executing: {name} with args: {kwargs}")
                            result = await session.call_tool(name, kwargs)
                            # Extract content from result
                            if hasattr(result, 'content'):
                                if isinstance(result.content, list):
                                    content = "\n".join([
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ])
                                else:
                                    content = str(result.content)
                            else:
                                content = str(result)
                            print(f"  📊 Result: {content[:150]}...")
                            return content
                        return tool_func
                    
                    lc_tool = StructuredTool.from_function(
                        coroutine=make_tool_func(tool_name),
                        name=tool_name,
                        description=tool_desc
                    )
                    lc_tools.append(lc_tool)
                
                print("📋 Tools available to LLM:")
                for tool in lc_tools:
                    print(f"  • {tool.name}")
                
                # Bind tools to LLM
                llm_with_tools = llm.bind_tools(lc_tools)
                
                # Test different queries where LLM decides what to do
                queries = [
                    "Show me all users in the database",
                    "Add a new user named Charlie Brown with email charlie@peanuts.com",
                    "What's the structure of the database?",
                    "List all products available"
                ]
                
                for query in queries:
                    print("\n" + "="*70)
                    print(f"💬 User Question: {query}")
                    print("="*70)
                    
                    messages = [HumanMessage(content=query)]
                    
                    # Agent loop - LLM decides which tools to call
                    max_iterations = 5
                    for iteration in range(max_iterations):
                        print(f"\n🤖 Iteration {iteration + 1}:")
                        
                        # Get LLM response
                        response = await llm_with_tools.ainvoke(messages)
                        messages.append(response)
                        
                        # Check if LLM is done (no more tool calls)
                        if not response.tool_calls:
                            print(f"\n✅ Final Answer: {response.content}\n")
                            break
                        
                        # LLM wants to call tools
                        print(f"  🧠 LLM decided to call {len(response.tool_calls)} tool(s):")
                        
                        # Execute each tool call
                        for tool_call in response.tool_calls:
                            tool_name = tool_call['name']
                            tool_args = tool_call['args']
                            
                            print(f"    → {tool_name}({tool_args})")
                            
                            try:
                                # Call the MCP tool
                                result = await session.call_tool(tool_name, tool_args)
                                
                                # Extract content
                                if hasattr(result, 'content'):
                                    if isinstance(result.content, list):
                                        result_text = "\n".join([
                                            item.text if hasattr(item, 'text') else str(item)
                                            for item in result.content
                                        ])
                                    else:
                                        result_text = str(result.content)
                                else:
                                    result_text = str(result)
                                
                                # Add tool result back to conversation
                                messages.append(ToolMessage(
                                    content=result_text,
                                    tool_call_id=tool_call['id']
                                ))
                                
                            except Exception as e:
                                error_msg = f"Error: {str(e)}"
                                print(f"    ❌ {error_msg}")
                                messages.append(ToolMessage(
                                    content=error_msg,
                                    tool_call_id=tool_call['id']
                                ))
                    
                    await asyncio.sleep(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 MCP Client Test\n")
    
    # Option 1: Run simple manual tests
    # print("=" * 60)
    # print("Running simple MCP tests")
    # print("=" * 60)
    # asyncio.run(run_simple_test())
    
    # Option 2: Run LLM-powered agent
    print("=" * 60)
    print("Running LLM-Powered Agent")
    print("=" * 60)
    print("The LLM will analyze questions and decide which tools to call!\n")
    asyncio.run(run_llm_agent())