"""
hello.py — your first ever LLM API call.

What this does: sends one question to Claude over the Anthropic API
and prints the answer. If this runs, your entire setup works.
"""

from dotenv import load_dotenv   # reads your .env file
import anthropic                 # the official Anthropic library

load_dotenv()  # loads ANTHROPIC_API_KEY from .env into the environment

# The client automatically finds ANTHROPIC_API_KEY — you never paste
# the key into code. This is the safe pattern, from day one.
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",   # fast + cheap; right model for this project
    max_tokens=200,              # cap on the length of the reply
    messages=[
        {"role": "user", "content": "In one sentence: what is Astra International?"}
    ],
)

# The API returns a list of content blocks; for plain text, take the first.
print(message.content[0].text)
