import telebot
import requests
import json
from flask import Flask, request

# Telegram bot token
TOKEN = "7981716643:AAEVGVTrp0OYcpq2itXA5xitnmzQoCkJkFg"
bot = telebot.TeleBot(TOKEN)

# DeepSeek API URL
API_URL = "https://deepseek.privates-bots.workers.dev/?question="

app = Flask(__name__)

# Set up webhook route
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = json.loads(json_str)
    
    # Get the message sent by the user
    user_question = update.get("message", {}).get("text", "")
    
    if user_question:
        response = requests.get(API_URL + user_question)
        if response.status_code == 200:
            try:
                data = json.loads(response.text)  # Parse the JSON response
                answer = data.get("message", "Koi jawab nahi mila.")
            except json.JSONDecodeError:
                answer = "JSON response parse karne mein error aayi."
        else:
            answer = "API request failed. Please try again later."
        
        chat_id = update['message']['chat']['id']
        bot.send_message(chat_id, answer)
    return "OK", 200

# Set up Flask to forward the webhook to Telegram
@app.route(f"/setwebhook", methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://yourdomain.com/{TOKEN}"  # Replace with your domain
    bot.set_webhook(url=webhook_url)
    return "Webhook set successfully!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
