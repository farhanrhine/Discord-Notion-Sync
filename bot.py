import discord
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Setup Discord intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Setup LLM
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="hidden",
    timeout=None,
    max_retries=2,
    # other params...
)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return

    user_input = message.content

    # Only respond if message starts with "!"
    if user_input.startswith("!"):
        query = user_input[1:]

        # Show thinking message
        thinking_msg = await message.channel.send("🤔 Thinking...")

        try:
            # Get response from LLM
            response = llm.invoke(query)
            response_text = response.content

            # Edit message with response
            await thinking_msg.edit(content=response_text)

        except Exception as e:
            MAX_LENGTH = 1900
            chunks = [response_text[i:i+MAX_LENGTH] for i in range(0, len(response_text), MAX_LENGTH)]
            await thinking_msg.edit(content=chunks[0])
            for chunk in chunks[1:]:
                await message.channel.send(chunk)

# Run bot
client.run(DISCORD_TOKEN)