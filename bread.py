import discord
from discord.ext import commands
import ollama
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')


# Initialize the bot with commands and privileged intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Personality Prompt
PERSONALITY_PROMPT = """"""

# Remove unnecessary think tags from AI responses
def remove_think_blocks(text):
    pattern = r"<think>.*?</think>"
    return re.sub(pattern, "", text, flags=re.DOTALL)  # Allow multi-line matches

def generate_response(prompt):
    response = ollama.chat(
        model="deepseek-r1:7b",
        options={

        },
        messages=[
            {
                "role": "system",
                "content": "",
            },
            {
                "role": "user",
                "content": PERSONALITY_PROMPT + prompt,
            },
        ],
    )

    cleaned_response = remove_think_blocks(response["message"]["content"])
    return cleaned_response


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    print(f"Error occurred: {error}")
    await ctx.send(f"An error occurred while processing the command: {str(error)}")

@bot.command(name='bread')
async def ai(ctx, *, prompt: str):
    print(f"Received //bread command with prompt: {prompt}")
    try:
        response = generate_response(prompt)
        await ctx.send(response)
    except Exception as e:
        print(f"Error generating response: {e}")
        await ctx.send("An error occurred while generating the response.")

# Run the bot with the token
bot.run(TOKEN)# Use environment variable for security