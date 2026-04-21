import json
import os
from os.path import join, dirname, realpath
from seguranca.Seguranca import Seguranca


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

    def adicionar_site(self, site, user, senha_site):
        """
        Adiciona uma nova credencial ao cofre. A senha do site é criptografada.
        :return: (bool, mensagem)
        """
        lista_sites = self._ler_cofre()

        # Verifica se já existe a mesma combinação de Site e Usuário
        for item in lista_sites:
            if item["Site"] == site and item["User"] == user:
                return False, "Usuário já cadastrado para este site."

        # Encripta a senha específica do site usando a senha mestra do sistema
        senha_cripto = self.seguranca.encrypt_password(senha_site, self.master_password)

        lista_sites.append({
            "Site": site,
            "User": user,
            "Senha": senha_cripto
        })

        self._salvar_cofre(lista_sites)
        return True, "Senha adicionada com sucesso!"

    def listar_sites(self):
        """
        Retorna todas as credenciais com as senhas já DESCRIPTOGRAFADAS para exibição.
        Se a senha mestra estiver incorreta, o campo senha trará um aviso de erro.
        """
        if not self.seguranca.verificar_senha(self.master_password):
            return [{"Site": "ERRO", "User": "SENHA MESTRA INVÁLIDA", "Senha": "---"}]

        lista_sites = self._ler_cofre()
        lista_descriptografada = []

        for item in lista_sites:
            try:
                # Tenta descriptografar usando a senha mestra fornecida no login
                senha_clara = self.seguranca.decrypt_password(item["Senha"], self.master_password)
                lista_descriptografada.append({
                    "Site": item["Site"],
                    "User": item["User"],
                    "Senha": senha_clara
                })
            except Exception:
                # Ocorre se a senha mestra mudou ou os dados foram corrompidos
                lista_descriptografada.append({
                    "Site": item["Site"],
                    "User": item["User"],
                    "Senha": "[ERRO AO DESCRIPTOGRAFAR]"
                })

        return lista_descriptografada

    def deletar_site(self, site, user):
        """
        Remove uma entrada específica do cofre.
        """
        lista_sites = self._ler_cofre()
        nova_lista = [s for s in lista_sites if not (s["Site"] == site and s["User"] == user)]

        if len(nova_lista) < len(lista_sites):
            self._salvar_cofre(nova_lista)
            return True
        return False

    def atualizar_info(self, site, user, nova_info, tipo="Senha"):
        """
        Atualiza campos (Site, User ou Senha).
        Se for 'Senha', realiza a criptografia automática antes de salvar.
        """
        lista_sites = self._ler_cofre()
        encontrado = False

        for item in lista_sites:
            if item["Site"] == site and item["User"] == user:
                if tipo == "Senha":
                    item["Senha"] = self.seguranca.encrypt_password(nova_info, self.master_password)
                else:
                    item[tipo] = nova_info
                encontrado = True
                break
        
        if encontrado:
            self._salvar_cofre(lista_sites)
            return True, f"{tipo} atualizado com sucesso."
        return False, "Site/Usuário não encontrado."