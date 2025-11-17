import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "osint_database.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela para buscas por nome
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nome_buscas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                resultado TEXT,
                fonte TEXT,
                data_busca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_busca TEXT
            )
        ''')
        
        # Tabela para buscas de processos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processo_buscas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_processo TEXT NOT NULL,
                resultado TEXT,
                fonte TEXT,
                data_busca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT
            )
        ''')
        
        # Tabela para buscas de fotos/imagens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foto_buscas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                termo_busca TEXT NOT NULL,
                url_imagem TEXT,
                resultado TEXT,
                fonte TEXT,
                data_busca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hash_imagem TEXT
            )
        ''')
        
        # Tabela para buscas de CPF
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cpf_buscas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                cpf_formatado TEXT,
                resultado TEXT,
                fonte TEXT,
                informacoes TEXT,
                data_busca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT
            )
        ''')
        
        # Tabela para histórico de buscas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_buscas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_busca TEXT NOT NULL,
                termo_busca TEXT NOT NULL,
                resultado TEXT,
                data_busca TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela para registro de IPs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ip_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                path TEXT,
                method TEXT,
                user_id TEXT,
                session_id TEXT,
                data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                country TEXT,
                city TEXT
            )
        ''')
        
        # Tabela para usuários e permissões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                nome TEXT,
                senha_hash TEXT,
                google_id TEXT UNIQUE,
                permissao TEXT DEFAULT 'user',
                ip_whitelist TEXT,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP
            )
        ''')
        
        # Tabela para permissões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS permissoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                email TEXT,
                permissao TEXT NOT NULL,
                data_atribuicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atribuido_por TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Verificar e adicionar coluna senha_hash se não existir
        try:
            cursor.execute('PRAGMA table_info(usuarios)')
            columns = [column[1] for column in cursor.fetchall()]
            if 'senha_hash' not in columns:
                cursor.execute('ALTER TABLE usuarios ADD COLUMN senha_hash TEXT')
                conn.commit()
        except Exception as e:
            print(f"Note: Could not add senha_hash column (may already exist): {e}")
        
        # Criar usuários padrão se não existirem
        from werkzeug.security import generate_password_hash
        
        # Conta principal do usuário
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE email = ?', ('finmogg@gmail.com',))
        if cursor.fetchone()[0] == 0:
            senha_hash = generate_password_hash('MOGG1212')
            cursor.execute('''
                INSERT INTO usuarios (email, nome, senha_hash, permissao)
                VALUES (?, ?, ?, ?)
            ''', ('finmogg@gmail.com', 'Administrator', senha_hash, 'admin'))
        else:
            # Atualizar senha
            senha_hash = generate_password_hash('MOGG1212')
            cursor.execute('UPDATE usuarios SET senha_hash = ?, permissao = ? WHERE email = ?', 
                         (senha_hash, 'admin', 'finmogg@gmail.com'))
        
        # Conta admin padrão (backup)
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE email = ?', ('admin@seita.com',))
        if cursor.fetchone()[0] == 0:
            senha_hash = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO usuarios (email, nome, senha_hash, permissao)
                VALUES (?, ?, ?, ?)
            ''', ('admin@seita.com', 'Administrator', senha_hash, 'admin'))
        
        conn.commit()
        conn.close()
    
    def salvar_busca_nome(self, nome: str, resultado: str, fonte: str, tipo_busca: str = "nome"):
        """Salva resultado de busca por nome"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nome_buscas (nome, resultado, fonte, tipo_busca)
            VALUES (?, ?, ?, ?)
        ''', (nome, resultado, fonte, tipo_busca))
        conn.commit()
        conn.close()
    
    def salvar_busca_processo(self, numero_processo: str, resultado: str, fonte: str, status: str = "pendente"):
        """Salva resultado de busca por processo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO processo_buscas (numero_processo, resultado, fonte, status)
            VALUES (?, ?, ?, ?)
        ''', (numero_processo, resultado, fonte, status))
        conn.commit()
        conn.close()
    
    def salvar_busca_foto(self, termo_busca: str, url_imagem: str, resultado: str, fonte: str, hash_imagem: str = ""):
        """Salva resultado de busca por foto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO foto_buscas (termo_busca, url_imagem, resultado, fonte, hash_imagem)
            VALUES (?, ?, ?, ?, ?)
        ''', (termo_busca, url_imagem, resultado, fonte, hash_imagem))
        conn.commit()
        conn.close()
    
    def salvar_busca_cpf(self, cpf: str, cpf_formatado: str, resultado: str, fonte: str, informacoes: str, status: str = "encontrado"):
        """Salva resultado de busca por CPF"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cpf_buscas (cpf, cpf_formatado, resultado, fonte, informacoes, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cpf, cpf_formatado, resultado, fonte, informacoes, status))
        conn.commit()
        conn.close()
    
    def salvar_historico(self, tipo_busca: str, termo_busca: str, resultado: str):
        """Salva no histórico geral"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historico_buscas (tipo_busca, termo_busca, resultado)
            VALUES (?, ?, ?)
        ''', (tipo_busca, termo_busca, resultado))
        conn.commit()
        conn.close()
    
    def buscar_historico_nome(self, nome: str) -> List[Dict]:
        """Busca histórico de buscas por nome"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM nome_buscas WHERE nome LIKE ? ORDER BY data_busca DESC
        ''', (f'%{nome}%',))
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': r[0],
            'nome': r[1],
            'resultado': r[2],
            'fonte': r[3],
            'data_busca': r[4],
            'tipo_busca': r[5]
        } for r in results]
    
    def buscar_historico_processo(self, numero_processo: str) -> List[Dict]:
        """Busca histórico de buscas por processo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM processo_buscas WHERE numero_processo LIKE ? ORDER BY data_busca DESC
        ''', (f'%{numero_processo}%',))
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': r[0],
            'numero_processo': r[1],
            'resultado': r[2],
            'fonte': r[3],
            'data_busca': r[4],
            'status': r[5]
        } for r in results]
    
    def buscar_historico_foto(self, termo_busca: str) -> List[Dict]:
        """Busca histórico de buscas por foto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM foto_buscas WHERE termo_busca LIKE ? ORDER BY data_busca DESC
        ''', (f'%{termo_busca}%',))
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': r[0],
            'termo_busca': r[1],
            'url_imagem': r[2],
            'resultado': r[3],
            'fonte': r[4],
            'data_busca': r[5],
            'hash_imagem': r[6]
        } for r in results]
    
    def obter_todas_buscas(self, limite: int = 50) -> List[Dict]:
        """Obtém todas as buscas recentes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tipo_busca, termo_busca, resultado, data_busca 
            FROM historico_buscas 
            ORDER BY data_busca DESC 
            LIMIT ?
        ''', (limite,))
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'tipo_busca': r[0],
            'termo_busca': r[1],
            'resultado': r[2],
            'data_busca': r[3]
        } for r in results]
    
    def criar_banco_personalizado(self, nome_banco: str) -> Dict:
        """Cria um novo banco de dados personalizado"""
        try:
            if not nome_banco.endswith('.db'):
                nome_banco += '.db'
            
            # Criar novo banco
            temp_db = Database(nome_banco)
            return {
                'sucesso': True,
                'mensagem': f'Banco de dados "{nome_banco}" criado com sucesso!',
                'nome': nome_banco
            }
        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro ao criar banco: {str(e)}',
                'nome': nome_banco
            }
    
    def listar_bancos_disponiveis(self) -> List[str]:
        """Lista todos os arquivos .db no diretório"""
        import glob
        bancos = glob.glob("*.db")
        return bancos
    
    def deletar_banco(self, nome_banco: str) -> Dict:
        """Deleta um banco de dados"""
        try:
            if os.path.exists(nome_banco):
                os.remove(nome_banco)
                return {
                    'sucesso': True,
                    'mensagem': f'Banco de dados "{nome_banco}" deletado com sucesso!'
                }
            else:
                return {
                    'sucesso': False,
                    'mensagem': f'Banco de dados "{nome_banco}" não encontrado!'
                }
        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro ao deletar banco: {str(e)}'
            }
    
    def obter_info_banco(self) -> Dict:
        """Obtém informações sobre o banco de dados atual"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Contar registros em cada tabela
            cursor.execute('SELECT COUNT(*) FROM nome_buscas')
            total_nomes = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM processo_buscas')
            total_processos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM foto_buscas')
            total_fotos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM historico_buscas')
            total_historico = cursor.fetchone()[0]
            
            # Tamanho do arquivo
            tamanho = os.path.getsize(self.db_name) if os.path.exists(self.db_name) else 0
            tamanho_mb = tamanho / (1024 * 1024)
            
            conn.close()
            
            return {
                'nome': self.db_name,
                'tamanho_mb': round(tamanho_mb, 2),
                'total_nomes': total_nomes,
                'total_processos': total_processos,
                'total_fotos': total_fotos,
                'total_historico': total_historico,
                'total_geral': total_nomes + total_processos + total_fotos
            }
        except Exception as e:
            return {
                'erro': str(e)
            }
    
    def limpar_banco(self, tabela: str = None) -> Dict:
        """Limpa dados do banco de dados"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tabelas permitidas (prevenção de SQL injection)
            tabelas_permitidas = ['nome_buscas', 'processo_buscas', 'foto_buscas', 'historico_buscas']
            
            if tabela:
                if tabela not in tabelas_permitidas:
                    return {
                        'sucesso': False,
                        'mensagem': f'Tabela "{tabela}" não é permitida!'
                    }
                cursor.execute(f'DELETE FROM {tabela}')
                conn.commit()
                conn.close()
                return {
                    'sucesso': True,
                    'mensagem': f'Tabela "{tabela}" limpa com sucesso!'
                }
            else:
                # Limpar todas as tabelas
                cursor.execute('DELETE FROM nome_buscas')
                cursor.execute('DELETE FROM processo_buscas')
                cursor.execute('DELETE FROM foto_buscas')
                cursor.execute('DELETE FROM historico_buscas')
                conn.commit()
                conn.close()
                return {
                    'sucesso': True,
                    'mensagem': 'Todos os dados foram limpos com sucesso!'
                }
        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro ao limpar banco: {str(e)}'
            }
    
    def registrar_ip(self, ip_address: str, user_agent: str = '', path: str = '', method: str = '', user_id: str = None, session_id: str = None, country: str = None, city: str = None):
        """Registra acesso de um IP"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ip_logs (ip_address, user_agent, path, method, user_id, session_id, country, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ip_address, user_agent, path, method, user_id, session_id, country, city))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging IP: {e}")
    
    def obter_ips_recentes(self, limite: int = 100) -> List[Dict]:
        """Obtém IPs recentes"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ip_logs 
                ORDER BY data_acesso DESC 
                LIMIT ?
            ''', (limite,))
            results = cursor.fetchall()
            conn.close()
            
            return [{
                'id': r[0],
                'ip_address': r[1],
                'user_agent': r[2],
                'path': r[3],
                'method': r[4],
                'user_id': r[5],
                'session_id': r[6],
                'data_acesso': r[7],
                'country': r[8],
                'city': r[9]
            } for r in results]
        except Exception as e:
            return []
    
    def obter_estatisticas_ips(self) -> Dict:
        """Obtém estatísticas de IPs"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(DISTINCT ip_address) FROM ip_logs')
            ips_unicos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM ip_logs')
            total_acessos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM ip_logs WHERE data_acesso > datetime("now", "-24 hours")')
            acessos_24h = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'ips_unicos': ips_unicos,
                'total_acessos': total_acessos,
                'acessos_24h': acessos_24h
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def criar_usuario(self, email: str, nome: str = '', senha_hash: str = None, google_id: str = None, permissao: str = 'user') -> Dict:
        """Cria um novo usuário"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, nome, senha_hash, google_id, permissao)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, nome, senha_hash, google_id, permissao))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {'sucesso': True, 'id': user_id}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
    
    def obter_usuario_por_email(self, email: str) -> Optional[Dict]:
        """Obtém usuário por email"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Usar nomes de colunas explicitamente para evitar problemas de ordem
            cursor.execute('''
                SELECT id, email, nome, google_id, permissao, ip_whitelist, ativo, data_criacao, ultimo_acesso, senha_hash
                FROM usuarios WHERE email = ?
            ''', (email,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'email': result[1],
                    'nome': result[2],
                    'google_id': result[3],
                    'permissao': result[4],
                    'ip_whitelist': result[5],
                    'ativo': result[6],
                    'data_criacao': result[7],
                    'ultimo_acesso': result[8],
                    'senha_hash': result[9]
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def atualizar_permissao(self, email: str, permissao: str, atribuido_por: str) -> Dict:
        """Atualiza permissão de um usuário"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Atualizar permissão
            cursor.execute('UPDATE usuarios SET permissao = ? WHERE email = ?', (permissao, email))
            
            # Registrar na tabela de permissões
            cursor.execute('''
                INSERT INTO permissoes (email, permissao, atribuido_por)
                VALUES (?, ?, ?)
            ''', (email, permissao, atribuido_por))
            
            conn.commit()
            conn.close()
            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
    
    def listar_usuarios(self) -> List[Dict]:
        """Lista todos os usuários"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, email, nome, google_id, permissao, ip_whitelist, ativo, data_criacao, ultimo_acesso, senha_hash
                FROM usuarios ORDER BY data_criacao DESC
            ''')
            results = cursor.fetchall()
            conn.close()
            
            return [{
                'id': r[0],
                'email': r[1],
                'nome': r[2],
                'google_id': r[3],
                'permissao': r[4],
                'ip_whitelist': r[5],
                'ativo': r[6],
                'data_criacao': r[7],
                'ultimo_acesso': r[8],
                'senha_hash': r[9]
            } for r in results]
        except Exception as e:
            return []

