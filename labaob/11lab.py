import json
import os
import random
from collections import Counter, defaultdict

from constants import (
    ALPHABET,
    INPUT_FILE_PATH,
    OUTPUT_ENCRYPTED_FILE_PATH,
    OUTPUT_KEY_FILE_PATH,
)

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

def calculate_frequency(text):
    """
    Подсчитывает частоту каждого символа в тексте.

    :param text: Текст для анализа.
    :return: Словарь с символами и их частотами, отсортированный по убыванию частоты.
    """
    try:
        frequency = defaultdict(float)
        total_characters = len(text)
        if total_characters == 0:
            raise ValueError("Текст пуст")

        for char in text:
            frequency[char] += 1

        frequency_index = {char: (count / total_characters) for char, count in frequency.items()}
        sorted_frequency_index = dict(sorted(frequency_index.items(), key=lambda item: item[1], reverse=True))
        return sorted_frequency_index

    except Exception as e:
        print(f"Ошибка при вычислении частоты символов: {e}")


def load_russian_frequencies(file_path):
    """
    Загружает частоты символов русского алфавита из JSON-файла.

    :param file_path: Путь к JSON-файлу с частотами.
    :return: Словарь с частотами символов.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")


def analyze_frequency(text):
    """
    Анализирует частоту символов в тексте.

    :param text: Текст для анализа.
    :return: Словарь с символами и их частотами.
    """
    freq_counter = Counter(text)
    total_chars = sum(freq_counter.values())
    return {char: count / total_chars for char, count in freq_counter.items()}

def get_mapping(encoded_freq, russian_freq):
    """
    Предназначена для сопоставления символов зашифрованного текста и символов русского алфавита
    :param encoded_freq: Словарь, где ключи — это символы зашифрованного текста, а значения — их частоты
    :param russian_freq: Словарь, где ключи — это символы русского алфавита, а значения — их частоты
    :return: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита
    """
    sorted_encoded = sorted(encoded_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_rus = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

    char_map = {}
    for (encoded_char, _), (rus_char, _) in zip(sorted_encoded, sorted_rus):
        if encoded_char not in char_map.values():
            char_map[encoded_char] = rus_char
    return char_map

def decrypt_text(text, mapping):
    """
    Расшифровывает текст с использованием предоставленного сопоставления.

    :param text: Зашифрованный текст.
    :param mapping: Словарь с сопоставлением символов.
    :return: Расшифрованный текст.
    """
    return ''.join(mapping.get(char, char) for char in text)

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