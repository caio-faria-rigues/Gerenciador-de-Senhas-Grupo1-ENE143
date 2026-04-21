import json
from os.path import dirname, realpath, join
from seguranca.Seguranca import Seguranca

class Json_seguranca:
    """
    Controla operações globais de segurança, como configuração inicial e re-criptografia
    do cofre para troca de senha mestra.
    """
    def __init__(self):
        """Inicializa o caminho para o arquivo de dados de segurança."""
        self.root = dirname(realpath(__file__))
        self.arquivo_seguranca = join(self.root, "..", "data", "seguranca.json")

    def inicializar_sistema(self, nova_senha_mestra):
        """
        Gera os dados de segurança iniciais (salt e hash) para uma nova senha mestra.
        """
        seg = Seguranca()
        seg.inicializar(nova_senha_mestra)
        return True

    def trocar_senha_mestra(self, senha_antiga, senha_nova):
        """
        Altera a senha mestra do sistema. Este processo exige:
        1. Validação da senha atual.
        2. Descriptografia de todo o cofre atual com a senha antiga.
        3. Geração de novos parâmetros de segurança (salt/hash).
        4. Re-criptografia de todo o cofre com a nova senha mestra.
        """
        seg = Seguranca()
        
        if not seg.esta_configurado():
            return False, "Sistema não configurado."

        if not seg.verificar_senha(senha_antiga):
            return False, "Senha atual incorreta."

        # Passo 1: Recuperar todas as senhas descriptografadas do cofre atual
        from Json_Manipulador import Json_Manipulador
        jm_antigo = Json_Manipulador(senha_antiga)
        dados_claros = jm_antigo.listar_sites()

        # Passo 2: Gerar novas credenciais de segurança mestra
        seg._salt = seg.generate_salt()
        nova_hash = seg.derive_validation_key(senha_nova)

        dados_seg = {
            "master_hash": nova_hash,
            "salt": seg._salt
        }
        
        # Salva o novo arquivo de segurança
        with open(self.arquivo_seguranca, "w") as arq:
            json.dump(dados_seg, arq, indent=4)

        # Passo 3: Limpar o cofre antigo e reinserir tudo com a nova criptografia
        jm_novo = Json_Manipulador(senha_nova)
        
        # Limpa o arquivo JSON existente
        with open(jm_novo.arquivo_json, 'w') as arq:
            json.dump([], arq)
            
        # Reinsere cada item, agora encriptado com a senha_nova
        for item in dados_claros:
            if item["Senha"] != "[ERRO AO DESCRIPTOGRAFAR]":
                jm_novo.adicionar_site(item["Site"], item["User"], item["Senha"])

        return True, "Senha mestra alterada com sucesso!"