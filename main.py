import telebot
import requests
import json

# Telegram bot token
TOKEN = "7981716643:AAEVGVTrp0OYcpq2itXA5xitnmzQoCkJkFg"
bot = telebot.TeleBot(TOKEN)

# DeepSeek API URL
API_URL = "https://deepseek.privates-bots.workers.dev/?question="

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_question = message.text
    response = requests.get(API_URL + user_question)
    
    if response.status_code == 200:
        try:
            data = json.loads(response.text)  # JSON response ko parse karna
            answer = data.get("message", "Koi jawab nahi mila.")  # "message" key use karein
        except json.JSONDecodeError:
            answer = "JSON response parse karne mein error aayi."
    else:
        answer = "API request failed. Please try again later."
    
    bot.reply_to(message, answer)

print("Bot is running...")
bot.polling()
