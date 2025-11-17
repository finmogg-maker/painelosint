#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização da Ferramenta OSINT
Python 3.x
"""

import sys
import os

# Verificar versão do Python
if sys.version_info < (3, 6):
    print("❌ Erro: Python 3.6 ou superior é necessário!")
    print(f"Versão atual: {sys.version}")
    sys.exit(1)

print("=" * 60)
print("🔍 FERRAMENTA OSINT - Inicializando...")
print("=" * 60)
print(f"Python {sys.version.split()[0]}")
print()

# Verificar se as dependências estão instaladas
try:
    import flask
    print("✅ Flask instalado")
except ImportError:
    print("❌ Flask não encontrado!")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

try:
    import requests
    print("✅ Requests instalado")
except ImportError:
    print("❌ Requests não encontrado!")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

print()
print("=" * 60)
print("🚀 Iniciando servidor...")
print("=" * 60)
print("📱 Acesse: http://localhost:5000")
print("⏹️  Para parar, pressione Ctrl+C")
print("=" * 60)
print()

# Importar e executar o app
try:
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)
except KeyboardInterrupt:
    print("\n\n⏹️  Servidor interrompido pelo usuário.")
except Exception as e:
    print(f"\n❌ Erro ao iniciar servidor: {e}")
    sys.exit(1)

