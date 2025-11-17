"""
Módulo para integração com APIs reais de consulta de CPF
Suporta múltiplos provedores de API
"""
import requests
import os
from typing import Dict, Optional
import json

# Tentar carregar variáveis de ambiente de arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv não instalado, usar apenas variáveis de ambiente do sistema

class CPFAPIClient:
    def __init__(self):
        # Configurações de API (definir em variáveis de ambiente)
        self.serasa_api_key = os.getenv('SERASA_API_KEY', '')
        self.serasa_api_url = os.getenv('SERASA_API_URL', 'https://api.serasa.com.br/v1/consulta-cpf')
        
        self.receita_federal_token = os.getenv('RECEITA_FEDERAL_TOKEN', '')
        self.receita_federal_url = os.getenv('RECEITA_FEDERAL_URL', 'https://www.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp')
        
        self.queromeusdados_api_key = os.getenv('QUEROMEUSDADOS_API_KEY', '')
        self.queromeusdados_url = os.getenv('QUEROMEUSDADOS_URL', 'https://api.queromeusdados.com.br/v1/cpf')
        
        # Headers padrão
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def consultar_serasa(self, cpf: str) -> Optional[Dict]:
        """
        Consulta CPF na API Serasa
        Requer: SERASA_API_KEY configurada
        """
        if not self.serasa_api_key:
            return None
        
        try:
            response = requests.post(
                self.serasa_api_url,
                headers={
                    **self.headers,
                    'Authorization': f'Bearer {self.serasa_api_key}'
                },
                json={'cpf': cpf},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Erro ao consultar Serasa: {e}")
        
        return None
    
    def consultar_receita_federal(self, cpf: str) -> Optional[Dict]:
        """
        Consulta situação cadastral na Receita Federal
        Nota: A Receita Federal não fornece API pública oficial
        Este método tenta fazer scraping (pode não funcionar)
        """
        # A Receita Federal não tem API pública oficial
        # Este é um placeholder para integração futura
        return None
    
    def consultar_queromeusdados(self, cpf: str) -> Optional[Dict]:
        """
        Consulta CPF na API Quero Meus Dados
        Requer: QUEROMEUSDADOS_API_KEY configurada
        """
        if not self.queromeusdados_api_key:
            return None
        
        try:
            response = requests.post(
                self.queromeusdados_url,
                headers={
                    **self.headers,
                    'X-API-Key': self.queromeusdados_api_key
                },
                json={'cpf': cpf},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Erro ao consultar Quero Meus Dados: {e}")
        
        return None
    
    def consultar_api_brasil(self, cpf: str) -> Optional[Dict]:
        """
        Consulta usando API Brasil (serviço público)
        URL: https://brasilapi.com.br
        Nota: A API Brasil pode não ter endpoint público de CPF
        Este método está preparado para quando a API estiver disponível
        """
        try:
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            # Tentar diferentes endpoints possíveis
            endpoints = [
                f'https://brasilapi.com.br/api/cpf/v1/{cpf_limpo}',
                f'https://brasilapi.com.br/api/cpf/{cpf_limpo}',
            ]
            
            for url in endpoints:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Formatar resposta da API Brasil
                        return {
                            'cpf': data.get('cpf', ''),
                            'nome': data.get('nome', ''),
                            'data_nascimento': data.get('dataNascimento', ''),
                            'situacao_cadastral': data.get('situacao', ''),
                            'endereco': {
                                'logradouro': data.get('logradouro', ''),
                                'numero': data.get('numero', ''),
                                'complemento': data.get('complemento', ''),
                                'bairro': data.get('bairro', ''),
                                'cidade': data.get('municipio', ''),
                                'estado': data.get('uf', ''),
                                'cep': data.get('cep', '')
                            }
                        }
                except requests.exceptions.RequestException:
                    continue
        except Exception as e:
            pass  # Silenciar erro, tentar outras APIs
        
        return None
    
    def consultar_multiplas_apis(self, cpf: str) -> Dict:
        """
        Consulta CPF em múltiplas APIs e consolida resultados
        """
        resultados = {
            'cpf': cpf,
            'fontes': [],
            'informacoes': {},
            'erro': None
        }
        
        # Tentar API Brasil primeiro (pública e gratuita)
        api_brasil_result = self.consultar_api_brasil(cpf)
        if api_brasil_result:
            resultados['informacoes'] = api_brasil_result
            resultados['fontes'].append({
                'nome': 'API Brasil',
                'resultado': 'Consulta realizada com sucesso',
                'tipo': 'api',
                'confiabilidade': 'alta'
            })
            return resultados
        
        # Tentar Serasa (se configurado)
        serasa_result = self.consultar_serasa(cpf)
        if serasa_result:
            resultados['informacoes'] = self._formatar_serasa(serasa_result)
            resultados['fontes'].append({
                'nome': 'Serasa',
                'resultado': 'Consulta realizada com sucesso',
                'tipo': 'api',
                'confiabilidade': 'alta'
            })
            return resultados
        
        # Tentar Quero Meus Dados (se configurado)
        qmd_result = self.consultar_queromeusdados(cpf)
        if qmd_result:
            resultados['informacoes'] = self._formatar_qmd(qmd_result)
            resultados['fontes'].append({
                'nome': 'Quero Meus Dados',
                'resultado': 'Consulta realizada com sucesso',
                'tipo': 'api',
                'confiabilidade': 'alta'
            })
            return resultados
        
        # Se nenhuma API funcionou
        resultados['erro'] = 'Nenhuma API configurada ou disponível. Configure as variáveis de ambiente.'
        return resultados
    
    def _formatar_serasa(self, data: Dict) -> Dict:
        """Formata resposta da Serasa"""
        return {
            'cpf': data.get('cpf', ''),
            'nome': data.get('nome', ''),
            'data_nascimento': data.get('dataNascimento', ''),
            'situacao_cadastral': data.get('situacao', ''),
            'endereco': data.get('endereco', {}),
            'telefone': data.get('telefone', ''),
            'email': data.get('email', '')
        }
    
    def _formatar_qmd(self, data: Dict) -> Dict:
        """Formata resposta do Quero Meus Dados"""
        return {
            'cpf': data.get('cpf', ''),
            'nome': data.get('nome', ''),
            'data_nascimento': data.get('data_nascimento', ''),
            'situacao_cadastral': data.get('situacao', ''),
            'endereco': data.get('endereco', {}),
            'telefone': data.get('telefone', ''),
            'email': data.get('email', '')
        }

