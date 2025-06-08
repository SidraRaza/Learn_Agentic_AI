import os
from agents import Agent , Runner , AsyncOpenAI , OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Key is missing")

externat_client=AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=externat_client
)
config=RunConfig(
    model=model,
    model_provider=externat_client,
    tracing_disabled=True

)
agent=Agent(name="Assistant",instructions="helper",model=model)
result=Runner.run_sync(agent,"who is the founder of pakistan",run_config=config)
print(result.final_output)
