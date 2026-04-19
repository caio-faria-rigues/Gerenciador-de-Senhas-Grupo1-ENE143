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

############# Descriptografar dicionário lista_json_site

        for i in lista_json_site:
            if i["Site"] == site and i["User"] == user:
                print("Atenção! Você não pode adicionar o mesmo usuário para um só site.")
                erro = True
                break
            else:
                erro = False

        if not erro:
            lista_json_site.append({"Site": site, "User": user, "Senha": senha_site})

############# Criptografar dicionário lista_json_site

        with open(self.arquivo_json, 'w') as arq:
            json.dump(lista_json_site, arq, indent=4)

    def deletar_site(self, site, user):
        # Deleta um item da lista. Recebe o nome do Site e o nome do usuário a ser deletado.

        # Verifica a senha:
        seguranca = Seguranca()

        if seguranca.verificarSenha():

            with open(self.arquivo_json, 'r') as arq:
                lista_json_site = json.load(arq)

############# Descriptografar lista-dicionário lista_json_site

            '''
            Se houver necessidade de deletar via indice, comentar 
            o código ativo logo abaixo e descomentar o código:
            
            i=0
            del lista_json_site[i]
            '''

            lista_json_site = [s for s in lista_json_site if s["Site"] != site or s["User"] != user]

############# Criptografar lista-dicionário lista_json_site

            with open(self.arquivo_json, 'w') as arq:
                json.dump(lista_json_site, arq, indent=4)

    def atualizar_info(self, site, user, info_nova = "****", tipo = "Senha"):

        with open(self.arquivo_json, 'r') as arq:
            lista_json_site = json.load(arq)

############# Descriptografar lista-dicionário lista_json_site

        '''
        Se for usar índice para escolher qual dicionário atualizar,
        comentar o looping for abaixo e descomentar o código:
        
        lista_json_site[i][tipo] = info_nova
        '''
        for s in lista_json_site:
            if s["Site"] == site and s["User"] == user:
                s[tipo] = info_nova

############# Criptografar lista-dicionário lista_json_site

        with open(self.arquivo_json, 'w') as arq:
            json.dump(lista_json_site, arq, indent=4)


if __name__ == '__main__':
    json_Manager = Json_Manipulador()
    #json_Manager.adicionar_site("site5", "daniel", "123")
    #json_Manager.deletar_site("site3","daniel")
    json_Manager.atualizar_info("site3", "Filipe", "Web.com", "Site")
