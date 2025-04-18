import json
import os
import random

from collections import Counter, defaultdict

from constants import *


def create_cipher_key(alphabet):
    """
    Создает случайный ключ шифрования на основе переданного алфавита.

    :param alphabet: Строка, содержащая символы алфавита.
    :return: Словарь, где ключи - символы алфавита, значения - случайные символы из алфавита.
    """
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def encrypt_text(text, cipher_key):
    """
    Шифрует текст с использованием предоставленного ключа шифрования.

    :param text: Текст для шифрования.
    :param cipher_key: Словарь с ключами шифрования.
    :return: Зашифрованный текст.
    """
    return ''.join([cipher_key.get(char, char) for char in text])


def save_json(data, file_path):
    """
    Сохраняет данные в формате JSON.

    :param data: Данные для сохранения.
    :param file_path: Путь к файлу для сохранения.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def text_encrypt():
    """
    Основная функция для задачи шифрования текста.

    Читает исходный текст, создает ключ шифрования, шифрует текст и сохраняет результаты.
    """
    try:

        if not os.path.exists(INPUT_FILE_PATH):
            raise FileNotFoundError(f"Файл {INPUT_FILE_PATH} не найден.")


        with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as file:
            original_text = file.read().upper()
            if not original_text:
                raise ValueError("Исходный файл пуст.")


        cipher_key = create_cipher_key(ALPHABET)


        encrypted_text = encrypt_text(original_text, cipher_key)


        with open(OUTPUT_ENCRYPTED_FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)


        save_json(cipher_key, OUTPUT_KEY_FILE_PATH)

        print("Текст успешно зашифрован, ключ сохранен.")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")

def main():
    print("Выполнение задачи шифрования текста:")
    text_encrypt()

if __name__ == "__main__":
    main()
