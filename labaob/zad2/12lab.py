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


def get_russian_frequencies(freq_filename):
    """
    Предназначена для загрузки данных о частоте использования русских букв
    :param freq_filename: Путь к файлу
    :return: Возвращает словарь
    """
    try:
        with open(freq_filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"Ошибка: Файл {freq_filename} не найден.")


def analyze_frequency(input_string):
    """
    Анализирует частоту появления каждого символа в переданном тексте
    :param input_string: Текст, который нужно проанализировать
    :return: Возвращает словарь
    """
    try:
        if not input_string:
            raise ValueError("Входная строка пуста.")
        char_count = Counter(input_string)
        total = sum(char_count.values())
        return {char: cnt / total for char, cnt in char_count.items()}
    except Exception as e:
        print(f"Ошибка при анализе частоты символов: {e}")


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

def json_data(data, output_filename):
     """
     предназначена для сохранения данных в формате JSON
     :param data: Данные, которые нужно сохранить
     :param output_filename: Путь к файлу
     :return: None
     """
     with open(output_filename, 'w', encoding='utf-8') as f:
         json.dump(data, f, ensure_ascii=False, indent=4)


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
    encrypted_data = get_cipher(INPUT_ENCODED_FILE)

    key = get_key(KEY_FILE)

    freq_analysis = analyze_frequency(encrypted_data)

    sorted_freq = dict(
        sorted(
            freq_analysis.items(),
            key=lambda item: (-item[1], item[0])
        )
    )
    json_data(sorted_freq, OUTPUT_FREQUENCIES_FILE)

    if encrypted_data and key:
        decoded_text = decrypt_text_with_key(encrypted_data, key)

        text_data(decoded_text, OUTPUT_DECRYPTED_FILE)

        print("Расшифрованный текст готов =)")
    else:
        print("Не удалось выполнить расшифровку: отсутствуют необходимые данные")


if __name__ == "__main__":
    main()
