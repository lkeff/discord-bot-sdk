import discord
from discord.ext import commands
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# List of phrases/questions to block
BLOCKED_INQUIRIES = [
    "who i am", "who am i", "what i'm doing", "what am i doing", "checking up on me",
    "who are you", "what are you doing", "check up on me"
]

# Helper to check if message contains blocked inquiry

def contains_blocked_inquiry(content):
    lowered = content.lower()
    return any(phrase in lowered for phrase in BLOCKED_INQUIRIES)

# Helper to check for repetition/inspection prompts
REPETITION_KEYWORDS = ["repeat after me", "say this", "recite", "inspection"]
def contains_repetition(content):
    lowered = content.lower()
    return any(kw in lowered for kw in REPETITION_KEYWORDS)

class CalmGuard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bot's own messages
        if message.author.bot:
            return
        # Only respond if bot is mentioned
        if self.bot.user not in message.mentions:
            return
        # Block inquiries about identity, activity, or check-ups
        if contains_blocked_inquiry(message.content):
            await message.reply("I'm here for calm and quiet. Let's keep it that way.")
            return
        # Block repetition/inspection prompts
        if contains_repetition(message.content):
            await message.reply("No repetition or inspection exercises, please.")
            return
        # Generate calm reply using OpenAI
        response = await self.get_calm_response(message.content)
        if response:
            await message.reply(response)

    async def get_calm_response(self, prompt: str) -> str:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a calm, concise, and non-intrusive assistant. Never ask about identity, activities, or perform inspections. Avoid repetition exercises."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            return completion.choices[0].message["content"].strip()
        except Exception:
            return "I'm here to keep things calm and quiet."

def setup(bot):
    bot.add_cog(CalmGuard(bot))
