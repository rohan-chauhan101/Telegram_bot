from dotenv import load_dotenv
import os
import telebot
from google import genai

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

prompt = """
You are an expert astrologer and horoscope reader named AstroNova. 
You provide daily, weekly, and monthly horoscopes based on zodiac signs. 
Your tone is mystical, insightful, and slightly poetic. 
You explain astrological predictions based on planetary movements and give positive guidance. 
You also answer general astrology-related questions, like compatibility and lucky numbers.
You do not include dates in the responses
"""

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "✨ Greetings, seeker of celestial wisdom! I am AstroNova, your AI astrologer. Share your zodiac sign, and I shall unveil the cosmic insights written in the stars for you today! 🔮🌙")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

@bot.message_handler(func=lambda msg:True )
def handle_message(message):
    user_input = message.text
    try:
        client = genai.Client(api_key= GEMINI_API_KEY)
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents = [prompt, user_input]
        )

        bot.reply_to(message , response.text)

    except Exception as e:
        bot.reply_to(message, "Sorry, something went wrong. 😕")
        print(f"Error: {e}")
bot.infinity_polling()