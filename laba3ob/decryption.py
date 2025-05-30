from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class FileDecryptor:
    """Класс для дешифрования файлов с использованием Blowfish"""

    def __init__(self, symmetric_key):
        self.symmetric_key = symmetric_key

    def decrypt(self, ciphertext, iv):
        """Дешифрует данные с использованием Blowfish
        :param ciphertext: Зашифрованные данные
        :param iv: Вектор инициализации
        :return: Расшифрованные данные
        """
        cipher = Cipher(algorithms.Blowfish(self.symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(64).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()