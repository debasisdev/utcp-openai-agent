import json
import asyncio
import re
import aiohttp
from dotenv import load_dotenv
from agents import Agent, Runner, FunctionTool
from utcp.utcp_client import UtcpClient
from utcp.data.utcp_client_config import UtcpClientConfigSerializer
from utcp.data.tool import Tool

async def initialize_utcp_client() -> UtcpClient:
    config = UtcpClientConfigSerializer().validate_dict(
        {
            "manual_call_templates": [
                {
                    "name": "service_catalog",
                    "call_template_type": "http",
                    "url": "http://127.0.0.1:3000/utcp",
                    "http_method": "GET"
                }
            ]
        }
    )
    
    client = await UtcpClient.create(config=config)
    return client

async def convert_api():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.github.com/openapi.json") as response:
            openapi_spec = await response.json()

    converter = OpenApiConverter(openapi_spec)
    manual = converter.convert()

    print(f"Generated {len(manual.tools)} tools from GitHub API!")
    return manual

def sanitize_tool_name(name: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    if not sanitized or not re.match(r'^[a-zA-Z0-9]', sanitized):
        sanitized = 'tool_' + sanitized
    return sanitized

def utcp_tool_to_agent_tool(utcp_client: UtcpClient, tool: Tool) -> FunctionTool:
    async def tool_invoke_handler(ctx, args: str) -> str:
        """
        Handler function for the UTCP tool invocation.
        """
        print(f"\n🤖 Agent is calling tool: {tool.name} with args: {args}")
        try:
            kwargs = json.loads(args) if args.strip() else {}
            
            result = await utcp_client.call_tool(tool.name, kwargs)
            print(f"✅ Tool {tool.name} executed successfully. Result: {result}")
            
            if isinstance(result, (dict, list)):
                return json.dumps(result)
            else:
                return str(result)
        except Exception as e:
            print(f"❌ Error calling tool {tool.name}: {e}")
            return f"Error: {str(e)}"

    params_schema = {"type": "object", "properties": {}, "required": []}
    
    if tool.inputs and tool.inputs.properties:
        inputs_dict = tool.inputs.model_dump(exclude_none=True)
        for prop_name, prop_schema in inputs_dict["properties"].items():
            params_schema["properties"][prop_name] = prop_schema
        
        if inputs_dict["required"]:
            params_schema["required"] = inputs_dict["required"]

    sanitized_name = sanitize_tool_name(tool.name)
    return FunctionTool(
        name=sanitized_name,
        description=tool.description or f"No description available for {tool.name}.",
        params_json_schema=params_schema,
        on_invoke_tool=tool_invoke_handler,
    )

async def main():
    load_dotenv(".env")
        
    print("🚀 Initializing UTCP client...")
    try:
        utcp_client = await initialize_utcp_client()
        utcp_tools = await utcp_client.config.tool_repository.get_tools()
        print(f"✅ UTCP client initialized. Found {len(utcp_tools)} tools.")
    except Exception as e:
        print(f"❌ Failed to initialize UTCP client or fetch tools: {e}")
        return

    agent_tools = [utcp_tool_to_agent_tool(utcp_client, tool) for tool in utcp_tools]

    print("\nSending request to OpenAI...")
    my_agent = Agent(
        name="Office Agent",
        instructions="You are a helpful and motivating assistant. You can find latitude and longitude of a City and provide it when required for fetching the accurate weather.",
        model="gpt-4o-mini",
        tools=agent_tools,
    )

    print("\n--- AI Assistant is ✅! ---")
    print("Type your request or 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("💪 Keep pushing! Goodbye!")
            break
        
        try:
            response_stream = await Runner.run(
                my_agent,
                user_input
            )
            
            print(response_stream)
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
    

if __name__ == "__main__":
    asyncio.run(main())