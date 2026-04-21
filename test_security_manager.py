
import os
import json
import shutil
from app.Json_Manipulador import Json_Manipulador
from app.security.Seguranca import Seguranca
from app.security.Json_seguranca import Json_seguranca

def test_security_flow():
    print("Iniciando testes de segurança e manipulação de JSON...")
    
    # Configurações iniciais
    master_pass = "senha_mestra_123"
    novo_site = "google.com"
    novo_user = "usuario_teste"
    nova_senha = "senha_secreta_456"
    '''
    # 1. Inicializar o sistema
    js = Json_seguranca()
    print(f"Passo 1: Inicializando sistema com senha mestra '{master_pass}'...")
    js.inicializar_sistema(master_pass)
    '''
    seg = Seguranca()
    if seg.esta_configurado():
        print(" [OK] Sistema configurado com sucesso.")
    else:
        print(" [ERRO] Falha ao configurar o sistema.")
        return

    # 2. Verificar senha mestra
    if seg.verificar_senha(master_pass):
        print(" [OK] Verificação de senha mestra funcionando.")
    else:
        print(" [ERRO] Falha na verificação da senha mestra.")
        return

    # 3. Adicionar uma nova credencial (com criptografia de Site e User)
    jm = Json_Manipulador(master_pass)
    print(f"Passo 2: Adicionando site '{novo_site}' para o usuário '{novo_user}'...")
    sucesso, msg = jm.adicionar_site(novo_site, novo_user, nova_senha)
    
    if sucesso:
        print(f" [OK] {msg}")
    else:
        print(f" [ERRO] {msg}")
        return

    # 4. Verificar se os dados no arquivo JSON estão criptografados
    with open(jm.arquivo_json, 'r') as f:
        dados_no_arquivo = json.load(f)
        item = dados_no_arquivo[0]
        print("Passo 3: Verificando criptografia no arquivo JSON...")
        print(f" - Site (no arquivo): {item['Site']}")
        print(f" - User (no arquivo): {item['User']}")
        print(f" - Senha (no arquivo): {item['Senha']}")
        
        if item['Site'] != novo_site and item['User'] != novo_user and item['Senha'] != nova_senha:
            print(" [OK] Todos os campos estão criptografados no arquivo.")
        else:
            print(" [ERRO] Algum campo não foi criptografado corretamente.")

    # 5. Listar e verificar se a descriptografia está correta
    print("Passo 4: Listando sites e verificando descriptografia...")
    sites = jm.listar_sites()
    if len(sites) > 0:
        s = sites[0]
        if s['Site'] == novo_site and s['User'] == novo_user and s['Senha'] == nova_senha:
            print(f" [OK] Descriptografia bem-sucedida: Site={s['Site']}, User={s['User']}, Senha={s['Senha']}")
        else:
            print(f" [ERRO] Dados descriptografados incorretamente: {s}")
    else:
        print(" [ERRO] Nenhum site listado.")

    # 6. Testar atualização de informação
    print("Passo 5: Testando atualização de usuário...")
    novo_user_2 = "usuario_atualizado"
    sucesso, msg = jm.atualizar_info(novo_site, novo_user, novo_user_2, tipo="User")
    if sucesso:
        sites = jm.listar_sites()
        if sites[0]['User'] == novo_user_2:
            print(f" [OK] Usuário atualizado e descriptografado corretamente para '{novo_user_2}'.")
        else:
            print(f" [ERRO] Falha ao verificar usuário atualizado.")
    else:
        print(f" [ERRO] {msg}")
    '''
    # 7. Testar troca de senha mestra
    print("Passo 6: Testando troca de senha mestra...")
    nova_master_pass = "nova_senha_mestra_789"
    sucesso, msg = js.trocar_senha_mestra(master_pass, nova_master_pass)
    
    if sucesso:
        print(" [OK] Senha mestra alterada com sucesso.")
        # Tentar listar com a NOVA senha mestra
        jm_novo = Json_Manipulador(nova_master_pass)
        sites = jm_novo.listar_sites()
        if len(sites) > 0 and sites[0]['User'] == novo_user_2:
            print(f" [OK] Dados acessíveis com a nova senha mestra. Usuário: {sites[0]['User']}")
        else:
            print(f" [ERRO] Falha ao acessar dados após troca de senha mestra.")
    else:
        print(f" [ERRO] {msg}")

    # 8. Testar deleção
    print("Passo 7: Testando deleção de site...")
    if jm_novo.deletar_site(novo_site, novo_user_2):
        if len(jm_novo.listar_sites()) == 0:
            print(" [OK] Site deletado com sucesso.")
        else:
            print(" [ERRO] Site ainda consta na lista após deleção.")
    else:
        print(" [ERRO] Falha ao executar deleção.")
    '''
if __name__ == "__main__":
    test_security_flow()
