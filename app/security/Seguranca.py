import json
import base64
from os.path import dirname, realpath, join, exists
from os import urandom
from app.Criptografia import PyCrypto

class Seguranca(PyCrypto):
    """
    Classe responsável pela gestão da segurança da Senha Mestra do sistema.
    Herda de PyCrypto para utilizar funções de derivação de chave e validação de hash.
    """
    def __init__(self):
        """
        Inicializa a classe de segurança, carregando o salt e o hash da senha mestra
        armazenados no arquivo JSON de segurança.
        """
        self.root = dirname(realpath(__file__))
        self.arquivo = join(self.root, "..", "data", "seguranca.json")

        # Tenta carregar dados se o arquivo existir
        dados = self._ler_arquivo()
        
        if dados:
            # Converte salt de base64 string para bytes para o PyCrypto poder processar
            self._salt = base64.b64decode(dados['salt'])
            self.validation_key = dados['master_hash']
        else:
            self._salt = None
            self.validation_key = None

        super().__init__(self.validation_key, self._salt)

    def _ler_arquivo(self):
        """
        Lê o arquivo de segurança JSON de forma privada.
        :return: Dicionário com os dados ou None em caso de erro/inexistência.
        """
        if not exists(self.arquivo):
            return None
        try:
            with open(self.arquivo, "r") as arq:
                return json.load(arq)
        except Exception:
            return None

    def esta_configurado(self):
        """
        Verifica se o sistema já possui uma senha mestra definida (se o arquivo existe e tem dados).
        :return: True se configurado, False caso contrário.
        """
        return self.validation_key is not None and self._salt is not None

    def verificar_senha(self, senha_digitada):
        """
        Valida se a senha digitada corresponde ao hash armazenado no sistema.
        :param senha_digitada: Senha em texto claro fornecida pelo usuário.
        :return: True se a senha estiver correta.
        """
        if not self.esta_configurado():
            return False
        return self.validate_key(senha_digitada)

    def encriptar_dados(self, dados, senha_mestra):
        """Alias para encrypt_password, mais genérico."""
        return self.encrypt_password(dados, senha_mestra)

    def descriptografar_dados(self, dados_cripto, senha_mestra):
        """Alias para decrypt_password, mais genérico."""
        return self.decrypt_password(dados_cripto, senha_mestra)

    def inicializar(self, senha_mestra):
        """
        Configura o sistema pela primeira vez, gerando um novo salt e derivando o hash
        da senha mestra para armazenamento persistente.
        :param senha_mestra: A nova senha mestra a ser definida.
        """
        # Gera o salt como string
        print(f"senha-mestra parâmetro de Seguranca.inicializar:({senha_mestra})")
        self._salt = self.generate_salt()

        # Atualiza a instância atual para uso imediato das funções de criptografia
        self.validation_key = self.derive_validation_key(senha_mestra)

        dados = {
            "master_hash": self.validation_key,
            "salt": self._salt,
        }

        # Garante que a pasta data existe antes de tentar salvar o arquivo
        import os
        os.makedirs(dirname(self.arquivo), exist_ok=True)

        with open(self.arquivo, "w") as arq:
            json.dump(dados, arq, indent=4)