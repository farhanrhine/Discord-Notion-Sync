import discord
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

from notion import save_note, read_notes

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
)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return

    user_input = message.content

    # ----------------------------
    # ✅ NOTION ROUTING FIRST
    # ----------------------------
    if user_input.startswith("!note save"):
        text = user_input.replace("!note save", "").strip()

        if not text:
            await message.channel.send("❌ Please provide text to save.")
            return

        try:
            save_note(text)
            await message.channel.send("✅ Saved to Notion")
        except Exception as e:
            await message.channel.send(f"❌ Notion save failed: {str(e)}")
        return

    elif user_input.startswith("!note read"):
        try:
            notes = read_notes()
            await message.channel.send(notes[:1900])
        except Exception as e:
            await message.channel.send(f"❌ Notion read failed: {str(e)}")
        return

    # ----------------------------
    # ✅ LLM HANDLING
    # ----------------------------
    if user_input.startswith("!"):
        query = user_input[1:]

        thinking_msg = await message.channel.send("🤔 Thinking...")

        try:
            response = llm.invoke(query)
            response_text = response.content

            # Handle long responses
            MAX_LENGTH = 1900
            chunks = [
                response_text[i:i+MAX_LENGTH]
                for i in range(0, len(response_text), MAX_LENGTH)
            ]

            await thinking_msg.edit(content=chunks[0])

            for chunk in chunks[1:]:
                await message.channel.send(chunk)

        except Exception as e:
            await thinking_msg.edit(content=f"❌ Error: {str(e)}")

# Run bot
client.run(DISCORD_TOKEN)