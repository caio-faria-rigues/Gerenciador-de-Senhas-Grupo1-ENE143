import hashlib, base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.fernet import Fernet

class PyCrypto:
    def __init__(self, validation_key, salt):
        #validation_key: hash modelo 256 em str da chave de criptografia armazenada no json
        #salt: bytes aleatórios armazenados no json
        self.validation_key = validation_key
        self.salt = salt

    def hash_password(self, password):
        #método estático usado para derivar a chave de validação
        #parâmetro (password): uma bytestr
        #retorna: a hash modelo SHA256 em str
        password = hashlib.sha256(password)
        password = password.hexdigest()
        return password

    def derive_encryption_key(self, master_password):
        #parâmetro (master_password): a senha mestra "crua" em str, precisa ser inserida pelo usuário
        #retorna: uma bytestr que serve de base para a chave de criptografia
        encryption_key = master_password.encode()
        kdf = Argon2id(
            salt = self.salt,
            length = 32,
            iterations = 6,
            lanes = 4,
            memory_cost = 256 * 1024
        )
        encryption_key = kdf.derive(encryption_key)
        return encryption_key

    def derive_validation_key(self, master_password):
        #parâmetro (master_password): a senha mestra "crua" em str, precisa ser inserida pelo usuário
        #retorna: a hash modelo SHA256 em str da chave de criptografia, serve para verificar se o usuário inseriu sua senha mestra corretamente
        validation_key = self.derive_encryption_key(master_password)
        validation_key = self.hash_password(validation_key)
        return validation_key

    def validate_key(self, input_password):
        #parâmetro (input_password): senha mestra digitada pelo usuário em str
        #retorna: True se a senha digitada corresponder a chave de validação armazenada no json, e False caso contrário
        input_password = self.derive_validation_key(input_password)
        return input_password == self.validation_key

    def encrypt_password(self, password, master_password):
        #parâmetro (password): uma senha comum em str a ser armazenada no json
        #parâmetro (master_password): a senha mestra em str que será transformada na chave de criptografia, PRECISA SER VALIDADA ANTES DE SER USADA!!!
        #retorna: a senha comum criptografada em str uando a chave de criptografia gerada à partir da senha mestra
        password = password.encode()
        key = self.derive_encryption_key(master_password)
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        return f.encrypt(password).decode()

    def decrypt_password(self, password, master_password):
        #parâmetro (password): uma senha comum criptografada em str armazenada no json
        #parâmetro (master_password): a senha mestra em str que será transformada na chave de criptografia, PRECISA SER VALIDADA ANTES DE SER USADA!!!
        #retorna: a senha comum descriptografada, se a senha mestra inserida for errada um gero será gerado provavelmente "crashando" o programa
        password = password.encode()
        key = self.derive_encryption_key(master_password)
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        return f.decrypt(password).decode()
