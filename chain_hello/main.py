import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,enable_verbose_stdout_logging,function_tool
from agents.run import RunConfig
from dotenv import load_dotenv 


load_dotenv()
enable_verbose_stdout_logging()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Check if the API key is present; if not, raise an error
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
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
@function_tool()
def weather(city: str) -> str:
  return f"The weather in {city} is sunny with a high of 25°C."

agent: Agent = Agent(name="Assistant", tools=[weather], model=model)
user_input = input("Enter your message: ")
result = Runner.run_sync(agent, user_input, run_config=config)

print("\nANSWER AGENT\n")
print(result.final_output)