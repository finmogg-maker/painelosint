from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import Database
from osint_tools import OSINTTools
from auth_system import criar_conta, fazer_login, fazer_logout, is_authenticated, get_user_info, alterar_senha
from middleware import log_request, is_admin, has_permission, get_client_ip
import json
import os
import secrets
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))
db = Database()
osint = OSINTTools()

# Middleware para capturar IPs em todas as requisições
@app.before_request
def before_request():
    log_request()

@app.route('/')
def index():
    """Página principal"""
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    """Página de login"""
    if is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/auth/register', methods=['POST'])
def register():
    """API para criar conta"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        nome = data.get('nome', '').strip()
        senha = data.get('senha', '').strip()
        
        if not email or not nome or not senha:
            return jsonify({'sucesso': False, 'erro': 'All fields are required'}), 400
        
        if len(senha) < 6:
            return jsonify({'sucesso': False, 'erro': 'Password must be at least 6 characters'}), 400
        
        resultado = criar_conta(email, nome, senha)
        
        if resultado.get('sucesso'):
            # Fazer login automático após registro
            login_result = fazer_login(email, senha)
            if login_result.get('sucesso'):
                return jsonify({'sucesso': True, 'mensagem': 'Account created successfully'}), 200
            return jsonify({'sucesso': True, 'mensagem': 'Account created. Please login.'}), 200
        else:
            return jsonify(resultado), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_api():
    """API para fazer login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        senha = data.get('senha', '').strip()
        
        if not email or not senha:
            return jsonify({'sucesso': False, 'erro': 'Email and password are required'}), 400
        
        resultado = fazer_login(email, senha)
        
        if resultado.get('sucesso'):
            return jsonify({'sucesso': True, 'mensagem': 'Login successful'}), 200
        else:
            return jsonify(resultado), 401
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/api/buscar/nome', methods=['POST'])
def buscar_nome():
    """API para buscar por nome"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        
        if not nome:
            return jsonify({'erro': 'Nome não fornecido'}), 400
        
        # Realizar busca OSINT
        resultado = osint.buscar_nome(nome)
        
        # Salvar no banco de dados
        for fonte in resultado.get('fontes', []):
            db.salvar_busca_nome(
                nome=nome,
                resultado=fonte.get('resultado', ''),
                fonte=fonte.get('nome', ''),
                tipo_busca='nome'
            )
            db.salvar_historico(
                tipo_busca='nome',
                termo_busca=nome,
                resultado=json.dumps(resultado, ensure_ascii=False)
            )
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/buscar/processo', methods=['POST'])
def buscar_processo():
    """API para buscar por processo"""
    try:
        data = request.get_json()
        numero_processo = data.get('numero_processo', '').strip()
        
        if not numero_processo:
            return jsonify({'erro': 'Número do processo não fornecido'}), 400
        
        # Validar formato
        if not osint.validar_processo(numero_processo):
            return jsonify({'erro': 'Formato de processo inválido'}), 400
        
        # Realizar busca OSINT
        resultado = osint.buscar_processo(numero_processo)
        
        # Salvar no banco de dados
        for fonte in resultado.get('fontes', []):
            db.salvar_busca_processo(
                numero_processo=numero_processo,
                resultado=fonte.get('resultado', ''),
                fonte=fonte.get('nome', ''),
                status=resultado.get('status', 'pendente')
            )
            db.salvar_historico(
                tipo_busca='processo',
                termo_busca=numero_processo,
                resultado=json.dumps(resultado, ensure_ascii=False)
            )
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/buscar/foto', methods=['POST'])
def buscar_foto():
    """API para buscar por foto"""
    try:
        data = request.get_json()
        termo_busca = data.get('termo_busca', '').strip()
        url_imagem = data.get('url_imagem', '').strip()
        
        if not termo_busca:
            return jsonify({'erro': 'Termo de busca não fornecido'}), 400
        
        # Realizar busca OSINT
        resultado = osint.buscar_foto(termo_busca, url_imagem if url_imagem else None)
        
        # Salvar no banco de dados
        for fonte in resultado.get('fontes', []):
            db.salvar_busca_foto(
                termo_busca=termo_busca,
                url_imagem=url_imagem if url_imagem else '',
                resultado=fonte.get('resultado', ''),
                fonte=fonte.get('nome', ''),
                hash_imagem=resultado.get('hash_imagem', '')
            )
            db.salvar_historico(
                tipo_busca='foto',
                termo_busca=termo_busca,
                resultado=json.dumps(resultado, ensure_ascii=False)
            )
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/buscar/cpf', methods=['POST'])
def buscar_cpf():
    """API para buscar por CPF"""
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').strip()
        
        if not cpf:
            return jsonify({'erro': 'CPF não fornecido'}), 400
        
        # Realizar busca OSINT
        resultado = osint.buscar_cpf(cpf)
        
        # Se houver erro na validação
        if resultado.get('erro'):
            return jsonify(resultado), 400
        
        # Salvar no banco de dados
        cpf_limpo = resultado.get('cpf_limpo', '')
        cpf_formatado = resultado.get('cpf', '')
        informacoes = json.dumps(resultado.get('informacoes', {}), ensure_ascii=False)
        
        for fonte in resultado.get('fontes', []):
            db.salvar_busca_cpf(
                cpf=cpf_limpo,
                cpf_formatado=cpf_formatado,
                resultado=fonte.get('resultado', ''),
                fonte=fonte.get('nome', ''),
                informacoes=informacoes,
                status=resultado.get('status', 'encontrado')
            )
            db.salvar_historico(
                tipo_busca='cpf',
                termo_busca=cpf_formatado,
                resultado=json.dumps(resultado, ensure_ascii=False)
            )
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    """API para obter histórico de buscas"""
    try:
        tipo = request.args.get('tipo', '')
        termo = request.args.get('termo', '')
        
        if tipo == 'nome' and termo:
            historico = db.buscar_historico_nome(termo)
        elif tipo == 'processo' and termo:
            historico = db.buscar_historico_processo(termo)
        elif tipo == 'foto' and termo:
            historico = db.buscar_historico_foto(termo)
        else:
            historico = db.obter_todas_buscas()
        
        return jsonify(historico), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/estatisticas', methods=['GET'])
def obter_estatisticas():
    """API para obter estatísticas do banco de dados"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Contar buscas por tipo
        cursor.execute('SELECT COUNT(*) FROM nome_buscas')
        total_nomes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM processo_buscas')
        total_processos = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM foto_buscas')
        total_fotos = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_nomes': total_nomes,
            'total_processos': total_processos,
            'total_fotos': total_fotos,
            'total_geral': total_nomes + total_processos + total_fotos
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    fazer_logout()
    return jsonify({'sucesso': True}), 200

