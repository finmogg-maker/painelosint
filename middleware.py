from flask import request, session
from database import Database
from auth_system import get_user_info as get_user_from_session
import re

db = Database()

def get_client_ip():
    """Obtém o IP real do cliente"""
    # Verifica headers de proxy
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

def log_request():
    """Registra o acesso no banco de dados"""
    try:
        # Ignorar requisições estáticas, API admin e login
        if (request.path.startswith('/static/') or 
            request.path.startswith('/api/admin/') or 
            request.path == '/login' or
            request.path.startswith('/api/auth/')):
            return
        
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent', '')
        path = request.path
        method = request.method
        user_id = session.get('user', {}).get('id') if 'user' in session else None
        
        # Gerar ou obter session_id
        if 'session_id' not in session:
            import secrets
            session['session_id'] = secrets.token_hex(16)
        session_id = session.get('session_id', '')
        
        # Registrar no banco
        db.registrar_ip(
            ip_address=ip,
            user_agent=user_agent,
            path=path,
            method=method,
            user_id=user_id,
            session_id=session_id
        )
    except Exception as e:
        print(f"Error logging request: {e}")

def is_admin(user_email: str = None) -> bool:
    """Verifica se o usuário é admin"""
    if not user_email:
        user = get_user_from_session()
        if not user:
            return False
        user_email = user.get('email')
    
    if not user_email:
        return False
    
    usuario = db.obter_usuario_por_email(user_email)
    if usuario and usuario.get('permissao') == 'admin':
        return True
    
    return False

def has_permission(user_email: str, required_permission: str) -> bool:
    """Verifica se o usuário tem a permissão necessária"""
    if not user_email:
        user = get_user_from_session()
        if not user:
            return False
        user_email = user.get('email')
    
    if not user_email:
        return False
    
    usuario = db.obter_usuario_por_email(user_email)
    if not usuario:
        return False
    
    permissao = usuario.get('permissao', 'user')
    
    # Hierarquia de permissões
    permissoes = {
        'user': 0,
        'member': 1,
        'moderator': 2,
        'admin': 3
    }
    
    user_level = permissoes.get(permissao, 0)
    required_level = permissoes.get(required_permission, 0)
    
    return user_level >= required_level

