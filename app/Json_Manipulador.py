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
        self.root = dirname(realpath(__file__))
        self.arquivo_json = join(self.root, "data", "arquivo_json.json")
        self.master_password = master_password
        self.seguranca = Seguranca()

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
        Adiciona uma nova credencial ao cofre. A senha é criptografada.
        :return: (bool, mensagem)
        """
        lista_sites = self._ler_cofre()

        for item in lista_sites:
            if item["Site"] == site and item["User"] == user:
                return False, "Usuário já cadastrado para este site."

        senha_cripto = self.seguranca.encrypt_password(senha_site, master_password)

        lista_sites.append({
            "Site": site,
            "User": user,
            "Senha": senha_cripto
        })

        self._salvar_cofre(lista_sites)
        return True, "Senha adicionada com sucesso!"

    def deletar_site(self, indice):
        """Remove uma entrada específica do cofre pelo índice."""
        lista_sites = self._ler_cofre()
        lista_sites.pop(indice)
        self._salvar_cofre(lista_sites)

    def atualizar_info(self, indice, nova_info, tipo="Senha"):
        """
        Atualiza campos (Site, User ou Senha).
        Realiza a criptografia automática antes de salvar se o tipo for Senha.

        BUG CORRIGIDO: `self.tipo` trocado por `tipo` (variável local).
        """
        lista_sites = self._ler_cofre()

        if tipo == "Senha":
            nova_info = self.seguranca.encrypt_password(nova_info, self.master_password)

        # CORREÇÃO: era `self.tipo` — variável inexistente que causava NameError
        lista_sites[indice][tipo] = nova_info

        self._salvar_cofre(lista_sites)

    def descriptografar_umso(self, indice, master_password):
        """
        Descriptografa a senha de uma única entrada do cofre.

        BUG CORRIGIDO: o método já estava correto estruturalmente.
        O problema era que `Seguranca` era re-instanciada sem o salt persistido
        corretamente. Agora funciona desde que Seguranca.__init__ carregue
        o salt salvo em base64 string (sem converter para bytes antes do super().__init__).
        """
        lista_sites = self._ler_cofre()
        senha_clara = self.seguranca.decrypt_password(
            lista_sites[indice]["Senha"], master_password
        )
        return senha_clara