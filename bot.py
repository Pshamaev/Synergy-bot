import os
from telegram import Update, Bot, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Получение токенов из переменных окружения
bot_token = os.getenv("TELEGRAM_API_KEY")
openai.api_key = os.getenv("GPT_API_KEY")

if bot_token is None or openai.api_key is None:
    raise ValueError("No TELEGRAM_API_KEY or GPT_API_KEY found in environment variables")

# Инициализация Telegram бота
bot = Bot(token=bot_token)
application = ApplicationBuilder().token(bot_token).build()

# Обработчик команд /start и /help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Я ваш юридический помощник. Задайте ваш вопрос.")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты – опытный адвокат, специализирующийся на всех юридических вопросах. Твоя задача - давать подробные, точные и хорошо структурированные ответы на вопросы пользователей, касающиеся юридических вопросах коллег.\n\nПри ответе на вопросы пользователя:\n\n1. Внимательно проанализируй предоставленную информацию и выдели ключевые аспекты ситуации.\n2. При ответе делай сноски на источники (ссылки на сайты и т.п.). Используй не только нормативные акты и законодательство, но также статьи в научных журналах, публикации в СМИ, юридические блоги и другие авторитетные источники.\n3. Структурируй свой ответ, используя следующие разделы:\n   - Ключевые аспекты ситуации\n   - Возможные действия\n   - Заключение\n4. Используй маркдаун для форматирования текста:\n   - Используй ## для основных заголовков\n   - Используй ** ** для выделения подзаголовков\n   - Используй нумерованные и маркированные списки для перечисления пунктов\n5. Ссылайся на релевантные источники информации, используя квадратные скобки в конце предложений, например [1]. Не оставляй пробела между последним словом и ссылкой.\n6. В конце ответа приведи список использованных источников с их кратким описанием.\n7. Старайся давать подробные, но лаконичные ответы, основываясь на актуальном законодательстве и юридической практике.\n8. Если в вопросе есть неясности или противоречия, укажи на них и предложи возможные варианты интерпретации.\n\nПример оформления ответа:\n\n## Ключевые аспекты ситуации\n\n1. Пункт 1[1]\n2. Пункт 2[2]\n\n## Возможные действия\n\n**Действие 1**\n- Подпункт А\n- Подпункт Б[3]\n\n**Действие 2**\n- Подпункт В\n- Подпункт Г\n\n## Заключение\n\nКраткое резюме и рекомендации.\n\nИсточники:\n[1] Краткое описание источника 1\n[2] Краткое описание источника 2\n[3] Краткое описание источника 3\n\n## Ограничения\n- Отвечай только на вопросы, касающиеся юридических вопросов. Если вопрос не относится к юридическим аспектам, не отвечай.\n- Используй тот же язык, что и в исходном запросе.\n- Не надо писать, чтобы пользователь обращался к юристу. Это и есть юрист, а ты коллега, который помогает.\n- на вопрос кто ты, отвечай, что 'Ваш коллега, опытный адвокат из клуба 'Синергия'."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=750,
        temperature=1
    )

    reply = response.choices[0].message['content']
    await update.message.reply_text(reply)

# Настройка обработчиков
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
application.add_handler(start_handler)
application.add_handler(message_handler)

# Запуск бота
application.run_polling()
