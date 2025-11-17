# 🔍 Ferramenta OSINT

Ferramenta de Open Source Intelligence (OSINT) para busca de informações em múltiplas fontes.

## 📋 Funcionalidades

- **Busca por Nome**: Procura informações sobre pessoas em várias fontes públicas
- **Busca de Processos**: Localiza informações sobre processos judiciais
- **Busca de Fotos**: Realiza busca reversa de imagens e análise de metadados
- **Banco de Dados**: Armazena todos os resultados das buscas para consulta posterior
- **Histórico**: Visualiza todas as buscas realizadas anteriormente
- **Estatísticas**: Dashboard com estatísticas das buscas realizadas

## 🚀 Instalação

**Requisitos:** Python 3.6 ou superior

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

ou

```bash
pip3 install -r requirements.txt
```

## 💻 Como Usar

**Opção 1 - Script de inicialização (recomendado):**
```bash
python iniciar.py
```

ou

```bash
python3 iniciar.py
```

**Opção 2 - Executar diretamente:**
```bash
python app.py
```

ou

```bash
python3 app.py
```

2. Acesse no navegador:
```
http://localhost:5000
```

3. Use as abas para:
   - **Buscar Nome**: Digite um nome completo ou parcial
   - **Buscar Processo**: Digite o número do processo
   - **Buscar Foto**: Digite um termo e opcionalmente uma URL de imagem
   - **Histórico**: Visualize todas as buscas anteriores

## 📁 Estrutura do Projeto

```
ferramenta.py/
├── app.py              # Aplicação Flask principal
├── iniciar.py          # Script de inicialização (Python 3)
├── database.py         # Gerenciamento do banco de dados SQLite
├── osint_tools.py      # Ferramentas de busca OSINT
├── requirements.txt    # Dependências do projeto
├── templates/
│   └── index.html     # Interface web
└── osint_database.db  # Banco de dados (criado automaticamente)
```

## 🗄️ Banco de Dados

O banco de dados SQLite armazena:
- **nome_buscas**: Resultados de buscas por nome
- **processo_buscas**: Resultados de buscas de processos
- **foto_buscas**: Resultados de buscas de fotos
- **historico_buscas**: Histórico geral de todas as buscas

## ⚠️ Nota Importante

Esta ferramenta é uma demonstração de conceitos OSINT. As buscas são simuladas para fins educacionais. Em um ambiente de produção, você precisaria integrar com APIs reais de serviços OSINT e seguir todas as leis e regulamentações aplicáveis.

## 🔒 Segurança

- Use esta ferramenta apenas para fins legítimos e éticos
- Respeite a privacidade e os termos de serviço dos sites consultados
- Não use para atividades ilegais ou não autorizadas

## 📝 Licença

Este projeto é fornecido "como está" para fins educacionais.

