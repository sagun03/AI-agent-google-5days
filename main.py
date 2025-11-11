import asyncio
import os
from dotenv import load_dotenv

# from agent import create_agents
from blog_agent import create_agents

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Ensure the API key is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")


async def main():
    runner = create_agents()

    # debuug for multi agent
    # response = await runner.run_debug(
    #     "What are the latest advancements in quantum computing and what do they mean for AI?"
    # )
    # print("\n🧩 Final Summary:\n", response)

    # Run the agent with a sample blog topic
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )
    print("\n🧩 Final Blog Post:\n", response)


if __name__ == "__main__":
    asyncio.run(main())
