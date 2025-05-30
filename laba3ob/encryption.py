from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


class FileEncryptor:
    """Класс для шифрования файлов с использованием Blowfish"""

    def __init__(self, symmetric_key):
        """Инициализирует шифратор с симметричным ключом"""
        self.symmetric_key = symmetric_key
        self.iv = os.urandom(8)

    def encrypt(self, plaintext):
        """Шифрует данные с использованием Blowfish
        :param plaintext: Исходные данные для шифрования
        :return: Зашифрованные данные
        """
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(algorithms.Blowfish(self.symmetric_key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        return encryptor.update(padded_data) + encryptor.finalize()