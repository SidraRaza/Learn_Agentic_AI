import chainlit as cl
import os 
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("error")

provider=AsyncOpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config=RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
aent=Agent(
    name="Asistnent",
    instructions="helper",
    model=model
)

result=Runner.run_sync(Agent,"who is the founder of pakistan",config=RunConfig)
print(result.final_output)