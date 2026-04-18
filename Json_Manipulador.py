import json
from os.path import join, dirname, realpath
from seguranca.Seguranca import Seguranca


class Json_Manipulador:
    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.arquivo_json = join(self.root, "data", "arquivo_json.json")
        self.lista_sites = []

    def adicionar_site(self, site, user, senha_site):
        # Adiciona um item à lista de Sites. Recebe o nome do site, usuário e a senha.
        with open(self.arquivo_json, 'r') as arq:
            lista_json_site = json.load(arq)
        for i in lista_json_site:
            if i["Site"] == site and i["User"] == user:
                print("Atenção! Você não pode adicionar o mesmo usuário para um só site.")
                erro = True
                break
            else:
                erro = False

        if not erro:
            lista_json_site.append({"Site": site, "User": user, "Senha": senha_site})

        with open(self.arquivo_json, 'w') as arq:
            json.dump(lista_json_site, arq, indent=4)

    def deletar_site(self, site, user):
        # Deleta um item da lista. Recebe o nome do Site e o nome do usuário a ser deletado.

        # Verifica a senha:
        seguranca = Seguranca()
        if seguranca.verificarSenha():
            with open(self.arquivo_json, 'r') as arq:
                lista_json_site = json.load(arq)
            lista_json_site = [s for s in lista_json_site if s["Site"] != site or s["User"] != user]

            with open(self.arquivo_json, 'w') as arq:
                json.dump(lista_json_site, arq, indent=4)


if __name__ == '__main__':
    json_Manager = Json_Manipulador()
    #json_Manager.adicionar_site("site3", "daniel", "123")
    json_Manager.deletar_site("site3","daniel")
