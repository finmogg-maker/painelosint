from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from flask import session
import secrets

db = Database()

def criar_conta(email: str, nome: str, senha: str) -> dict:
    """Cria uma nova conta de usuário"""
    # Verificar se email já existe
    usuario = db.obter_usuario_por_email(email)
    if usuario:
        return {'sucesso': False, 'erro': 'Email already registered'}
    
    # Hash da senha
    senha_hash = generate_password_hash(senha)
    
    # Verificar se é o primeiro usuário (sem admins)
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE permissao = ?', ('admin',))
    admin_count = cursor.fetchone()[0]
    conn.close()
    
    # Se não há admins, tornar o primeiro usuário admin
    permissao = 'admin' if admin_count == 0 else 'user'
    
    # Criar usuário
    resultado = db.criar_usuario(
        email=email,
        nome=nome,
        senha_hash=senha_hash,
        permissao=permissao
    )
    
    return resultado

def fazer_login(email: str, senha: str) -> dict:
    """Faz login do usuário"""
    usuario = db.obter_usuario_por_email(email)
    
    if not usuario:
        return {'sucesso': False, 'erro': 'Invalid email or password'}
    
    if not usuario.get('ativo'):
        return {'sucesso': False, 'erro': 'Account is inactive'}
    
    # Verificar senha
    senha_hash = usuario.get('senha_hash')
    if not senha_hash or not check_password_hash(senha_hash, senha):
        return {'sucesso': False, 'erro': 'Invalid email or password'}
    
    # Criar sessão
    session['user'] = {
        'id': str(usuario.get('id')),
        'email': usuario.get('email'),
        'name': usuario.get('nome'),
        'permissao': usuario.get('permissao')
    }
    
    # Atualizar último acesso
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE email = ?', (email,))
    conn.commit()
    conn.close()
    
    return {'sucesso': True, 'usuario': usuario}

def fazer_logout():
    """Faz logout do usuário"""
    session.pop('user', None)
    return {'sucesso': True}

def is_authenticated():
    """Verifica se o usuário está autenticado"""
    return 'user' in session

def get_user_info():
    """Obtém informações do usuário da sessão"""
    return session.get('user', None)

def alterar_senha(email: str, senha_atual: str, nova_senha: str) -> dict:
    """Altera a senha do usuário"""
    usuario = db.obter_usuario_por_email(email)
    
    if not usuario:
        return {'sucesso': False, 'erro': 'User not found'}
    
    if not usuario.get('ativo'):
        return {'sucesso': False, 'erro': 'Account is inactive'}
    
    # Verificar senha atual
    senha_hash = usuario.get('senha_hash')
    if not senha_hash or not check_password_hash(senha_hash, senha_atual):
        return {'sucesso': False, 'erro': 'Current password is incorrect'}
    
    # Validar nova senha
    if len(nova_senha) < 6:
        return {'sucesso': False, 'erro': 'New password must be at least 6 characters'}
    
    # Atualizar senha
    try:
        nova_senha_hash = generate_password_hash(nova_senha)
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET senha_hash = ? WHERE email = ?', 
                      (nova_senha_hash, email))
        conn.commit()
        conn.close()
        
        return {'sucesso': True, 'mensagem': 'Password changed successfully'}
    except Exception as e:
        return {'sucesso': False, 'erro': f'Error updating password: {str(e)}'}

