import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные окружения из .env

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def push_code():
    if not GITHUB_TOKEN:
        raise Exception("Нет токена GitHub в переменных окружения")
    # логика пуша с использованием GITHUB_TOKEN
    print("Токен загружен успешно, можно пушить.")

if __name__ == "__main__":
    push_code()