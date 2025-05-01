import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurações de cores para o terminal
from colorama import Fore, Style, init
init(autoreset=True)

# Configurações do modelo
MODEL_NAME = "gpt-3.5-turbo-0125"
MAX_TOKENS = 1000
TEMPERATURE = 0 