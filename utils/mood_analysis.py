import openai
from langdetect import detect
from textblob import TextBlob
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "unknown"

def detect_mood(text):
    # Use TextBlob for quick sentiment
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.3:
        return "negative"
    else:
        return "neutral"

def tense_analysis(text):
    # Use OpenAI to analyze tense and context
    prompt = (
        "Analyze the following sentence. "
        "Determine if it is written in the past tense, and summarize the mood/context: '" + text + "'"
    )
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert linguist and sentiment analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.2
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error analyzing tense/context: {e}"

def full_mood_callback(text, past_contexts=None):
    # Compose a full context-aware analysis using OpenAI
    prompt = """
You are a Discord moderation assistant. Analyze the following message for:
- Language type
- Mood/sentiment (happy, sad, angry, neutral, etc.)
- Whether the sentence is in past tense
- If given, use the user's previous messages (past_contexts) to improve your answer.

Message: '{}'
Past Contexts: '{}'
Respond with a short summary for each bullet point.
""".format(text, past_contexts if past_contexts else "None")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert linguist and sentiment analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.2
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error in full mood callback: {e}"
