import math
from const import *
from scipy.special import erfc, gammainc




def frequency_test(bits):
    """
    Частотный побитовый тест
    :param bits: бинарная последовательность
    :return: результат выполнения теста
    """
    n = len(bits)
    sum_s = sum(1 if bit == '1' else -1 for bit in bits)
    return erfc(abs(sum_s) / math.sqrt(n) / math.sqrt(2))




def same_bits_test(bits):
    """
    Тест на одинаковые подряд идущие биты
    :param bits: последовательность
    :return: результат выполнения теста
    """
    n = len(bits)
    pi = bits.count('1') / n


    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    r = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            r += 1
    n = abs(r - 2 * n * pi * (1 - pi))
    d = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    return erfc(n / d)



def longest_sequence_test(data):
    """
    Тест на самую длинную последовательность единиц
    :param data: последовательность
    :return:результат выполнения теста
    """
    blocks = [data[i:i + 8] for i in range(0, len(data), 8)]
    v = [0, 0, 0, 0]


    for block in blocks:
        max_length = current_length = 0
        for digit in block:
            if digit == '1':
                current_length += 1
                max_length = max(max_length, current_length)
            else:
                current_length = 0

        match max_length:
            case max_length if max_length <= 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case max_length if max_length >= 4:
                v[3] += 1




    xi_square = sum(((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])
                    for i in range(len(v)))
    return gammainc((3 / 2), (xi_square / 2))


def load_sequences():
    """
    Загружает бинарные последовательности из файлов
    :return: кортеж (cpp_seq, java_seq)
    """
    cpp_seq = ""
    java_seq = ""

    try:
        with open("res.c++", "r") as f:
            cpp_seq = f.read().strip()
    except FileNotFoundError:
        print("Ошибка: файл res.c++ не найден")

    try:
        with open("res.java", "r") as f:
            java_seq = f.read().strip()
    except FileNotFoundError:
        print("Ошибка: файл res.java не найден")

    return cpp_seq, java_seq


def save_test_results(filename, cpp_seq, java_seq):
    """
    Сохраняет результаты тестов в файл
    :param filename: имя файла для сохранения
    :param cpp_seq: последовательность C++
    :param java_seq: последовательность Java
    """
    with open(filename, "w") as f:
        if cpp_seq:
            freq_cpp = frequency_test(cpp_seq)
            same_bits_cpp = same_bits_test(cpp_seq)
            long_seq_cpp = longest_sequence_test(cpp_seq)

            f.write("       ~Результаты для C++ последовательности~\n")
            f.write(f"1 Частотный тест: {freq_cpp:.8f}\n")
            f.write(f"2 Тест на одинаковые подряд идущие биты: {same_bits_cpp:.8f}\n")
            f.write(f"3 Тест на длинные последовательности: {long_seq_cpp:.8f}\n\n")
        else:
            f.write("последовательность c++ не была загружена\n\n")

        
        if java_seq:
            freq_java = frequency_test(java_seq)
            same_bits_java = same_bits_test(java_seq)
            long_seq_java = longest_sequence_test(java_seq)

            f.write("       ~Результаты для Java последовательности~\n")
            f.write(f"1 Частотный тест: {freq_java:.8f}\n")
            f.write(f"2 Тест на одинаковые подряд идущие биты: {same_bits_java:.8f}\n")
            f.write(f"3 Тест на длинные последовательности: {long_seq_java:.8f}\n")
        else:
            f.write(" последовательность lava не была загружена\n")


def main():
    cpp_sequence, java_sequence = load_sequences()
    if not cpp_sequence and not java_sequence:
        print("Ошибка: не удалось загрузить ни одну последовательность")
        return


    save_test_results("test_results.txt", cpp_sequence, java_sequence)
    print("Результаты тестов сохранены в test_results.txt")


if __name__ == "__main__":
    main()
