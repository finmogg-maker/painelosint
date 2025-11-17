# 🚨 Solução Rápida: Deploy da Aplicação Flask

## ✅ Solução: Use Render.com (GRÁTIS e FÁCIL)

### Passo a Passo (5 minutos):

1. **Crie uma conta no Render**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Conecte seu repositório**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório com seu código

3. **Configure o deploy**
   - **Name**: `seu-app-osint` (ou qualquer nome)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Escolha "Free" (grátis)
   
   ⚠️ **Importante**: Se der erro 502, tente também: `gunicorn app:app`

4. **Adicione variável de ambiente** (opcional mas recomendado)
   - Clique em "Environment"
   - Adicione: `SECRET_KEY` = (gere uma chave aleatória)
   - Para gerar: `python -c "import secrets; print(secrets.token_hex(32))"`

5. **Deploy!**
   - Clique em "Create Web Service"
   - Aguarde 2-3 minutos
   - Pronto! Seu site estará no ar

### ✅ Arquivos já criados para você:

- ✅ `Procfile` - Configuração para Render/Heroku
- ✅ `requirements.txt` - Com gunicorn incluído
- ✅ `app.py` - Atualizado para produção
- ✅ `runtime.txt` - Versão do Python

## 🎯 Outras Opções Rápidas:

### Railway.app (Também grátis)
1. Acesse: https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Pronto! Detecta automaticamente Python

### PythonAnywhere (Grátis para iniciantes)
1. Acesse: https://www.pythonanywhere.com
2. Crie conta gratuita
3. Faça upload dos arquivos
4. Configure WSGI file

## 📞 Precisa de ajuda?

Todos os arquivos necessários já estão criados. Basta:
1. Fazer push para GitHub
2. Conectar no Render.com
3. Deploy automático!

**Tempo estimado: 5 minutos** ⏱️

