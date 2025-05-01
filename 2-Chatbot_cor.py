import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Atribui a chave da API à variável de ambiente
api_key = os.getenv("OPENAI_API_KEY")

import openai
openai.api_key = api_key
from colorama import Fore, Style , init


client = openai.Client()
init (autoreset=True)


def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    print(f"{Fore.YELLOW}Bot:", end="")
    texto_completo = ""
    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            texto_completo += texto
    print()
    mensagens.append({"role": "assistant" , "content": texto_completo})
    return mensagens
if __name__ == "__main__":
    print("Bem vindo ao chat")
    mensagens = []
    while True:
        in_user = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
        mensagens.append({"role": "user", "content": in_user})
        mensagens = geracao_texto(mensagens)