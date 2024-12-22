import requests
import mysql.connector
import time

# Telegram Bot API Token и ваш Chat ID
BOT_TOKEN = ""
CHAT_ID = ""  

# Подключение к базе данных MySQL
DB_HOST = 'localhost'
DB_NAME = 'feedbacks'
DB_USER = 'root'
DB_PASSWORD = ''

# Подключение к MySQL с обработкой ошибок
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def send_feedback_to_telegram(message, retries=3):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message
    }

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"Message sent successfully: {message}")
                return True
            else:
                print(f"Failed to send message: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message (attempt {attempt+1}): {e}")
        
        attempt += 1
        time.sleep(2)  
    return False

# Функция для обработки таблиц и отправки данных в Telegram
def process_table(table_name, select_query, update_query, message_format, entity_type):
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()

    if rows:
        print(f"Found {len(rows)} new entries in {table_name}.")
        for row in rows:
            message = message_format(row)
            if send_feedback_to_telegram(message):
                cursor.execute(update_query, (row[0],))
                conn.commit()
                print(f"Updated {table_name} entry ID {row[0]} to processed = 1")

    cursor.close()
    conn.close()

# Форматирование сообщений для каждой таблицы
def process_appointments():
    select_query = """
        SELECT id, user_id, name, phone_number, issue_description
        FROM appointments
        WHERE processed = 0
    """
    update_query = "UPDATE appointments SET processed = 1 WHERE id = %s"
    message_format = lambda row: f" Новый запрос на прием \n" \
                                 f"ID записи: {row[0]}\n" \
                                 f"Имя клиента: {row[2]}\n" \
                                 f"Телефон: {row[3]}\n" \
                                 f"Описание проблемы: {row[4]}\n" \
                                 f"Конец запроса "
    process_table("appointments", select_query, update_query, message_format, "Appointment")

# Форматирование сообщений для звонков
def process_calls():
    select_query = """
        SELECT id, user_id, name, phone_number, created_at
        FROM calls
        WHERE processed = 0
    """
    update_query = "UPDATE calls SET processed = 1 WHERE id = %s"
    message_format = lambda row: f"Новый запрос на звонок \n" \
                                 f"ID звонка: {row[0]}\n" \
                                 f"Имя клиента: {row[2]}\n" \
                                 f"Телефон: {row[3]}\n" \
                                 f"Дата и время отправки запроса: {row[4]}\n" \
                                 f"Конец запроса"
    process_table("calls", select_query, update_query, message_format, "Call")

# Форматирование сообщений для отзывов
def process_reviews():
    select_query = """
        SELECT id, user_id, rating, service_feedback, timestamp
        FROM reviews
        WHERE processed = 0
    """
    update_query = "UPDATE reviews SET processed = 1 WHERE id = %s"
    message_format = lambda row: f"Новый отзыв \n" \
                                 f"ID отзыва: {row[0]}\n" \
                                 f"Оценка: {row[2]}\n" \
                                 f"Отзыв о сервисе: {row[3]}\n" \
                                 f"Дата и время отзыва: {row[4]}\n" \
                                 f"Конец отзыва"
    process_table("reviews", select_query, update_query, message_format, "Review")

# Главная функция для регулярной проверки и обработки данных
def main():
    while True:
        process_appointments()
        process_calls()
        process_reviews()
        time.sleep(5)  # Задержка в 5 секунд между проверками

# Запуск программы
if __name__ == "__main__":
    main()
