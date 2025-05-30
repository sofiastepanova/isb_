import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes



class FileManager:
    """Класс для операций с файлами и сохранения ключей"""

    @staticmethod
    def save_keys(encrypted_sym_key_path, public_key_path, private_key_path,
                  public_key, private_key, symmetric_key):
        """Сохраняет все ключи в файлы.
        :param encrypted_sym_key_path: Путь для зашифрованного симметричного ключа
        :param public_key_path: Путь для публичного ключа
        :param private_key_path: Путь для приватного ключа
        :param public_key: Публичный ключ RSA
        :param private_key: Приватный ключ RSA
        :param symmetric_key: Симметричный ключ Blowfish
        """
        print("Сохранение ключей...")

        with open(public_key_path, 'wb') as pub_out:
            pub_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        with open(private_key_path, 'wb') as priv_out:
            priv_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        encrypted_key = public_key.encrypt(
            symmetric_key,
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

    @staticmethod
    def encrypt_file(input_file, output_file, encryptor):
        """Шифрует файл с использованием Blowfish
        :param input_file: Путь к исходному файлу
        :param output_file: Путь для зашифрованного файла
        :param encryptor: Объект FileEncryptor
        """
        print(f"Шифрование файла {input_file}...")

        with open(input_file, 'rb') as f:
            plaintext = f.read()

        ciphertext = encryptor.encrypt(plaintext)

        with open(output_file, 'wb') as f:
            f.write(encryptor.iv)
            f.write(ciphertext)

        print("\nHex-дамп зашифрованного файла:")
        with open(output_file, 'rb') as f:
            print(f.read().hex())

        print(f"Файл зашифрован и сохранен в {output_file}")

    @staticmethod
    def decrypt_file(input_file, output_file, decryptor):
        """Расшифровывает файл, зашифрованный Blowfish
        :param input_file: Путь к зашифрованному файлу
        :param output_file: Путь для расшифрованного файла
        :param decryptor: Объект FileDecryptor
        """
        print(f"Расшифровка файла {input_file}...")

        with open(input_file, 'rb') as f:
            iv = f.read(8)
            ciphertext = f.read()

        decrypted = decryptor.decrypt(ciphertext, iv)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

        print(f"Файл расшифрован и сохранен в {output_file}")

    @staticmethod
    def load_settings(settings_path):
        """Загружает настройки из JSON-файла
        :param settings_path: Путь к файлу настроек
        :return: Словарь с настройками
        """
        with open(settings_path) as f:
            return json.load(f)