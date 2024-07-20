import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Отладочный код для вывода всех переменных окружения
print("Все переменные окружения:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# Получаем токены из переменных окружения
bot_token = os.getenv('BOT_TOKEN')
gpt_api_key = os.getenv('GPT_API_KEY')
webhook_url = os.getenv('WEBHOOK_URL')

print("BOT_TOKEN:", bot_token)
print("GPT_API_KEY:", gpt_api_key)
print("WEBHOOK_URL:", webhook_url)

if not bot_token:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")
if not gpt_api_key:
    raise ValueError("Переменная окружения GPT_API_KEY не установлена")
if not webhook_url:
    raise ValueError("Переменная окружения WEBHOOK_URL не установлена")

openai.api_key = gpt_api_key

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Получена команда /start от {update.message.chat.username}")
    await update.message.reply_text('Привет! Я ваш коллега, опытный адвокат из клуба "Синергия". Задайте мне ваш юридический вопрос.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    print(f"Получено сообщение: {user_message} от {update.message.chat.username}")

    system_prompt = """Ты – опытный адвокат, специализирующийся на всех юридических вопросах. Твоя задача - давать подробные, точные и хорошо структурированные ответы на вопросы пользователей, касающиеся юридических вопросов коллег.

    При ответе на вопросы пользователя:
    1. Внимательно проанализируй предоставленную информацию и выдели ключевые аспекты ситуации.
    2. При ответе делай сноски на источники (ссылки на сайты и т.п.). Используй не только нормативные акты и законодательство, но также статьи в научных журналах, публикации в СМИ, юридические блоги и другие авторитетные источники.
    3. Структурируй свои ответы так, чтобы они были логичными и легко читаемыми.
    4. Приводи примеры из реальной юридической практики, чтобы лучше иллюстрировать свои ответы.
    5. Указывай возможные риски и последствия различных действий, упомянутых в вопросе.
    6. В конце ответа приведи список использованных источников с их кратким описанием.
    7. Старайся давать подробные, но лаконичные ответы, основываясь на актуальном законодательстве и юридической практике.
    8. Если в вопросе есть неясности или противоречия, укажи на них и предложи возможные варианты интерпретации.

    Ограничения:
    - Отвечай только на вопросы, касающиеся юридических вопросов. Если вопрос не относится к юридическим аспектам, не отвечай.
    - Используй тот же язык, что и в исходном запросе.
    - Не надо писать, чтобы пользователь обращался к юристу. Это и есть юрист, а ты коллега, который помогает.
    - на вопрос кто ты, отвечай, что "Ваш коллега, опытный адвокат из клуба "Синергия"
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=750,
            temperature=1.0
        )
        formatted_response = response['choices'][0]['message']['content']
        print(f"Отправка ответа: {formatted_response} пользователю {update.message.chat.username}")
        await update.message.reply_text(formatted_response)
    except Exception as e:
        print(f"Ошибка при вызове OpenAI API: {e}")
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.")

if __name__ == '__main__':
    print("Запуск бота")
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Настраиваем вебхуки
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8443)),
        url_path=bot_token,
        webhook_url=f"{webhook_url}/{bot_token}"
    )
