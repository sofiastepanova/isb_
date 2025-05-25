import os
import json
import argparse
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class HybridCryptoSystem:
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
        :return: Кортеж
        """
        print("Генерация ключей RSA...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        print("Ключи RSA успешно сгенерированы")
        return self.private_key, self.public_key

    def save_keys(self, encrypted_sym_key_path, public_key_path, private_key_path):
        """Сохраняет все ключи в файлы.
        :param encrypted_sym_key_path: Путь для зашифрованного симметричного ключа
        :param public_key_path: Путь для публичного ключа
        :param private_key_path: Путь для приватного ключа
        """
        print("Сохранение ключей...")


        with open(public_key_path, 'wb') as pub_out:
            pub_out.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))


        with open(private_key_path, 'wb') as priv_out:
            priv_out.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Шифр и сохр сим ключа
        encrypted_key = self.public_key.encrypt(
            self.symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(encrypted_sym_key_path, 'wb') as sym_out:
            sym_out.write(encrypted_key)

        print(f"Публичный ключ сохранен в {public_key_path}")
        print(f"Приватный ключ сохранен в {private_key_path}")
        print(f"Зашифрованный симметричный ключ сохранен в {encrypted_sym_key_path}")

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

    def encrypt_file(self, input_file, output_file):
        """Шифрует файл с использованием Blowfish
        :param input_file: Путь к исходному файлу
        :param output_file: Путь для зашифрованного файла
        """
        print(f"Шифрование файла {input_file}...")

        # Генерация вектора инициализации
        self.iv = os.urandom(8)


        with open(input_file, 'rb') as f:
            plaintext = f.read()


        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Шифр
        cipher = Cipher(algorithms.Blowfish(self.symmetric_key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()


        with open(output_file, 'wb') as f:
            f.write(self.iv)
            f.write(ciphertext)


        # посмотреть норм символы

        print("\nHex-дамп зашифрованного файла:")
        with open(output_file, 'rb') as f:
            print(f.read().hex())

        print(f"Файл зашифрован и сохранен в {output_file}")

    def decrypt_file(self, input_file, output_file):
        """Расшифровывает файл, зашифрованный Blowfish
        :param input_file: Путь к зашифрованному файлу.
        :param output_file: Путь для расшифрованного файла.
        """
        print(f"Расшифровка файла {input_file}...")


        with open(input_file, 'rb') as f:
            iv = f.read(8)  # Первые 8 байт - IV
            ciphertext = f.read()

        # Расшифр
        cipher = Cipher(algorithms.Blowfish(self.symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Удаляем паддинг
        unpadder = padding.PKCS7(64).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()


        with open(output_file, 'wb') as f:
            f.write(decrypted)

        print(f"Файл расшифрован и сохранен в {output_file}")


def get_valid_key_size():
    """Получает от пользователя размер ключа Blowfish
    :return: Проверенный размер ключа в битах
    """
    while True:
        try:
            key_size = int(input("Введите размер ключа Blowfish (32-448 бит с шагом 8): "))
            if key_size < 32 or key_size > 448 or key_size % 8 != 0:
                print("Ошибка: Размер ключа должен быть 32-448 бит с шагом 8")
                continue
            return key_size
        except ValueError:
            print("Ошибка: Введите целое число")


def main():
    """Функция обрабатывающая аргументы командной строки и управляющая криптооперациями."""
    parser = argparse.ArgumentParser(description='Гибридная криптосистема (Blowfish + RSA)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true', help='Режим генерации ключей')
    group.add_argument('-enc', '--encrypt', action='store_true', help='Режим шифрования файла')
    group.add_argument('-dec', '--decrypt', action='store_true', help='Режим расшифровки файла')

    parser.add_argument('--key-size', type=int, default=None,
                        help='Размер ключа Blowfish (32-448 бит с шагом 8)')
    parser.add_argument('--settings', type=str, default='settings.json',
                        help='Путь к файлу настроек (по умолчанию: settings.json)')

    args = parser.parse_args()

    # Загрузка настроек
    try:
        with open(args.settings) as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл настроек {args.settings} не найден")
        return

    crypto = HybridCryptoSystem()

    if args.generate:
        print("\n= Режим генерации ключей =")


        if args.key_size is not None:
            try:
                crypto.validate_key_size(args.key_size)
                key_size = args.key_size
            except ValueError as e:
                print(e)
                return
        else:
            key_size = get_valid_key_size()

        # Генерация ключей
        crypto.generate_symmetric_key(key_size)
        crypto.generate_asymmetric_keys()
        crypto.save_keys(
            settings['symmetric_key'],
            settings['public_key'],
            settings['private_key']
        )

    elif args.encrypt:
        print("\n= Режим шифрования =")
        crypto.load_private_key(settings['private_key'])
        crypto.decrypt_symmetric_key(settings['symmetric_key'])
        crypto.encrypt_file(
            settings['initial_file'],
            settings['encrypted_file']
        )

    elif args.decrypt:
        print("\n= Режим расшифровки =")
        crypto.load_private_key(settings['private_key'])
        crypto.decrypt_symmetric_key(settings['symmetric_key'])
        crypto.decrypt_file(
            settings['encrypted_file'],
            settings['decrypted_file']
        )


if __name__ == "__main__":
    main()