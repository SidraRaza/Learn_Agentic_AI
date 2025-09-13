from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import os
from dotenv import load_dotenv 


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# 333333
#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


@function_tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    return f"The current weather in {location} is sunny with a high of 25°C."


@function_tool
def get_add_items(item1: str, item2: str) -> str:
    """Add two items."""
    return f"The sum of {item1} and {item2} is {int(item1) + int(item2)}."

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant",tools=[get_weather, get_add_items])

result = Runner.run_sync(agent, "What is 2 - 4", run_config=config)

print(result.final_output)