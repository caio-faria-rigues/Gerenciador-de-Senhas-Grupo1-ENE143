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

#########################################################################

    def encriptar(self, __senha):
        """
        Recebe a lógica de criptografia da hash no lugar de += "123"
        """
        __senha += "1234"
        return __senha

##########################################################################

    def verificarSenha(self):
        # Verifica se a entrada do metodo e igual à senha mestra
        __senha_digitada = input("Digite sua senha: ")
        __senha_digitada = self.encriptar(__senha_digitada)

        __senha_mestra = self.arquivo_json()

        if __senha_digitada == __senha_mestra:
            __senha_mestra = ""
            return True
        else:
            for i in range(2):
                print("Senha incorreta.")
                __senha_digitada = input("Digite sua senha novamente: ")
                __senha_digitada = self.encriptar(__senha_digitada)
                if __senha_digitada == __senha_mestra:
                    __senha_mestra = ""
                    return True
                else:
                    pass

        __senha_mestra = ""
        return False


if __name__ == "__main__":
    seguranca = Seguranca()
    print(seguranca.verificarSenha("daniel"))