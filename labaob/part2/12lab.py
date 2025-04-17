import json
from collections import Counter
from constants2 import *


def get_cipher(input_filename):
    """
    Предназначена для чтения текстового содержимого из файла по указанному пути
    :param input_filename: Путь к файлу
    :return: Возвращает строку
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_filename} не найден.")


def get_key(key_filename):
    """
    Предназначена для загрузки ключа расшифровки из JSON-файла
    :param key_filename: Путь к файлу с ключом
    :return: Возвращает словарь с ключом
    """
    try:
        with open(key_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {key_filename} не найден.")


def decrypt_text_with_key(encoded_string, key):
    """
    Предназначена для расшифровки текста с использованием готового ключа
    :param encoded_string: Зашифрованный текст
    :param key: Словарь с сопоставлением символов
    :return: Расшифрованный текст
    """
    return ''.join(key.get(ch, ch) for ch in encoded_string)


def text_data(text_data, output_filename):
    """
    Предназначена для сохранения текстовых данных в файл
    :param text_data: Строка, содержащая текстовые данные
    :param output_filename: Путь к файлу
    :return: None
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text_data)


def main():
    # Получаем зашифрованный текст из cod4.txt
    encrypted_data = get_cipher(INPUT_ENCODED_FILE)

    # Загружаем ключ из key.json
    key = get_key(KEY_FILE)

    if encrypted_data and key:
        # Расшифровываем текст с использованием ключа
        decoded_text = decrypt_text_with_key(encrypted_data, key)

        # Сохраняем расшифрованный текст в decrypted.txt
        text_data(decoded_text, OUTPUT_DECRYPTED_FILE)

        print("Расшифрованный текст готов =)")
    else:
        print("Не удалось выполнить расшифровку: отсутствуют необходимые данные")


if __name__ == "__main__":
    main()