import json
from os.path import dirname, realpath, join


class Seguranca:
    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.arquivo = join(self.root, "..", "data", "arquivo_desimportante.json")

    def arquivo_json(self):
        with open(self.arquivo, "r") as arq:
            __senha = json.load(arq)
        __senha = __senha["senha"]
        return __senha

    def encriptar(self, __senha):
        """
        Recebe a lógica de criptografia da hash no lugar de += "123"
        """
        __senha += "123"
        return __senha

    def verificarSenha(self):
        # Verifica se a entrada do metodo e igual à senha mestra
        __senha_digitada = input("Diga sua senha: ")
        __senha_digitada = self.encriptar(__senha_digitada)

        __senha_mestra = self.arquivo_json()
        if __senha_digitada == __senha_mestra:
            return True
        else:
            print("Senha incorreta.")
            return False


if __name__ == "__main__":
    seguranca = Seguranca()
    print(seguranca.verificarSenha("daniel"))