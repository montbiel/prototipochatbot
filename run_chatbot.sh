#!/bin/bash

# Navega para o diretório do projeto
cd "$(dirname "$0")"

# Ativa o ambiente virtual
source .venv/bin/activate

# Executa o chatbot
python3 2-Chatbot_cor.py 