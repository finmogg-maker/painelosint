# 🚀 Guia de Deploy - Ferramenta OSINT

## ✅ Opções Recomendadas para Flask

### 1. **Render.com** (Recomendado - Grátis)

1. Acesse [render.com](https://render.com) e crie uma conta
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub/GitLab
4. Configure:
   - **Name**: seu-app-osint
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Adicione variáveis de ambiente se necessário
6. Clique em "Create Web Service"

**Arquivo necessário**: Crie um arquivo `Procfile` na raiz:
```
web: gunicorn app:app
```

### 2. **Railway.app** (Grátis com limites)

1. Acesse [railway.app](https://railway.app)
2. Clique em "New Project" → "Deploy from GitHub repo"
3. Selecione seu repositório
4. Railway detecta automaticamente Python e instala dependências
5. Configure a porta (Railway usa variável de ambiente `PORT`)

**Modificação necessária no `app.py`**:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### 3. **PythonAnywhere** (Grátis para iniciantes)

1. Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crie uma conta gratuita
3. Faça upload dos arquivos via interface web ou Git
4. Configure o WSGI file para apontar para `app.py`
5. Recarregue o site

### 4. **Heroku** (Pago, mas tem tier grátis limitado)

1. Instale Heroku CLI
2. Execute:
```bash
heroku create seu-app-osint
git push heroku main
```

**Arquivos necessários**:
- `Procfile`: `web: gunicorn app:app`
- `runtime.txt`: `python-3.11.0` (ou sua versão)

## 📝 Preparação do Projeto

### 1. Adicionar Gunicorn

Adicione ao `requirements.txt`:
```
gunicorn>=21.2.0
```

### 2. Criar Procfile (para Render/Heroku)

Crie um arquivo `Procfile` na raiz:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 3. Atualizar app.py para produção

Modifique o final do `app.py`:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 4. Configurar variáveis de ambiente

Configure estas variáveis na plataforma escolhida:
- `SECRET_KEY`: Uma chave secreta aleatória (use `secrets.token_hex(32)`)

## 📚 Recursos

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

