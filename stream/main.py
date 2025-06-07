import os
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel 
from agents.run import RunConfig
from dotenv import load_dotenv  # ✅ Add this
from openai.types.responses import ResponseTextDeltaEvent


load_dotenv()
 
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
agent=Agent(name="Assistant",instructions="helper",model=model)

async def main():
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


# message handler user list 
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="Maintain a conversation with me").send()
@cl.on_message
async def handle_message(message: cl.Message):  
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    cl.user_session.set("history", history)

    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config
    )

    msg = cl.Message(content="")
    await msg.send()  # Send an initial empty message for streaming

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            msg.content += event.data.delta
            await msg.update()

# @cl.on_chat_start
# async def start():
#     await cl.Message(content="💡 *Made by Sidra Raza*").send()