@app.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """API para alterar senha"""
    try:
        if not is_authenticated():
            return jsonify({'sucesso': False, 'erro': 'Authentication required'}), 401
        
        user = get_user_info()
        email = user.get('email')
        
        data = request.get_json()
        senha_atual = data.get('senha_atual', '').strip()
        nova_senha = data.get('nova_senha', '').strip()
        confirmar_senha = data.get('confirmar_senha', '').strip()
        
        if not senha_atual or not nova_senha or not confirmar_senha:
            return jsonify({'sucesso': False, 'erro': 'All fields are required'}), 400
        
        if nova_senha != confirmar_senha:
            return jsonify({'sucesso': False, 'erro': 'New passwords do not match'}), 400
        
        resultado = alterar_senha(email, senha_atual, nova_senha)
        
        if resultado.get('sucesso'):
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/api/user/profile', methods=['GET'])
def user_profile():
    """Get user profile information"""
    try:
        if is_authenticated():
            user = get_user_info()
            user_id = user.get('id')
            email = user.get('email')
            
            # Get user info from database
            usuario = db.obter_usuario_por_email(email)
            permissao = usuario.get('permissao', 'user') if usuario else 'user'
            
            # Get user statistics from database
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM nome_buscas WHERE fonte LIKE ?', (f'%{user_id}%',))
            name_searches = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM processo_buscas WHERE fonte LIKE ?', (f'%{user_id}%',))
            process_searches = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM foto_buscas WHERE fonte LIKE ?', (f'%{user_id}%',))
            photo_searches = cursor.fetchone()[0]
            
            conn.close()
            
            return jsonify({
                'authenticated': True,
                'name': user.get('name'),
                'email': email,
                'permissao': permissao,
                'is_admin': is_admin(email),
                'stats': {
                    'name_searches': name_searches,
                    'process_searches': process_searches,
                    'photo_searches': photo_searches
                }
            }), 200
        else:
            return jsonify({'authenticated': False}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Admin routes
def admin_required(f):
    """Decorator para rotas que requerem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({'erro': 'Authentication required'}), 401
        
        user = get_user_info()
        if not is_admin(user.get('email')):
            return jsonify({'erro': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
def admin_panel():
    """Admin panel page"""
    if not is_authenticated():
        return redirect(url_for('index'))
    
    user = get_user_info()
    if not is_admin(user.get('email')):
        return redirect(url_for('index'))
    
    return render_template('admin.html')

@app.route('/api/admin/ips', methods=['GET'])
@admin_required
def admin_get_ips():
    """Get IP logs"""
    try:
        limite = request.args.get('limit', 100, type=int)
        ips = db.obter_ips_recentes(limite)
        return jsonify(ips), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/ips/stats', methods=['GET'])
@admin_required
def admin_ip_stats():
    """Get IP statistics"""
    try:
        stats = db.obter_estatisticas_ips()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/usuarios', methods=['GET'])
@admin_required
def admin_get_usuarios():
    """Get all users"""
    try:
        usuarios = db.listar_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/admin/usuarios/permissao', methods=['POST'])
@admin_required
def admin_update_permissao():
    """Update user permission"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        permissao = data.get('permissao', '').strip()
        
        if not email or not permissao:
            return jsonify({'erro': 'Email and permission required'}), 400
        
        if permissao not in ['user', 'member', 'moderator', 'admin']:
            return jsonify({'erro': 'Invalid permission'}), 400
        
        user = get_user_info()
        resultado = db.atualizar_permissao(email, permissao, user.get('email'))
        
        if resultado.get('sucesso'):
            return jsonify({'sucesso': True, 'mensagem': f'Permission updated to {permissao}'}), 200
        else:
            return jsonify({'erro': resultado.get('erro', 'Error updating permission')}), 500
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Seita Research starting...")
    port = int(os.environ.get('PORT', 5000))
    print(f"Access: http://localhost:{port}")
    print("=" * 50)
    print("Default account created:")
    print("  Admin: finmogg@gmail.com / MOGG1212")
    print("=" * 50)
    # Em produção, debug deve ser False
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

