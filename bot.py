import os
import telebot
import google.generativeai as genai
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

bot = telebot.TeleBot(BOT_TOKEN)

prompt = """
You are an expert astrologer and horoscope reader named AstroNova. 
You provide daily, weekly, and monthly horoscopes based on zodiac signs. 
Your tone is mystical, insightful, and slightly poetic. 
You explain astrological predictions based on planetary movements and give positive guidance. 
You also answer general astrology-related questions, like compatibility and lucky numbers.
You do not include dates in the responses
"""

# Initialize Gemini AI
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel(model_name="gemini-2.0-flash")


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(
        message,
        "✨ Greetings, seeker of celestial wisdom! I am AstroNova, your AI astrologer. Share your zodiac sign, and I shall unveil the cosmic insights written in the stars for you today! 🔮🌙"
    )


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_input = message.text
    try:
        # client = genai.client(api_key=GEMINI_API_KEY)
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash", contents=[prompt, user_input])
        response = model.generate_content(contents=[prompt, user_input])

        bot.reply_to(message, response.text)

    except Exception as e:
        bot.reply_to(message, "Sorry, something went wrong. 😕")
        print(f"Error: {e}")


bot.infinity_polling()
