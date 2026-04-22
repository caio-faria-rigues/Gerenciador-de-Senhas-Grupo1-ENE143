# Gerenciador de Senhas - Grupo 1 ENE143

Um gerenciador de senhas moderno, seguro e multiplataforma desenvolvido em Python utilizando a biblioteca **Flet** para a interface gráfica e padrões robustos de criptografia.

## Funcionalidades

- **Cofre de Senhas:** Armazenamento seguro de credenciais (Site/Serviço, Usuário e Senha).
- **Segurança Avançada:**
    - Proteção por **Senha Mestra**.
    - Derivação de chave utilizando **Argon2id** (altamente resistente a ataques de força bruta).
    - Criptografia simétrica com **Fernet (AES-128)**.
    - Sal (Salt) aleatório gerado individualmente para cada instalação.
- **Interface Intuitiva:**
    - Busca rápida de credenciais.
    - Cópia segura para a área de transferência.
    - Visualização/Ocultação de senhas sob demanda.
    - Gerenciamento completo (Adicionar, Visualizar e Excluir).
- **Navegação Fluida:** Sistema de visualizações (Views) modular para Início, Cofre e Configurações.

## Tecnologias Utilizadas

- **Python 3.x**
- **Flet:** Framework para interfaces ricas e responsivas.
- **Cryptography:** Biblioteca padrão ouro para operações de segurança em Python.
- **Argon2id:** Algoritmo de derivação de chave (KDF) vencedor da Password Hashing Competition.

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Recomenda-se o uso de um ambiente virtual.

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate
```

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto.
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Como Executar

Para iniciar a aplicação, execute o arquivo principal:

```bash
python main.py
```

## Estrutura do Projeto

```text
├── main.py                # Ponto de entrada da aplicação
├── app/                   # Lógica de negócio e backend local
│   ├── Criptografia.py    # Implementação de Argon2id e Fernet
│   ├── Json_Manipulador.py # Persistência de dados em JSON
│   ├── mainWindow.py      # Gerenciamento da janela principal
│   └── masterPasswordHandler.py # Lógica da senha mestra
├── views/                 # Definição das telas (UI)
│   ├── homeView.py        # Tela inicial
│   ├── vaultView.py       # Tela do cofre (listagem/busca)
│   ├── settingsView.py    # Tela de configurações
│   └── view.py            # Classe base para as views
├── src/                   # Componentes e recursos
│   ├── dialogs/           # Janelas modais (Nova senha, Inserir mestre)
│   ├── widgets/           # Componentes customizados (Barra de navegação)
│   └── pallete.py         # Definição de cores e temas
└── requirements.txt       # Dependências do projeto
```
