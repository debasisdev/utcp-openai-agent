import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from openai_bridge import initialize_utcp_client, utcp_tool_to_agent_tool

async def main():
    load_dotenv(".env")
        
    print("🚀 Initializing UTCP client...")
    try:
        utcp_client = await initialize_utcp_client()
        utcp_tools = await utcp_client.config.tool_repository.get_tools()
        print(f"✅ UTCP client initialized. Found {len(utcp_tools)} tools.")
    except Exception as e:
        print(f"❌ Failed to initialize UTCP tools: {e}")
        return

    agent_tools = [utcp_tool_to_agent_tool(utcp_client, tool) for tool in utcp_tools]

    my_agent = Agent(
        name="Office Agent",
        instructions="You are a helpful and motivating assistant. Always encourage users to stay positive and keep pushing forward!",
        model="gpt-4o-mini",
        tools=agent_tools,
    )

    print("\n---✅ AI Assistant is ✅! ---")
    print("Type your request or 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("\n👋🏼 Ciao!")
            break
        
        try:
            response_stream = await Runner.run(my_agent,user_input)
            print(f"\n{response_stream.final_output}")
            
        except Exception as e:
            print(f"\nError occurred: {e}")
    

if __name__ == "__main__":
    asyncio.run(main())