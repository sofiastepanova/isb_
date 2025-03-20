import json
import os
import random
from collections import Counter, defaultdict



alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '


def create_cipher_key(alphabet):
    """
    Ключ шифрования на основе переданного алфавита

    :param alphabet:  символы алфавита
    :return: Словарь
    """
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


def encrypt_text(text, cipher_key):
    """
    Шифрует текст с использованием предоставленного ключа

    :param text: Текст
    :param cipher_key: Словарь с ключами шифрования
    :return: Зашифрованный текст
    """
    return ''.join([cipher_key.get(char, char) for char in text])


def calculate_frequency(text):
    """
    Подсчитывает частоту каждого символа в тексте

    :param text: Текст для анализа
    :return: Словарь с символами и их частотами
    """
    frequency = defaultdict(float)
    total_characters = len(text)

    for char in text:
        frequency[char] += 1

    frequency_index = {char: (count / total_characters) for char, count in frequency.items()}
    sorted_frequency_index = dict(sorted(frequency_index.items(), key=lambda item: item[1], reverse=True))

    return sorted_frequency_index


def load_russian_frequencies(file_path):
    """
    Загружает частоты символов русского алфавита из JSON файла

    :param file_path: Путь к JSON-файлу с частотами
    :return: Словарь с частотами символов
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def analyze_frequency(text):
    """
    Анализирует частоту символов в тексте

    :param text: Текст для анализа
    :return: Словарь с символами и их частотами
    """
    freq_counter = Counter(text)
    total_chars = sum(freq_counter.values())
    return {char: count / total_chars for char, count in freq_counter.items()}


def create_mapping(cipher_freq, russian_freq):
    """
    сопоставляет символы зашифрованного текста с русским алфавитом

    :param cipher_freq: Частоты символов в зашифрованном тексте
    :param russian_freq: Частоты символов русского алфавита
    :return: Словарь с сопоставлением символов
    """
    sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_russian = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

    mapping = {}
    for (cipher_char, _), (russian_char, _) in zip(sorted_cipher, sorted_russian):
        if cipher_char not in mapping.values():
            mapping[cipher_char] = russian_char
    return mapping


def decrypt_text(text, mapping):
    """
    Расшифровывает текст с использованием сопоставления

    :param text: Зашифрованный текст
    :param mapping: Словарь с сопоставлением символов
    :return: Расшифрованный текст
    """
    return ''.join(mapping.get(char, char) for char in text)


def save_json(data, file_path):
    """
    Сохраняет данные в формате JSON

    :param data: Данные для сохранения
    :param file_path: Путь к файлу для сохранения
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def zad1():

    try:
        input_file_path = os.path.join('zad1', 'original_text.txt')
        output_encrypted_file_path = os.path.join('zad1', 'encrypted_text.txt')
        output_key_file_path = os.path.join('zad1', 'cipher_key.json')

        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Файл {input_file_path} не найден.")

        with open(input_file_path, 'r', encoding='utf-8') as file:
            original_text = file.read().upper()

        cipher_key = create_cipher_key(alphabet)

        encrypted_text = encrypt_text(original_text, cipher_key)

        with open(output_encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)

        save_json(cipher_key, output_key_file_path)

        print("Текст успешно зашифрован, ключ сохранен.")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")


def main():
    print("шифрование текста:")
    zad1()


if __name__ == "__main__":
    main()