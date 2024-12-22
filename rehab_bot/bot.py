from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.contrib.middlewares.fsm import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import logging
import os
import mysql.connector
from mysql.connector import Error

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен Telegram-бота
BOT_TOKEN = "8013691624:AAG0iXy9Ysd4K0ii_-ADwt33D0PVZsYypF4"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Подключение к базе данных MySQL 
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="feedbacks"
        )
        return connection
    except Error as e:
        logging.error(f"Ошибка подключения к базе данных: {e}")
        return None

# Состояния для формы заказа звонка
class CallbackRequest(StatesGroup):
    name = State()  
    phone_number = State()  

# Состояния для формы обратной связи
class FeedbackForm(StatesGroup):
    rating = State()  
    feedback_text = State()  

# Главная клавиатура
@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    welcome_text = "Главное меню."
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    buttons = [
        ["🏥 Клиники", "ℹ️ О нас"],
        ["👨‍⚕️ Наши специалисты"],
        ["📝 Записаться на прием"],
        ["📍 Адреса", "📩 Обратная связь"]
    ]
    
    for row in buttons:
        keyboard.add(*row)
    
    await message.answer(welcome_text, reply_markup=keyboard)

# Обработчики для кнопок
@dp.message_handler(text="🏥 Клиники")
async def clinics_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [["GLORY DETOX", "FREEDOM DETOX"], ["Назад"]]
    
    for row in buttons:
        keyboard.add(*row)
    
    photo_path = "images/our.png"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Выберите клинику для получения информации:", reply_markup=keyboard)
    else:
        await message.answer("Извините, изображение не найдено. Выберите клинику:", reply_markup=keyboard)

@dp.message_handler(text="GLORY DETOX")
async def glory_detox_info(message: types.Message):
    info_text = (
        "<b>🏥 GLORY DETOX</b>\n\n"
        "<b>Адрес:</b> Узбекистан, город Ташкент, район Мирзо-Улугбека, улица Феруза, 32\n\n"
        "<b>Контактный телефон:</b> +998992002008"
    )
    photo_path = "images/our.png"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=info_text,
                parse_mode="HTML"  # Указываем режим HTML для форматирования
            )
    else:
        await message.answer(info_text, parse_mode="HTML")  # Указываем режим HTML

@dp.message_handler(text="FREEDOM DETOX")
async def freedom_detox_info(message: types.Message):
    info_text = (
        "<b>🏥 FREEDOM DETOX</b>\n\n"
        "<b>Адрес:</b> Узбекистан, город Ташкент, район Олмазор, Аллон МФЙ, улица Фаробий, дом 320-А.\n\n"
        "<b>Контактный телефон:</b> +998777272277"
    )
    photo_path = "images/our.png"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=info_text,
                parse_mode="HTML"  # Указываем режим HTML
            )
    else:
        await message.answer(info_text, parse_mode="HTML")  # Указываем режим HTML

# Обработчик для кнопки "Назад"
@dp.message_handler(text="Назад")
async def back_to_main_menu(message: types.Message):
    await main_menu(message)
# Обработчик для кнопки "👨‍⚕️ Наши специалисты"
@dp.message_handler(text="👨‍⚕️ Наши специалисты")
async def specialists_menu(message: types.Message):
    info_text = "<b>Выберите специалиста, чтобы познакомиться с ним поближе.</b>"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        ["Каграманян Карлен Суренович"],
        ["Хан Елена Николаевна"],
        ["Нурматова Фатима Пулатовна"],
        ["Назад"]
    ]
    
    for row in buttons:
        keyboard.add(*row)
    
    photo_path = "images/specialists.png"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

# Обработчик для кнопки "Каграманян Карлен Суренович"
@dp.message_handler(text="Каграманян Карлен Суренович")
async def psychologist_1_info(message: types.Message):
    info_text = (
        "<b>Каграманян Карлен Суренович</b> — Руководитель с богатым опытом в сфере психотерапии и медицины.\n\n"
        "Он поможет вам разобраться в ваших чувствах и выбрать эффективные пути восстановления.\n\n"
        "<i>Чтобы записаться на консультацию, напишите нам, и мы договоримся о времени.</i>"
    )
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Записаться на прием", url="tg://resolve?domain=maryfound")
    keyboard.add(button)
    
    photo_path = "images/karlen.jpg"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

# Обработчик для кнопки "Хан Елена Николаевна"
@dp.message_handler(text="Хан Елена Николаевна")
async def psychologist_2_info(message: types.Message):
    info_text = (
        "<b>Хан Елена Николаевна</b> — Психиатр-нарколог с опытом работы более 30 лет.\n\n"
        "Она предоставляет помощь людям с зависимостями и психологическими проблемами.\n\n"
        "<i>Чтобы записаться на консультацию, напишите нам.</i>"
    )
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Записаться на прием", url="tg://resolve?domain=maryfound")
    keyboard.add(button)
    
    photo_path = "images/elena.jpg"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

