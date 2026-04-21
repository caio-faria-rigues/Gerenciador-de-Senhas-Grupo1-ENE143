import json
import os
from os.path import join, dirname, realpath
from app.security.Seguranca import Seguranca


class Json_Manipulador:
    """
    Gerencia as operações de CRUD (Criar, Ler, Atualizar, Deletar) do cofre de senhas.
    As senhas individuais são armazenadas de forma criptografada usando a senha mestra.
    """
    def __init__(self, master_password):
        """
        Inicializa o manipulador com a senha mestra atual.
        :param master_password: Senha necessária para criptografar/descriptografar os dados.
        """
        self.root = dirname(realpath(__file__))
        self.arquivo_json = join(self.root, "data", "arquivo_json.json")
        self.master_password = master_password
        self.seguranca = Seguranca()
        print(f"senha-mestra parâmetro de Json_Manipulador:({self.master_password})")

        # Garante que a estrutura de pastas exista
        os.makedirs(dirname(self.arquivo_json), exist_ok=True)
        if not os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, 'w') as arq:
                json.dump([], arq)

    def _ler_cofre(self):
        """Lê o conteúdo bruto do arquivo JSON."""
        try:
            with open(self.arquivo_json, 'r') as arq:
                return json.load(arq)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _salvar_cofre(self, dados):
        """Escreve os dados no arquivo JSON com formatação indentada."""
        with open(self.arquivo_json, 'w') as arq:
            json.dump(dados, arq, indent=4)

    def adicionar_site(self, site, user, senha_site, master_password):
        """
        Adiciona uma nova credencial ao cofre. O site, usuário e senha são criptografados.
        :return: (bool, mensagem)
        """
        lista_sites = self._ler_cofre()

        # Verifica se já existe a mesma combinação de Site e Usuário
        # Como estão criptografados, precisamos descriptografar para comparar
        for item in lista_sites:
            if item["Site"] == site and item["User"] == user:
                return False, "Usuário já cadastrado para este site."
            '''
            try:
                s_dec = self.seguranca.decrypt_password(item["Site"], master_password)
                if s_dec == 0: s_dec = item["Site"]
                
                u_dec = self.seguranca.decrypt_password(item["User"], master_password)
                if u_dec == 0: u_dec = item["User"]
                
                if s_dec == site and u_dec == user:
                    return False, "Usuário já cadastrado para este site."
            except Exception:
                continue
            '''
        senha_cripto = self.seguranca.encrypt_password(senha_site, master_password)
        print(f"senha mestre usada para criptografar:({master_password})")

        lista_sites.append({
            "Site": site,
            "User": user,
            "Senha": senha_cripto
        })

        self._salvar_cofre(lista_sites)
        return True, "Senha adicionada com sucesso!"

    '''
    def listar_sites(self):
        """
        Retorna todas as credenciais com os dados já DESCRIPTOGRAFADOS para exibição.
        Se a senha mestra estiver incorreta, os campos trarão aviso de erro.
        """
        if not self.seguranca.verificar_senha(self.master_password):
            return [{"Site": "ERRO", "User": "SENHA MESTRA INVÁLIDA", "Senha": "---"}]

        lista_sites = self._ler_cofre()
        lista_descriptografada = []

        for item in lista_sites:
            #try:
                # Tenta descriptografar usando a senha mestra fornecida no login
                # Fallback para o valor original se não estiver criptografado (migração)
                # site_claro = self.seguranca.decrypt_password(item["Site"], self.master_password)
                # if site_claro == 0: site_claro = item["Site"]
                
                # user_claro = self.seguranca.decrypt_password(item["User"], self.master_password)
                # if user_claro == 0: user_claro = item["User"]
                
                # senha_clara = self.seguranca.decrypt_password(item["Senha"], self.master_password)
                # if senha_clara == 0: senha_clara = item["Senha"]
                
                # lista_descriptografada.append({
                #     "Site": site_claro,
                #     "User": user_claro,
                #     "Senha": senha_clara
                # })
            #except Exception:
                # Ocorre se os dados estiverem corrompidos
            lista_descriptografada.append({
                "Site": item["Site"],
                "User": item["User"],
                "Senha": ""
            })

        return lista_descriptografada
    '''
    def deletar_site(self, indice):
        """
        Remove uma entrada específica do cofre.
        """
        lista_sites = self._ler_cofre()
        lista_sites.pop(indice)
        self._salvar_cofre(lista_sites)

        """
        nova_lista = []
        encontrado = False

        for item in lista_sites:
            try:
                s_dec = self.seguranca.decrypt_password(item["Site"], self.master_password)
                if s_dec == 0: s_dec = item["Site"]
                
                u_dec = self.seguranca.decrypt_password(item["User"], self.master_password)
                if u_dec == 0: u_dec = item["User"]
                
                if s_dec == site and u_dec == user:
                    encontrado = True
                    continue # Não adiciona na nova lista
            except Exception:
                pass
            nova_lista.append(item)

        if encontrado:
            self._salvar_cofre(nova_lista)
            return True
        return False
        """

    def atualizar_info(self, indice, nova_info, tipo="Senha"):
        """
        Atualiza campos (Site, User ou Senha).
        Realiza a criptografia automática antes de salvar.
        """
        lista_sites = self._ler_cofre()
        encontrado = False

        if tipo == "Senha":
            nova_info = self.seguranca.encrypt_password(nova_info, self.master_password)

        lista_sites[indice][self.tipo] = nova_info

        self._salvar_cofre(lista_sites)
        '''
        for item in lista_sites:
            try:
                s_dec = self.seguranca.decrypt_password(item["Site"], self.master_password)
                if s_dec == 0: s_dec = item["Site"]
                
                u_dec = self.seguranca.decrypt_password(item["User"], self.master_password)
                if u_dec == 0: u_dec = item["User"]
                
                if s_dec == site and u_dec == user:
                    item[tipo] = self.seguranca.encrypt_password(nova_info, self.master_password)
                    encontrado = True
                    break
            except Exception:
                continue
            '''
        '''
        if encontrado:
            self._salvar_cofre(lista_sites)
            return True, f"{tipo} atualizado com sucesso."
        return False, "Site/Usuário não encontrado."
        '''

    def descriptografar_umso(self, indice, master_password):
        lista_sites = self._ler_cofre()
        senha_clara = self.seguranca.decrypt_password(lista_sites[indice]["Senha"], master_password)

        return senha_clara
        #self.atualizar_info(indice, senha_clara)
