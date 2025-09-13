from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool , handoff
from agents.run import RunConfig
import os
import asyncio
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

fitness_coach = Agent(
    name="Fitness Coach",
    instructions=(
        "You're a running coach. Ask 1-2 quick questions, then give a week plan. "
        "Keep it simple and encouraging. No medical advice."
    ),
)

# Study Coach
study_coach = Agent(
    name="Study Coach",
    instructions=(
        "You're a study planner. Ask for current routine, then give a 1-week schedule. "
        "Keep steps small and doable."
    ),
)

# Router that decides who should OWN the conversation
router = Agent(
    name="Coach Router",
    instructions=(
        "Route the user:\n"
        "- If message is about running, workout, stamina → handoff to Fitness Coach.\n"
        "- If it's about exams, study plan, focus, notes → handoff to Study Coach.\n"
        "After handoff, the specialist should continue the conversation."
    ),
    handoffs=[study_coach, handoff(fitness_coach)],
)

async def main():
    # ---- Turn 1: user asks about running → should handoff to Fitness Coach
    r1 = await Runner.run(router, "I want to run a 5Km in 8 weeks. Can you help?", run_config=config)
    print("\nTurn 1 (specialist reply):\n", r1.final_output)

    # Grab the specialist that actually replied (Fitness Coach)
    specialist = r1.last_agent

    # ---- Turn 2: user answers the coach's follow-up; continue with SAME specialist
    t2_input = r1.to_input_list() + [
        {"role": "user", "content": "Right now I can jog about 2 km, 3 days per week."}
    ]
    r2 = await Runner.run(specialist, t2_input, run_config=config)
    print("\nTurn 2 (specialist reply):\n", r2.final_output)

    # ---- Turn 3: another follow-up; still same specialist
    t3_input = r2.to_input_list() + [
        {"role": "user", "content": "Nice. What should I eat on training days?"}
    ]
    r3 = await Runner.run(specialist, t3_input , run_config=config)
    print("\nTurn 3 (specialist reply):\n", r3.final_output)


if __name__ == "__main__":
    asyncio.run(main())