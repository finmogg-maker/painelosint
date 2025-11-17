# 🔧 Troubleshooting: Erro 502 no Render

## ❌ Erro 502 Bad Gateway

Este erro significa que o Render não consegue se conectar à sua aplicação Flask.

## ✅ Soluções

### 1. Verificar o Start Command

No Render, o **Start Command** deve ser:

```
gunicorn app:app --bind 0.0.0.0:$PORT
```

**OU** (versão mais simples que também funciona):

```
gunicorn app:app
```

### 2. Verificar os Logs do Render

1. No dashboard do Render, clique no seu serviço
2. Vá na aba **"Logs"**
3. Procure por erros de importação ou inicialização

**Erros comuns nos logs:**
- `ModuleNotFoundError` → Falta dependência no `requirements.txt`
- `ImportError` → Erro ao importar algum módulo
- `Port already in use` → Conflito de porta

### 3. Verificar Build Command

O **Build Command** deve ser:

```
pip install -r requirements.txt
```

### 4. Verificar se todas as dependências estão no requirements.txt

Certifique-se de que o `requirements.txt` contém:

```
Flask>=3.0.0
requests>=2.31.0
flask-login>=0.6.3
werkzeug>=3.0.0
gunicorn>=21.2.0
```

### 5. Verificar variáveis de ambiente

No Render, vá em **Environment** e adicione (se necessário):

- `SECRET_KEY`: Gere uma chave aleatória
  - Para gerar: `python -c "import secrets; print(secrets.token_hex(32))"`

### 6. Testar localmente com Gunicorn

Antes de fazer deploy, teste localmente:

```bash
pip install gunicorn
gunicorn app:app
```

Se funcionar localmente, deve funcionar no Render.

### 7. Verificar se há erros na inicialização

O problema pode estar na inicialização do `Database()` ou `OSINTTools()`. 

Verifique os logs do Render para ver se há erros específicos.

## 🔍 Comandos para Debug

### Verificar se o app pode ser importado:

```bash
python -c "from app import app; print('OK')"
```

### Testar com gunicorn localmente:

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

## 📞 Próximos Passos

1. Verifique os **Logs** no Render
2. Copie o erro completo
3. Verifique se todas as dependências estão instaladas
4. Teste localmente com gunicorn

## ⚠️ Problemas Comuns

### Problema: "ModuleNotFoundError: No module named 'X'"
**Solução**: Adicione a dependência faltante no `requirements.txt`

### Problema: "Address already in use"
**Solução**: Use `$PORT` no bind (já está no comando correto)

### Problema: App inicia mas dá 502
**Solução**: Verifique se o app está escutando em `0.0.0.0` e não em `127.0.0.1`

