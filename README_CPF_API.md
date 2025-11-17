# Configuração de API Real para Consulta de CPF

## APIs Disponíveis

### 1. API Brasil
- **URL**: https://brasilapi.com.br
- **Status**: ⚠️ Endpoint de CPF pode não estar disponível publicamente
- **Nota**: A estrutura está preparada para quando a API estiver disponível

### 2. Serasa
- **URL**: https://api.serasa.com.br
- **Requer**: Chave de API (paga)
- **Configuração**: 
  ```bash
  export SERASA_API_KEY="sua_chave_aqui"
  export SERASA_API_URL="https://api.serasa.com.br/v1/consulta-cpf"
  ```

### 3. Quero Meus Dados
- **URL**: https://api.queromeusdados.com.br
- **Requer**: Chave de API (paga)
- **Configuração**:
  ```bash
  export QUEROMEUSDADOS_API_KEY="sua_chave_aqui"
  export QUEROMEUSDADOS_URL="https://api.queromeusdados.com.br/v1/cpf"
  ```

## Como Configurar

### Windows (PowerShell)
```powershell
$env:SERASA_API_KEY="sua_chave"
$env:QUEROMEUSDADOS_API_KEY="sua_chave"
```

### Windows (CMD)
```cmd
set SERASA_API_KEY=sua_chave
set QUEROMEUSDADOS_API_KEY=sua_chave
```

### Linux/Mac
```bash
export SERASA_API_KEY="sua_chave"
export QUEROMEUSDADOS_API_KEY="sua_chave"
```

## Arquivo .env (Recomendado)

Crie um arquivo `.env` na raiz do projeto:

```env
SERASA_API_KEY=sua_chave_serasa
SERASA_API_URL=https://api.serasa.com.br/v1/consulta-cpf
QUEROMEUSDADOS_API_KEY=sua_chave_qmd
QUEROMEUSDADOS_URL=https://api.queromeusdados.com.br/v1/cpf
```

E instale python-dotenv:
```bash
pip install python-dotenv
```

## Status Atual

✅ **API Brasil**: Funcionando automaticamente (pública e gratuita)
⚠️ **Outras APIs**: Requerem configuração de chaves

## Notas Legais

- Todas as consultas devem respeitar a LGPD (Lei Geral de Proteção de Dados)
- Use apenas APIs autorizadas e legítimas
- Não armazene dados pessoais sem consentimento
- Consulte apenas CPFs com autorização legal

