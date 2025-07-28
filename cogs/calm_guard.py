import discord
from discord.ext import commands
import os
import openai
from dotenv import load_dotenv

# Securely load secrets from .env if present
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Ensure secrets are never hardcoded or printed

# List of phrases/questions to block
BLOCKED_INQUIRIES = [
    "who i am", "who am i", "what i'm doing", "what am i doing", "checking up on me",
    "who are you", "what are you doing", "check up on me"
]

# Helper to check if message contains blocked inquiry

def contains_blocked_inquiry(content):
    lowered = content.lower()
    # Block classified, operational, or inspection prompts
    classified_phrases = ["classified", "secret", "operation", "mission", "deployment", "orders"]
    return any(phrase in lowered for phrase in BLOCKED_INQUIRIES + classified_phrases)

# Helper to check for repetition/inspection prompts
REPETITION_KEYWORDS = ["repeat after me", "say this", "recite", "inspection"]
def contains_repetition(content):
    lowered = content.lower()
    # Block repetition, inspection, and drill/recite prompts
    repetition_extras = ["drill", "exercise", "repeat after me", "say exactly"]
    return any(kw in lowered for kw in REPETITION_KEYWORDS + repetition_extras)

class CalmGuard(commands.Cog):
    # List of allowed roles for bot interaction
    ALLOWED_ROLES = ["Admin", "Moderator"]  # Customize as needed
    
    def __init__(self, bot):
        self.bot = bot
        self.last_messages = {}  # For spam detection

    @staticmethod
    def contains_profanity(content):
        # Simple profanity check (expand as needed)
        profanities = ["fuck", "shit", "bitch", "asshole"]
        # Add more severe/obfuscated forms as needed
        lowered = content.lower()
        return any(word in lowered for word in profanities)

    @staticmethod
    def is_shouting(content):
        # Detect excessive all-caps (volume)
        letters = [c for c in content if c.isalpha()]
        return len(letters) > 4 and sum(1 for c in letters if c.isupper()) / len(letters) > 0.7

    def is_spam(self, author_id, content):
        # Basic spam: repeated messages or too many in short time
        from time import time
        now = time()
        if author_id not in self.last_messages:
            self.last_messages[author_id] = []
        # Keep only last 5 seconds
        self.last_messages[author_id] = [msg for msg in self.last_messages[author_id] if now - msg[1] < 5]
        # Add current message
        self.last_messages[author_id].append((content, now))
        # Check for repeated content or >3 messages in 5 seconds
        if len(self.last_messages[author_id]) > 3:
            return True
        contents = [msg[0] for msg in self.last_messages[author_id]]
        if contents.count(content) > 1:
            return True
        return False

    def user_has_permission(self, member: discord.Member):
        # Only allow users with permitted roles
        return any(role.name in self.ALLOWED_ROLES for role in member.roles)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        import logging
        from utils.redact import redact_sensitive
        logging.basicConfig(level=logging.INFO)
        # Always redact sensitive info in logs
        def safe_log(msg):
            logging.info(redact_sensitive(msg))
        # Uncomment to enable logging of redacted message content
        # safe_log(message.content)

        if message.author.bot:
            return
        if self.bot.user not in message.mentions:
            return
        # Role-based permission check
        if isinstance(message.author, discord.Member) and not self.user_has_permission(message.author):
            await message.reply("Sorry, you don't have permission to interact with me.")
            return
        # Profanity filter
        if self.contains_profanity(message.content):
            await message.reply("Let's keep it civil.")
            return
        # Volume (shouting) filter
        if self.is_shouting(message.content):
            await message.reply("No need to shout, let's stay calm.")
            return
        # Spam check
        if self.is_spam(message.author.id, message.content):
            await message.reply("Please avoid spamming.")
            return
        if contains_blocked_inquiry(message.content):
            await message.reply("I'm here for calm and quiet. Let's keep it that way.")
            return
        if contains_repetition(message.content):
            await message.reply("No repetition or inspection exercises, please.")
            return
        # --- Mood, language, and tense/context analysis ---
        from utils.mood_analysis import detect_language, detect_mood, tense_analysis, full_mood_callback
        # Gather context: last 3 user messages (if available)
        user_id = message.author.id
        if not hasattr(self, 'user_histories'):
            self.user_histories = {}
        if user_id not in self.user_histories:
            self.user_histories[user_id] = []
        self.user_histories[user_id].append(message.content)
        if len(self.user_histories[user_id]) > 3:
            self.user_histories[user_id] = self.user_histories[user_id][-3:]
        past_contexts = '\n'.join(self.user_histories[user_id][:-1]) if len(self.user_histories[user_id]) > 1 else None

        # Get full mood/language/tense callback from OpenAI
        analysis = full_mood_callback(message.content, past_contexts)
        response = await self.get_calm_response(f"{message.content}\n\nAnalysis: {analysis}")
        if response:
            await message.reply(f"{response}\n\n(Analysis: {analysis})")

    # Deployment: After testing, deploy this bot to a secure VPS or cloud instance.

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
