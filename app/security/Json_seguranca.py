import json
from os.path import dirname, realpath, join
from app.security.Seguranca import Seguranca

class Json_seguranca:
    """
    Controla operações globais de segurança, como configuração inicial e re-criptografia
    do cofre para troca de senha mestra.
    """
    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.arquivo_seguranca = join(self.root, "..", "data", "seguranca.json")
        self.seg = Seguranca()

    def inicializar_sistema(self, nova_senha_mestra):
        """
        Gera os dados de segurança iniciais (salt e hash) para uma nova senha mestra.
        """
        self.seg.inicializar(nova_senha_mestra)
        return True

    def trocar_senha_mestra(self, senha_antiga, senha_nova):
        """
        Altera a senha mestra do sistema:
        1. Valida a senha atual.
        2. Descriptografa todo o cofre com a senha antiga.
        3. Gera novos parâmetros (salt/hash) para a senha nova.
        4. Re-criptografa todo o cofre com a senha nova.
        """
        if not self.seg.esta_configurado():
            return False, "Sistema não configurado."

        if not self.seg.verificar_senha(senha_antiga):
            return False, "Senha atual incorreta."

        # Passo 1: descriptografar TUDO com o salt/senha antigos — antes de qualquer mudança
        from app.Json_Manipulador import Json_Manipulador
        jm = Json_Manipulador(senha_antiga)
        dados_cifrados = jm._ler_cofre()

        dados_claros = []
        for item in dados_cifrados:
            senha_descriptografada = self.seg.descriptografar_dados(item["Senha"], senha_antiga)
            dados_claros.append({
                "Site": item["Site"],
                "User": item["User"],
                "Senha": senha_descriptografada if senha_descriptografada != 0
                        else "[ERRO AO DESCRIPTOGRAFAR]"
            })

        # Passo 2: SÓ AGORA gera novo salt e hash — após ter todos os dados claros em memória
        self.seg.inicializar(senha_nova)

        # Passo 3: limpa o cofre e reinsere tudo com a nova criptografia
        jm_novo = Json_Manipulador(senha_nova)
        with open(jm_novo.arquivo_json, 'w') as arq:
            json.dump([], arq)

        for item in dados_claros:
            if (item["Senha"] != "[ERRO AO DESCRIPTOGRAFAR]"
                    and item["Site"] != "[ERRO]"
                    and item["User"] != "[ERRO]"):
                jm_novo.adicionar_site(item["Site"], item["User"], item["Senha"], senha_nova)

        return True, "Senha mestra alterada com sucesso!"