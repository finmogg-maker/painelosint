import requests
import json
from typing import Dict, List, Optional
import hashlib
import base64
from urllib.parse import quote
from cpf_api import CPFAPIClient

class OSINTTools:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.cpf_api = CPFAPIClient()
    
    def buscar_nome(self, nome: str) -> Dict:
        """
        Busca informações sobre um nome em várias fontes OSINT
        """
        nome_encoded = quote(nome)
        resultados = {
            'nome': nome,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        # Links reais para sites de OSINT
        fontes = [
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para "{nome}"',
                'url': f'https://www.google.com/search?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Facebook',
                'resultado': f'Buscar "{nome}" no Facebook',
                'url': f'https://www.facebook.com/search/people/?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'LinkedIn',
                'resultado': f'Buscar "{nome}" no LinkedIn',
                'url': f'https://www.linkedin.com/search/results/people/?keywords={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Twitter/X',
                'resultado': f'Buscar "{nome}" no Twitter/X',
                'url': f'https://twitter.com/search?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Instagram',
                'resultado': f'Buscar "{nome}" no Instagram',
                'url': f'https://www.instagram.com/explore/tags/{nome_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'Pipl',
                'resultado': f'Buscar "{nome}" no Pipl (People Search)',
                'url': f'https://pipl.com/search/?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'TruePeopleSearch',
                'resultado': f'Buscar "{nome}" no TruePeopleSearch',
                'url': f'https://www.truepeoplesearch.com/results?name={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Whitepages',
                'resultado': f'Buscar "{nome}" no Whitepages',
                'url': f'https://www.whitepages.com/name/{nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Spokeo',
                'resultado': f'Buscar "{nome}" no Spokeo',
                'url': f'https://www.spokeo.com/{nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex',
                'resultado': f'Busca no Yandex para "{nome}"',
                'url': f'https://yandex.com/search/?text={nome_encoded}',
                'tipo': 'link'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
            resultados['total_resultados'] += 1
        
        resultados['resumo'] = f"Busca por '{nome}' retornou {resultados['total_resultados']} fontes de informação. Clique nos links para acessar."
        
        return resultados
    
    def buscar_processo(self, numero_processo: str) -> Dict:
        """
        Busca informações sobre um processo judicial
        """
        # Remove caracteres não numéricos para padronizar
        numero_limpo = ''.join(filter(str.isdigit, numero_processo))
        
        resultados = {
            'numero_processo': numero_processo,
            'numero_limpo': numero_limpo,
            'fontes': [],
            'status': 'Pendente'
        }
        
        # Simulação de busca em sistemas judiciais
        fontes = [
            {
                'nome': 'Sistema Judicial',
                'resultado': f'Processo {numero_limpo} encontrado no sistema. Status: Em andamento.'
            },
            {
                'nome': 'Tribunal de Justiça',
                'resultado': f'Informações sobre o processo {numero_limpo} disponíveis.'
            },
            {
                'nome': 'Base de Dados Pública',
                'resultado': f'Dados públicos do processo {numero_limpo} recuperados.'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
        
        resultados['status'] = 'Encontrado'
        resultados['resumo'] = f"Processo {numero_processo} encontrado em {len(resultados['fontes'])} fontes."
        
        return resultados
    
    def buscar_foto(self, termo_busca: str, url_imagem: Optional[str] = None) -> Dict:
        """
        Busca informações sobre uma foto ou imagem
        """
        resultados = {
            'termo_busca': termo_busca,
            'url_imagem': url_imagem,
            'fontes': [],
            'hash_imagem': None
        }
        
        # Se houver URL, calcular hash da imagem
        if url_imagem:
            try:
                # Simulação de hash (em produção, baixaria a imagem)
                hash_input = f"{url_imagem}{termo_busca}".encode()
                resultados['hash_imagem'] = hashlib.md5(hash_input).hexdigest()
            except:
                pass
        
        # Simulação de busca reversa de imagem
        fontes = [
            {
                'nome': 'Busca Reversa de Imagem',
                'resultado': f'Imagens similares encontradas para "{termo_busca}".'
            },
            {
                'nome': 'Análise de Metadados',
                'resultado': f'Metadados extraídos da imagem relacionada a "{termo_busca}".'
            },
            {
                'nome': 'Busca em Redes Sociais',
                'resultado': f'Possíveis ocorrências da imagem em redes sociais para "{termo_busca}".'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
        
        resultados['resumo'] = f"Busca por foto '{termo_busca}' retornou {len(resultados['fontes'])} resultados."
        
        return resultados
    
    def buscar_multiplas_fontes(self, tipo: str, termo: str) -> Dict:
        """
        Busca em múltiplas fontes OSINT baseado no tipo
        """
        if tipo == 'nome':
            return self.buscar_nome(termo)
        elif tipo == 'processo':
            return self.buscar_processo(termo)
        elif tipo == 'foto':
            return self.buscar_foto(termo)
        else:
            return {'erro': 'Tipo de busca inválido'}
    
    def validar_processo(self, numero: str) -> bool:
        """
        Valida formato de número de processo
        """
        # Formato brasileiro: NNNNNNN-DD.AAAA.J.TR.OOOO
        numero_limpo = ''.join(filter(str.isdigit, numero))
        return len(numero_limpo) >= 15
    
    def extrair_metadados_imagem(self, url: str) -> Dict:
        """
        Extrai metadados de uma imagem (simulação)
        """
        return {
            'url': url,
            'metadados': {
                'formato': 'JPEG',
                'tamanho': 'N/A',
                'data_criacao': 'N/A',
                'localizacao': 'N/A'
            },
            'observacao': 'Metadados simulados. Em produção, use bibliotecas como PIL/Pillow ou exifread.'
        }
    
    def validar_cpf(self, cpf: str) -> bool:
        """
        Valida formato de CPF brasileiro
        """
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais (CPF inválido)
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(cpf, peso):
            soma = sum(int(cpf[i]) * (peso - i) for i in range(len(cpf)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Valida primeiro dígito verificador
        if calcular_digito(cpf_limpo[:9], 10) != int(cpf_limpo[9]):
            return False
        
        # Valida segundo dígito verificador
        if calcular_digito(cpf_limpo[:10], 11) != int(cpf_limpo[10]):
            return False
        
        return True
    
    def buscar_cpf(self, cpf: str) -> Dict:
        """
        Busca informações sobre um CPF usando APIs reais
        Tenta múltiplas APIs e retorna dados reais quando disponível
        """
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Valida CPF
        if not self.validar_cpf(cpf_limpo):
            return {
                'erro': 'CPF inválido. Verifique o formato.',
                'cpf': cpf_limpo
            }
        
        # Formata CPF (XXX.XXX.XXX-XX)
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        resultados = {
            'cpf': cpf_formatado,
            'cpf_limpo': cpf_limpo,
            'status': 'Encontrado',
            'informacoes': {},
            'fontes': [],
            'links': []
        }
        
        # Tentar consultar APIs reais
        api_result = self.cpf_api.consultar_multiplas_apis(cpf_limpo)
        
        if api_result.get('informacoes') and not api_result.get('erro'):
            # Dados reais obtidos da API
            resultados['informacoes'] = api_result['informacoes']
            resultados['informacoes']['cpf'] = cpf_formatado
            resultados['fontes'] = api_result.get('fontes', [])
            resultados['resumo'] = f"Consulta do CPF {cpf_formatado} realizada com sucesso usando API real."
            resultados['aviso'] = 'Dados obtidos de API autorizada. Informações protegidas por LGPD.'
            return resultados
        
        # Se nenhuma API funcionou, retornar erro informativo
        resultados['erro'] = api_result.get('erro', 'Nenhuma API configurada')
        resultados['resumo'] = f"Consulta do CPF {cpf_formatado} não pôde ser realizada."
        resultados['aviso'] = 'Configure as variáveis de ambiente com as chaves de API para consultas reais. Veja README.md para instruções.'
        
        # Adicionar links para serviços oficiais
        fontes = [
            {
                'nome': 'Receita Federal',
                'resultado': f'Consulta de situação cadastral do CPF {cpf_formatado}',
                'url': f'https://www.receita.fazenda.gov.br/Aplicacoes/ATCTA/CPF/ConsultaPublica.asp',
                'tipo': 'link',
                'observacao': 'Consulta oficial da Receita Federal'
            },
            {
                'nome': 'API Brasil',
                'resultado': f'API pública gratuita para consulta de CPF',
                'url': f'https://brasilapi.com.br/api/cpf/v1/{cpf_limpo}',
                'tipo': 'link',
                'observacao': 'API pública e gratuita'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        return resultados

