from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.genai import types


def create_agents():
    """Creates and returns the root agent and runner."""

    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

    # Research Agent
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    # Summarizer Agent
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
        instruction="""Read the provided research findings: {research_findings}
Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    # Root Agent
    root_agent = Agent(
        name="ResearchCoordinator",
        model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
        instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
1. First, call `ResearchAgent` to find relevant information.
2. Then call `SummarizerAgent` to create a concise summary.
3. Present the summary clearly to the user.""",
        tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
    )

    runner = InMemoryRunner(agent=root_agent)
    return runner
