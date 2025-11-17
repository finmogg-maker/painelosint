# 🔧 Solução: gunicorn não encontrado

## ❌ Problema

O erro `gunicorn: command not found` significa que o gunicorn não foi instalado durante o build.

## ✅ Soluções

### Solução 1: Atualizar requirements.txt no GitHub

O `requirements.txt` no seu repositório GitHub pode não ter o gunicorn. 

**Faça isso:**

1. Certifique-se de que o `requirements.txt` local tem:
   ```
   Flask>=3.0.0
   requests>=2.31.0
   flask-login>=0.6.3
   werkzeug>=3.0.0
   gunicorn>=21.2.0
   ```

2. Faça commit e push:
   ```bash
   git add requirements.txt
   git commit -m "Add gunicorn to requirements"
   git push
   ```

3. No Render, clique em **"Manual Deploy"** → **"Deploy latest commit"**

### Solução 2: Usar comando alternativo (temporário)

No Render, mude o **Start Command** para:

```
python -m gunicorn app:app --bind 0.0.0.0:$PORT
```

Ou tente:

```
pip install gunicorn && gunicorn app:app --bind 0.0.0.0:$PORT
```

### Solução 3: Verificar se requirements.txt está correto

Certifique-se de que não há espaços extras ou linhas vazias problemáticas no final do arquivo.

