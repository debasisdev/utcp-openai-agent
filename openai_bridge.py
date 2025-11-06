import json
import re
from agents import FunctionTool
from utcp.utcp_client import UtcpClient
from utcp.data.tool import Tool
from utcp_http.openapi_converter import OpenApiConverter

async def initialize_utcp_client() -> UtcpClient:
    client = await UtcpClient.create(config="./utcp-config.json")
    return client

async def convert_openapi_spec():
    with open('./openapi-spec.json') as fp:
        data = json.load(fp)
        converter = OpenApiConverter(data)
        manual = converter.convert()

        print(manual.model_dump())

def sanitize_tool_name(name: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    if not sanitized or not re.match(r'^[a-zA-Z0-9]', sanitized):
        sanitized = 'tool_' + sanitized
    return sanitized

def utcp_tool_to_agent_tool(utcp_client: UtcpClient, tool: Tool) -> FunctionTool:
    async def tool_invoke_handler(ctx, args: str) -> str:
        print(f"\n🤖 Agent is calling tool: {tool.name} with args: {args}")
        try:
            kwargs = json.loads(args) if args.strip() else {}
            
            result = await utcp_client.call_tool(tool.name, kwargs)
            print(f"✅ Tool {tool.name} executed successfully")
            
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
