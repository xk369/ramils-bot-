import logging
#1294774551
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters, CallbackContext,
)

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '7468007082:AAEiuW7ZjOpULUKdEDQw6Z4n4Im9GwQARP4'

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Задать вопрос", callback_data='question')],
        [InlineKeyboardButton("Предложить сотрудничество", callback_data='collaboration')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)



async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")


# Обработка нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)  # Убираем клавиатуру после выбора

    if query.data == 'question':
        await query.edit_message_text("Задайте свой вопрос:")
        context.user_data['type'] = 'question'
    elif query.data == 'collaboration':
        await query.edit_message_text("Опишите ваше предложение о сотрудничестве:")
        context.user_data['type'] = 'collaboration'

# Обработка текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_data = context.user_data

    try:
        # Проверяем тип сообщения, заданный через кнопки
        message_type = user_data['type']
        username = message.from_user.username
        if username is None:
            username = "Анонимный пользователь"

        # Формируем текст для отправки
        text = f"({message_type.capitalize()}) \"{username}\"\n\n{message.text}"

        # Отправляем сообщение владельцу бота (замените 'YOUR_CHAT_ID' на ваш ID чата)
        await context.bot.send_message(chat_id='1294774551', text=text)
        await message.reply_text("Сообщение отправлено!")

        # После успешной отправки отображаем клавиатуру снова
        keyboard = [
            [InlineKeyboardButton("Задать вопрос", callback_data='question')],
            [InlineKeyboardButton("Предложить сотрудничество", callback_data='collaboration')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Выберите следующее действие:", reply_markup=reply_markup)

        # Очищаем пользовательские данные
        del user_data['type']

    except KeyError:
        # Если пользователь пропустил выбор действия
        await message.reply_text("Пожалуйста, выберите действие с помощью кнопок.")
    except Exception as e:
        # Обработка общих ошибок
        logging.error(f"Ошибка при обработке сообщения: {e}")
        await message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

# Основная функция
def main() -> None:
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("get_chat_id", get_chat_id))

    # Запускаем приложение
    application.run_polling()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

if __name__ == '__main__':
    main()