# Обработчик для кнопки "Нурматова Фатима Пулатовна"
@dp.message_handler(text="Нурматова Фатима Пулатовна")
async def psychologist_3_info(message: types.Message):
    info_text = (
        "<b>Нурматова Фатима Пулатовна</b> — Старшая мед. сестра с опытом работы более 19 лет.\n\n"
        "Она специализируется на восстановлении здоровья и поддержке пациентов на разных этапах лечения.\n\n"
        "<i>Запишитесь на консультацию для получения помощи.</i>"
    )
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Записаться на прием", url="tg://resolve?domain=maryfound")
    keyboard.add(button)
    
    photo_path = "images/fatima.jpg"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

# Обработчик для кнопки "📍 Адреса"
@dp.message_handler(text="📍 Адреса")
async def locations(message: types.Message):
    info_text = (
        "<b>Наши клиники расположены по следующим адресам:</b>\n\n"
        "1. <b>GLORY DETOX</b> — Узбекистан, город Ташкент, район Мирзо-Улугбека, улица Феруза, 32\n\n"
        "2. <b>FREEDOM DETOX</b> — Узбекистан, город Ташкент, район Олмазор, Аллон МФЙ, улица Фаробий, дом 320-А."
    )
    photo_path = "images/address.png"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML"
        )

@dp.message_handler(text="ℹ️ О нас")
async def about_us(message: types.Message):
    info_text = (
        "<b>Мы — команда профессионалов, работающих в сфере психотерапии и наркологии.</b>\n\n"
        "<b>Мы предлагаем:</b>\n"
        "🔹 <i>Анонимное лечение</i>\n"
        "🔹 <i>Помощь при зависимостях</i>\n"
        "🔹 <i>Психологические консультации</i>\n\n"
        "<b>Наши клиники работают с высококвалифицированными специалистами,</b> "
        "которые помогут вам на пути к восстановлению.\n\n"
        "<b>Наш сайт:</b> <a href='https://narkologicheskaya-klinika.uz/'>narkologicheskaya-klinika.uz</a>"
    )
    photo_path = "images/aboutus.png"
    with open(photo_path, "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=info_text,
            parse_mode="HTML"  # Указываем режим HTML для форматирования
        )

# Обработчик для кнопки "📩 Обратная связь"
@dp.message_handler(text="📩 Обратная связь")
async def feedback_menu(message: types.Message):
    info_text = "Уточните, пожалуйста, какой у Вас запрос, выбрав подходящую кнопку:"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [["🖊️ Оставить отзыв", "Заказать звонок"], ["Назад"]]
    
    for row in buttons:
        keyboard.add(*row)
    
    await message.answer(info_text, reply_markup=keyboard)
# Обработчик для кнопки "🖊️ Оставить отзыв"
@dp.message_handler(text="🖊️ Оставить отзыв")
async def leave_feedback(message: types.Message):
    info_text = (
        "<b>Отзывы наших клиентов</b> - самое ценное, что у нас есть, "
        "ведь они напрямую отражают результат, полученный на сеансе или программе.\n\n"
        "<b>Оцените по 5-бальной шкале Ваш визит:</b>"
    )
    
    # Inline keyboard for rating buttons (1 to 5)
    inline_keyboard = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        button = InlineKeyboardButton(text=str(i), callback_data=f"feedback_{i}")
        inline_keyboard.add(button)

    # Regular keyboard for the "Cancel" button
    cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = KeyboardButton("❌ Отменить")
    cancel_keyboard.add(cancel_button)

    # Send message with rating buttons and cancel button
    await message.answer(info_text, reply_markup=inline_keyboard, parse_mode="HTML")
    await message.answer("Выберите оценку и, если нужно, отмените процесс.", reply_markup=cancel_keyboard)

    await FeedbackForm.rating.set()  # Устанавливаем состояние для рейтинга

# Глобальный обработчик кнопки "Отменить"
@dp.message_handler(lambda message: message.text == "❌ Отменить", state="*")
async def cancel_feedback(message: types.Message, state: FSMContext):
    """
    Handle the 'Cancel' button globally and return to the main menu.
    """
    await state.finish()  # Clear any active state
    await message.answer("Процесс отменен. Возвращаю в главное меню.", reply_markup=types.ReplyKeyboardRemove())
    await main_menu(message)

# Обработчик выбора оценки
@dp.callback_query_handler(lambda query: query.data.startswith("feedback_"), state=FeedbackForm.rating)
async def feedback_score_callback(query: types.CallbackQuery, state: FSMContext):
    score = int(query.data.split("_")[1])
    await state.update_data(rating=score)
    await bot.send_message(chat_id=query.message.chat.id, text="<b>Спасибо за отзыв, теперь пожалуйста, оставьте свой отзыв</b> по тому, как прошел визит.", parse_mode="HTML")
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=None)
    await FeedbackForm.feedback_text.set()  # Переходим к следующему состоянию

