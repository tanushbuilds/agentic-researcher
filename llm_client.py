import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("ACTIVE_PROVIDER", "gemini").lower()

PROVIDERS = {
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model_fast": "gemini-2.5-flash",
        "model_smart": "gemini-2.5-flash",
    },
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
        "model_fast": "llama-3.1-8b-instant",
        "model_smart": "llama-3.3-70b-versatile",
    },
}

config = PROVIDERS[PROVIDER]

client = OpenAI(
    api_key=config["api_key"],
    base_url=config["base_url"]
)

MODEL_FAST = config["model_fast"]
MODEL_SMART = config["model_smart"]


def call_llm(prompt, mode="fast", temperature=0.7, max_tokens=None):
    model = MODEL_SMART if mode == "smart" else MODEL_FAST
    kwargs = dict(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content