# Documentação do Sistema de Segurança e Persistência

Este documento explica o funcionamento e a interação entre as classes `Json_Manipulador`, `Json_seguranca` e `Seguranca` no projeto de Gerenciador de Senhas.

---

## 1. Seguranca.py (`Classe Seguranca`)
Localização: `app/security/Seguranca.py`

Esta classe é a base da segurança do sistema. Ela herda de `PyCrypto` e gerencia a **Senha Mestra** e os parâmetros de criptografia (salt e hash).

### Principais Responsabilidades:
- **Persistência de Credenciais:** Lê e grava no arquivo `app/data/seguranca.json`.
- **Verificação:** Valida se a senha digitada pelo usuário coincide com a senha mestra armazenada.
- **Inicialização:** Configura o sistema pela primeira vez, gerando um novo *salt* aleatório.

### Métodos Chave:
- `esta_configurado()`: Retorna `True` se o sistema já possui uma senha mestra definida.
- `verificar_senha(senha_digitada)`: Compara a senha fornecida com o hash seguro no disco.
- `inicializar(senha_mestra)`: Cria o arquivo de segurança inicial com a senha escolhida.

---

## 2. Json_Manipulador.py (`Classe Json_Manipulador`)
Localização: `app/Json_Manipulador.py`

É o motor de **CRUD (Criação, Leitura, Atualização e Deleção)** do cofre de senhas. Todas as informações sensíveis (Site, Usuário, Senha) são armazenadas de forma criptografada no arquivo `app/data/arquivo_json.json`.

### Principais Responsabilidades:
- **Criptografia Transparente:** Ao adicionar um site, os dados são criptografados automaticamente usando a senha mestra.
- **Descriptografia sob Demanda:** Ao listar os sites, os dados são descriptografados para exibição.
- **Isolamento:** Requer a senha mestra no construtor para garantir que nenhuma operação seja feita sem autorização.

### Métodos Chave:
- `adicionar_site(site, user, senha_site)`: Criptografa e salva uma nova credencial.
- `listar_sites()`: Retorna a lista de todas as credenciais em texto claro (se a senha mestra estiver correta).
- `deletar_site(site, user)`: Remove uma entrada específica do cofre.
- `atualizar_info(site, user, nova_info, tipo)`: Atualiza um campo específico, re-criptografando o dado.

---

## 3. Json_seguranca.py (`Classe Json_seguranca`)
Localização: `app/security/Json_seguranca.py`

Esta classe lida com operações administrativas de segurança que afetam o sistema como um todo.

### Principais Responsabilidades:
- **Gestão de Ciclo de Vida:** Inicialização do sistema e troca de senha mestra.
- **Migração de Dados:** O método de troca de senha é o mais complexo, pois exige descriptografar todo o cofre com a senha antiga e re-criptografar com a nova.

### Métodos Chave:
- `inicializar_sistema(nova_senha_mestra)`: Interface para a primeira configuração.
- `trocar_senha_mestra(senha_antiga, senha_nova)`: Realiza a transição segura entre senhas mestras.

---

## Fluxo de Interação Típico

1. **Login:** 
   - O sistema usa `Seguranca.esta_configurado()` para saber se deve mostrar a tela de "Criar Senha" ou "Login".
   - `Seguranca.verificar_senha()` valida o acesso do usuário.
2. **Uso do Cofre:**
   - Uma instância de `Json_Manipulador` é criada passando a senha validada.
   - Chamadas como `adicionar_site` ou `listar_sites` utilizam internamente a lógica de criptografia da classe `Seguranca` (via herança de `PyCrypto`).
3. **Troca de Senha:**
   - O usuário solicita a troca via `Json_seguranca.trocar_senha_mestra`.
   - Esta classe utiliza tanto `Seguranca` (para validar e gerar novos hashes) quanto `Json_Manipulador` (para ler os dados antigos e gravar os novos).
