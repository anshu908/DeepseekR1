import telebot
import requests
import json
from flask import Flask, request

# Telegram bot token
TOKEN = "7981716643:AAEVGVTrp0OYcpq2itXA5xitnmzQoCkJkFg"
bot = telebot.TeleBot(TOKEN)

# DeepSeek API URL
API_URL = "https://deepseek.privates-bots.workers.dev/?question="

# Flask app
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = json.loads(json_str)
    chat_id = update['message']['chat']['id']
    user_question = update['message']['text']

    response = requests.get(API_URL + user_question)
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            answer = data.get("message", "Koi jawab nahi mila.")
        except json.JSONDecodeError:
            answer = "JSON response parse karne mein error aayi."
    else:
        answer = "API request failed. Please try again later."
    
    bot.send_message(chat_id, answer)
    return 'OK', 200

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    # Fixed the URL string, removed the newline at the end
    webhook_url = f"https://fixed-rebekkah-pyare-a6dce348.koyeb.app/7981716643:AAEVGVTrp0OYcpq2itXA5xitnmzQoCkJkFg"
    bot.set_webhook(url=webhook_url)
    return "Webhook is set!", 200

if __name__ == "__main__":
    app.run(port=5000)
