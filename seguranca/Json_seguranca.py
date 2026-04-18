import json
from os.path import dirname, realpath, join
from seguranca.Seguranca import Seguranca


class Json_seguranca:
    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.arquivo = join(self.root, "..","data","arquivo_desimportante.json")

    def arquivo_json(self):
        with open(self.arquivo, "r") as arq:
            __senha = json.load(arq)
        __senha = __senha["senha"]
        return __senha

    def adicionar_senha_mestra(self):
        # Metodo que adiciona ou troca senha
        with open(self.arquivo, "r") as arq:
            __senha_antiga = json.load(arq)

        #verificar a senha
        seguranca = Seguranca()
        verificar = seguranca.verificarSenha()
        if verificar:
            __senha_nova = input("Digite sua nova senha: ")
            __senha_nova_2 = input("Digite sua nova senha novamente: ")
            while __senha_nova != __senha_nova_2:
                print("Senhas não batem.")
                __senha_nova = input("Digite sua nova senha: ")
                __senha_nova_2 = input("Digite sua nova senha novamente: ")

            ####################################
            """
            Adicionar camada de criptografia aqui.
            Exemplo:
                __senha_nova = criptografa(__senha_nova)
            """
            __senha_nova = Seguranca().encriptar(__senha_nova)
            ####################################

            with open(self.arquivo, "w") as arq:
                json.dump({"senha": __senha_nova}, arq)
                print("Senha salva com sucesso.")
        else:
            print("Não será possível realizar a operação.")

if __name__ == "__main__":
    Json_seguranca = Json_seguranca()
    Json_seguranca.adicionar_senha_mestra()