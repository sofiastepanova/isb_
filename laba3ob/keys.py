import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class KeyManager:
    """Гибридная криптосистема, объединяющая Blowfish и RSA"""

    def __init__(self):
        """Инициализирует криптосистему с пустыми ключами"""
        self.symmetric_key = None
        self.iv = None
        self.private_key = None
        self.public_key = None

    def validate_key_size(self, key_size):
        """Проверяет корректность размера ключа Blowfish.
        :param key_size: Размер ключа в битах.
        :raises ValueError: Если размер ключа недопустим.
        """
        if key_size < 32 or key_size > 448 or key_size % 8 != 0:
            raise ValueError(
                "Недопустимый размер ключа. Должен быть 32-448 бит с шагом 8 бит.\n"
                f"Получено: {key_size} бит."
            )

    def generate_symmetric_key(self, key_size=448):
        """Генерирует симметричный ключ Blowfish
        :param key_size: Размер ключа в битах
        :return: Сгенерированный симметричный ключ
        """
        self.validate_key_size(key_size)
        self.symmetric_key = os.urandom(key_size // 8)
        print(f"Сгенерирован {key_size}-битный симметричный ключ Blowfish")
        return self.symmetric_key

    def generate_asymmetric_keys(self):
        """Генерирует пару ключей RSA
        :return: Кортеж (приватный ключ, публичный ключ)
        """
        print("Генерация ключей RSA...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        print("Ключи RSA успешно сгенерированы")
        return self.private_key, self.public_key

    def load_private_key(self, private_key_path):
        """Загружает приватный ключ из файла.
        :param private_key_path: Путь к файлу с приватным ключом.
        :return: Загруженный приватный ключ.
        """
        print(f"Загрузка приватного ключа из {private_key_path}...")
        with open(private_key_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
        self.private_key = load_pem_private_key(private_bytes, password=None)
        return self.private_key

    def decrypt_symmetric_key(self, encrypted_sym_key_path):
        """Расшифровывает симметричный ключ с помощью RSA приватного ключа.
        :param encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
        :return: Расшифрованный симметричный ключ.
        """
        print(f"Расшифровка симметричного ключа из {encrypted_sym_key_path}...")
        with open(encrypted_sym_key_path, 'rb') as key_file:
            encrypted_key = key_file.read()

        self.symmetric_key = self.private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ успешно расшифрован")
        return self.symmetric_key