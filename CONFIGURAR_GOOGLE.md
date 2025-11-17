# 🔧 Como Configurar Google OAuth - Guia Rápido

## ⚠️ Erro Atual
Você está vendo o erro: **"OAuth client was not found" (Error 401: invalid_client)**

Isso significa que as credenciais do Google OAuth não estão configuradas.

## 📝 Passo a Passo (5 minutos)

### 1️⃣ Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Selecionar projeto"** → **"Novo Projeto"**
3. Nome do projeto: `Seita Research` (ou qualquer nome)
4. Clique em **"Criar"**

### 2️⃣ Ativar Google+ API

1. No menu lateral, vá em **"APIs e Serviços"** → **"Biblioteca"**
2. Procure por **"Google+ API"** ou **"People API"**
3. Clique em **"Ativar"**

### 3️⃣ Criar Credenciais OAuth

1. Vá em **"APIs e Serviços"** → **"Credenciais"**
2. Clique em **"+ CRIAR CREDENCIAIS"** → **"ID do cliente OAuth"**
3. Se pedir, configure a tela de consentimento:
   - Tipo de usuário: **"Externo"**
   - Nome do app: `Seita Research`
   - Email de suporte: seu email
   - Clique em **"Salvar e continuar"** até finalizar
4. Volte para **"Credenciais"** → **"+ CRIAR CREDENCIAIS"** → **"ID do cliente OAuth"**
5. Tipo de aplicativo: **"Aplicativo da Web"**
6. Nome: `Seita Research Web Client`
7. **URIs de redirecionamento autorizados**: Adicione:
   ```
   http://localhost:5000/auth/callback
   ```
8. Clique em **"Criar"**
9. **COPIE** o **Client ID** e **Client Secret** que aparecerem

### 4️⃣ Configurar no Windows

Abra o PowerShell e execute:

```powershell
$env:GOOGLE_CLIENT_ID="COLE_SEU_CLIENT_ID_AQUI"
$env:GOOGLE_CLIENT_SECRET="COLE_SEU_CLIENT_SECRET_AQUI"
```

**Exemplo:**
```powershell
$env:GOOGLE_CLIENT_ID="123456789-abcdefghijklmnop.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="GOCSPX-abcdefghijklmnopqrstuvwxyz"
```

### 5️⃣ Reiniciar a Aplicação

```bash
python iniciar.py
```

## ✅ Verificação

Após configurar, quando você clicar em "Login with Google", deve:
- Abrir a página de login do Google (não o erro)
- Permitir fazer login
- Redirecionar de volta para o site

## 🔍 Solução de Problemas

### Erro persiste?
1. Verifique se copiou o Client ID e Secret corretamente (sem espaços)
2. Verifique se adicionou o URI de redirecionamento: `http://localhost:5000/auth/callback`
3. Reinicie o PowerShell e configure novamente
4. Reinicie a aplicação

### Quer usar sem Google OAuth?
A aplicação funciona em modo demo sem Google OAuth, mas o login não funcionará.

## 📞 Precisa de Ajuda?

- Verifique se o projeto está ativo no Google Cloud Console
- Certifique-se de que a API está ativada
- O URI de redirecionamento deve ser EXATAMENTE: `http://localhost:5000/auth/callback`

