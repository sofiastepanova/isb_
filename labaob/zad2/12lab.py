import json
from collections import Counter
from constants2 import (
    INPUT_ENCODED_FILE,
    FREQUENCIES_FILE,
    OUTPUT_FREQUENCIES_FILE,
    OUTPUT_MAPPING_FILE,
    OUTPUT_DECRYPTED_FILE

)



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


def get_mapping(encoded_freq, russian_freq):
    """
    Предназначена для сопоставления символов зашифрованного текста и символов русского алфавита
    :param encoded_freq: Словарь, где ключи — это символы зашифрованного текста, а значения — их частоты
    :param russian_freq: Словарь, где ключи — это символы русского алфавита, а значения — их частоты
    :return: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита
    """
    try:
        if not encoded_freq or not russian_freq:
            raise ValueError("Один из входных словарей пуст.")

        sorted_encoded = sorted(encoded_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_rus = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

        char_map = {}
        for (encoded_char, _), (rus_char, _) in zip(sorted_encoded, sorted_rus):
            if encoded_char not in char_map.values():
                char_map[encoded_char] = rus_char

        return char_map
    except Exception as e:
        print(f"Ошибка при создании таблицы соответствий: {e}")



def decrypt_text(encoded_string, char_mapping):
    """
    Предназначена для расшифровки текста с использованием заранее созданного сопоставления
    :param encoded_string: Строка, представляющая зашифрованный текст, который нужно расшифровать.
    :param char_mapping: Словарь, где ключи — это символы зашифрованного текста, а значения — соответствующие символы русского алфавита.
    :return: Расшифрованный текст
    """
    return ''.join(char_mapping.get(ch, ch) for ch in encoded_string)


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
    :param text_data: Строка, содержащая текстовые данные, которые нужно сохранить в файл
    :param output_filename: Путь к фалу
    :return: None
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text_data)


def main():
    encrypted_data = get_cipher(INPUT_ENCODED_FILE)
    rus_char_freq = get_russian_frequencies(FREQUENCIES_FILE)

    freq_analysis = analyze_frequency(encrypted_data)

    sorted_freq = dict(
        sorted(
            freq_analysis.items(),
            key=lambda item: (-item[1], item[0])
        )
    )

    json_data(sorted_freq, OUTPUT_FREQUENCIES_FILE)

    translation_table = get_mapping(freq_analysis, rus_char_freq)
    decoded_text = decrypt_text(encrypted_data, translation_table)

    json_data(translation_table, OUTPUT_MAPPING_FILE)
    text_data(decoded_text, OUTPUT_DECRYPTED_FILE)

    print("Расшифрованный текст готов =) ")


if __name__ == "__main__":
    main()
