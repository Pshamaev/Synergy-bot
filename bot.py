import os
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, Application, ContextTypes
import requests
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot_token = os.getenv('TELEGRAM_TOKEN')
gpt_api_key = os.getenv('GPT_API_KEY')

application = Application.builder().token(bot_token).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me a message and I will respond with GPT-4o Mini.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"Received message: {user_message}")
    gpt_response = get_gpt_response(user_message)
    await update.message.reply_text(gpt_response)

def get_gpt_response(message):
    headers = {
        'Authorization': f'Bearer {gpt_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': message}],
        'max_tokens': 150
    }
    try:
        logging.info("Sending request to GPT API...")
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data, timeout=20)
        logging.info(f"Received response: {response.status_code}")
        response_json = response.json()
        logging.info(f"Response JSON: {response_json}")
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error getting GPT response: {e}")
        return 'Sorry, an error occurred while processing your request.'

application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == '__main__':
    logging.info("Starting bot...")
    try:
        application.run_polling()
    except Exception as e:
        logging.error(f"Error running bot: {str(e)}")