# Обработчик текста отзыва
@dp.message_handler(state=FeedbackForm.feedback_text)
async def service_feedback(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    service_feedback = message.text.strip()
    
    # Получаем рейтинг из состояния
    state_data = await state.get_data()
    rating = state_data.get("rating")
    
    if not service_feedback:
        await message.answer("Вы не оставили отзыв. Ваш отзыв не был сохранен.")
        await state.finish()  # Завершаем процесс
    else:
        # Сохраняем данные в базу данных
        connection = get_db_connection()
        if connection:
            try:
                db_cursor = connection.cursor()
                query = "INSERT INTO reviews (user_id, rating, service_feedback) VALUES (%s, %s, %s)"
                values = (user_id, rating, service_feedback)
                db_cursor.execute(query, values)
                connection.commit()
                await message.answer("Спасибо за ваш отзыв!")
            except Error as e:
                logging.error(f"Ошибка при сохранении отзыва: {e}")
                await message.answer("Произошла ошибка при сохранении отзыва. Пожалуйста, попробуйте снова позже.")
            finally:
                connection.close()
        else:
            await message.answer("Не удалось подключиться к базе данных. Пожалуйста, попробуйте позже.")
        
        await state.finish()  # Завершаем процесс
    await main_menu(message)

# Обработчик кнопки "Назад"
@dp.message_handler(text="Назад")
async def back_to_main_menu(message: types.Message):
    await main_menu(message)

# Состояния для формы заказа звонка
class CallRequest(StatesGroup):
    name = State()  # Состояние для имени
    phone_number = State()  # Состояние для номера телефона

# Обработчик для кнопки "Заказать звонок"
@dp.message_handler(text="Заказать звонок")
async def request_call(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = KeyboardButton("❌ Отменить")
    keyboard.add(cancel_button)

    await message.answer("Как к вам обращаться?", reply_markup=keyboard)
    await CallRequest.name.set()  # Переходим к состоянию имени
# Обработчик для имени
@dp.message_handler(state=CallRequest.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if name.lower() == "❌ отменить":
        await state.finish()  # Завершаем процесс
        await message.answer("Процесс отменен. Возвращаю в главное меню.", reply_markup=types.ReplyKeyboardRemove())
        await main_menu(message)
    else:
        await state.update_data(name=name)
        phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        phone_button = KeyboardButton("📞 Отправить номер телефона", request_contact=True)
        cancel_button = KeyboardButton("❌ Отменить")
        phone_keyboard.add(phone_button) 
        phone_keyboard.add(cancel_button)  

        await message.answer("Пожалуйста, отправьте ваш номер телефона:", reply_markup=phone_keyboard)
        await CallRequest.phone_number.set()  

# Обработчик для номера телефона (если пользователь отправляет номер через кнопку)
@dp.message_handler(content_types=types.ContentType.CONTACT, state=CallRequest.phone_number)
async def process_phone_number_from_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_data = await state.get_data()
    name = user_data.get("name")
    
    connection = get_db_connection()
    if connection:
        try:
            db_cursor = connection.cursor()
            query = "INSERT INTO calls (user_id, name, phone_number) VALUES (%s, %s, %s)"
            values = (message.chat.id, name, phone_number)
            db_cursor.execute(query, values)
            connection.commit()
            await message.answer(f"Спасибо, {name}! Ваш запрос на звонок принят. Мы свяжемся с вами скоро.")
        except Error as e:
            logging.error(f"Ошибка при сохранении данных: {e}")
            await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова позже.")
        finally:
            connection.close()

    await state.finish()  
    await main_menu(message)

# Обработчик для ввода номера телефона вручную
@dp.message_handler(state=CallRequest.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text.strip()
    if phone_number.lower() == "❌ отменить":
        await state.finish()  # Завершаем процесс
        await message.answer("Процесс отменен. Возвращаю в главное меню.", reply_markup=types.ReplyKeyboardRemove())
        await main_menu(message)
    else:
        # Получаем имя из состояния
        user_data = await state.get_data()
        name = user_data.get("name")
        
        # Сохраняем данные в базу данных
        connection = get_db_connection()
        if connection:
            try:
                db_cursor = connection.cursor()
                query = "INSERT INTO calls (user_id, name, phone_number) VALUES (%s, %s, %s)"
                values = (message.chat.id, name, phone_number)
                db_cursor.execute(query, values)
                connection.commit()
                await message.answer(f"Спасибо, {name}! Ваш запрос на звонок принят. Мы свяжемся с вами скоро.")
            except Error as e:
                logging.error(f"Ошибка при сохранении данных: {e}")
                await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова позже.")
            finally:
                connection.close()

        await state.finish()  
        await main_menu(message)



# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)