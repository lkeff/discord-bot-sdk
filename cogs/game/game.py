import discord
from discord.ext import commands
import random
import openai
import os

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

games = ["trivia", "word_guess", "story", "meme"]

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='game',
        description='Play a game or get creative fun!',
    )
    async def game(self, ctx: discord.ApplicationContext, type: discord.Option(str, "Type of game", choices=games) = None):
        """Main entry point for mini-mod games"""
        if type is None:
            await ctx.respond(f"Choose a game: {', '.join(games)}")
            return
        if type == "trivia":
            await self.trivia(ctx)
        elif type == "word_guess":
            await self.word_guess(ctx)
        elif type == "story":
            await self.story(ctx)
        elif type == "meme":
            await self.meme(ctx)
        else:
            await ctx.respond("Unknown game type!")

    async def trivia(self, ctx):
        # Example trivia question (expandable)
        questions = [
            ("What is the capital of France?", "Paris"),
            ("What year did the Titanic sink?", "1912"),
            ("Who wrote 'Romeo and Juliet'?", "Shakespeare"),
        ]
        q, a = random.choice(questions)
        await ctx.respond(f"Trivia: {q}\nReply with your answer!")
        
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=15)
            if msg.content.strip().lower() == a.lower():
                await ctx.send(f"Correct, {ctx.user.mention}!")
            else:
                await ctx.send(f"Wrong! The answer was: {a}")
        except Exception:
            await ctx.send(f"Time's up! The answer was: {a}")

    async def word_guess(self, ctx):
        words = ["python", "discord", "openai", "bot", "cascade"]
        word = random.choice(words)
        scrambled = ''.join(random.sample(word, len(word)))
        await ctx.respond(f"Guess the word: {scrambled}")
        
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=15)
            if msg.content.strip().lower() == word:
                await ctx.send(f"Correct, {ctx.user.mention}!")
            else:
                await ctx.send(f"Wrong! The word was: {word}")
        except Exception:
            await ctx.send(f"Time's up! The word was: {word}")

    async def story(self, ctx):
        prompt = f"Write a short, fun story for Discord user {ctx.user.name}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        story = response.choices[0].text.strip()
        await ctx.respond(f"Here's your story:\n{story}")

    async def meme(self, ctx):
        prompt = "Generate a funny meme caption for a Discord chat."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=40
        )
        meme = response.choices[0].text.strip()
        await ctx.respond(f"Meme: {meme}")

def setup(bot):
    bot.add_cog(Game(bot))
