import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Получаем токены из переменных окружения
bot_token = os.getenv('BOT_TOKEN')
if not bot_token:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")
print(f"Bot Token: {bot_token}")

gpt_api_key = os.getenv('GPT_API_KEY')
if not gpt_api_key:
    raise ValueError("Переменная окружения GPT_API_KEY не установлена")
print(f"GPT API Key: {gpt_api_key}")

openai.api_key = gpt_api_key

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш юридический ассистент. Задайте мне ваш вопрос.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты – опытный адвокат, специализирующийся на всех юридических вопросах. Твоя задача - давать подробные, точные и хорошо структурированные ответы на вопросы пользователей, касающиеся юридических вопросах коллег."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=750,
        temperature=1.0
    )

    # Форматируем ссылки как гиперссылки
    formatted_response = response.choices[0].message['content'].replace('[', '[').replace(']', ']')

    # Отправляем ответ пользователю
    await update.message.reply_text(formatted_response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()
