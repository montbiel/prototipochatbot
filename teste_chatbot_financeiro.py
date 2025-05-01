import os
from dotenv import load_dotenv
import random
import json
import time
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

# Atribui a chave da API à variável de ambiente
api_key = os.getenv("OPENAI_API_KEY")

import openai
openai.api_key = api_key
from colorama import Fore, Style, init

client = openai.Client()
init(autoreset=True)

# Banco de dados fictício de boletos
boletos_db = {
    "123456": {"valor": 299.70, "vencimento": "2024-04-15", "status": "aberto"},
    "789012": {"valor": 249.70, "vencimento": "2024-04-20", "status": "aberto"},
    "345678": {"valor": 99.70, "vencimento": "2024-04-25", "status": "aberto"},
    "901234": {"valor": 299.70, "vencimento": "2024-04-30", "status": "aberto"},
    "567890": {"valor": 249.70, "vencimento": "2024-05-05", "status": "aberto"}
}

# Banco de dados fictício de previsões de pagamento
previsoes_db = {}

# Variável global para armazenar o valor total dos boletos
valor_total_boletos = 0

def gerar_numero_boletos():
    return random.randint(1, 12)

def calcular_valor_total(numero_boletos):
    # Distribuição dos valores dos boletos
    valores = [299.70, 249.70, 99.70]
    # Seleciona aleatoriamente os valores dos boletos
    boletos = random.choices(valores, k=numero_boletos)
    # Calcula o valor total
    valor_total = sum(boletos)
    return valor_total, boletos

def normalizar_resposta(resposta):
    # Remove acentos e converte para minúsculas
    resposta = resposta.lower().strip()
    # Remove acentos
    resposta = resposta.replace('á', 'a').replace('à', 'a').replace('ã', 'a').replace('â', 'a')
    resposta = resposta.replace('é', 'e').replace('ê', 'e')
    resposta = resposta.replace('í', 'i').replace('î', 'i')
    resposta = resposta.replace('ó', 'o').replace('ô', 'o').replace('õ', 'o')
    resposta = resposta.replace('ú', 'u').replace('û', 'u')
    resposta = resposta.replace('ç', 'c')
    return resposta

def mostrar_beneficios_reparcelamento():
    return "Antes de decidir, gostaria de destacar os benefícios do reparcelamento:\n" \
           "✅ Redução significativa no valor das parcelas\n" \
           "✅ Evita juros e multas por atraso\n" \
           "✅ Regularização imediata da sua situação\n" \
           "✅ Flexibilidade no número de parcelas\n" \
           "✅ Sem custos adicionais\n\n" \
           "Deseja reconsiderar a proposta? (sim/nao)"

def processar_reparcelamento(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Ótima escolha! Vamos encontrar a melhor solução para você. " \
               "Qual número de parcelas seria mais adequado para sua situação? " \
               "(Por favor, informe um número entre 2 e 12)"
    elif resposta == "nao" or resposta == "não":
        resposta = mostrar_beneficios_reparcelamento()
        print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
        nova_resposta = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
        if normalizar_resposta(nova_resposta) == "sim":
            return "Ótima escolha! Vamos encontrar a melhor solução para você. " \
                   "Qual número de parcelas seria mais adequado para sua situação? " \
                   "(Por favor, informe um número entre 2 e 12)"
        else:
            return "Entendido. Você tem alguma previsão para realizar o pagamento? (sim/nao)"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def processar_quantidade_parcelas(resposta):
    try:
        parcelas = int(resposta)
        if 2 <= parcelas <= 12:
            # Usa o valor total armazenado anteriormente
            valor_parcela = valor_total_boletos / parcelas
            return f"Perfeito! Para {parcelas} parcelas, cada parcela ficaria em R$ {valor_parcela:.2f}. " \
                   "Você concorda com essas condições? (sim/nao)"
        else:
            return "Por favor, informe um número de parcelas entre 2 e 12."
    except ValueError:
        return "Por favor, informe um número válido de parcelas (entre 2 e 12)."

def processar_confirmacao_reparcelamento(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Excelente! O reparcelamento será processado e os novos boletos serão enviados para seu e-mail em até 5 minutos. " \
               "Posso ajudar com mais alguma coisa?"
    elif resposta == "nao" or resposta == "não":
        return "Entendi. O que não ficou bom na oferta?\n" \
               "1 - Valor da parcela\n" \
               "2 - Número de parcelas\n" \
               "3 - Outro motivo"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def processar_ajuste_reparcelamento(resposta):
    try:
        opcao = int(resposta)
        if opcao == 1:
            return "Entendi que o valor da parcela não está adequado. " \
                   "Podemos aumentar o número de parcelas para reduzir o valor. " \
                   "Quantas parcelas você gostaria? (entre 2 e 12)"
        elif opcao == 2:
            return "Entendi que o número de parcelas não está adequado. " \
                   "Quantas parcelas você gostaria? (entre 2 e 12)"
        elif opcao == 3:
            return "Entendi. Podemos tentar uma nova proposta com um número diferente de parcelas. " \
                   "Quantas parcelas você gostaria? (entre 2 e 12)"
        else:
            return "Por favor, escolha uma das opções (1, 2 ou 3)."
    except ValueError:
        return "Por favor, escolha uma das opções (1, 2 ou 3)."

def processar_outro_motivo(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Ótimo! Vamos tentar uma nova proposta. " \
               "Quantas parcelas você gostaria? (entre 2 e 12)"
    elif resposta == "nao" or resposta == "não":
        return "Entendido. Você tem alguma previsão para realizar o pagamento? (sim/nao)"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def processar_previsao_pagamento(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Ótimo! Qual seria a data prevista para o pagamento? (Por favor, informe no formato DD/MM/AAAA)"
    elif resposta == "nao" or resposta == "não":
        return "Entendido. Compreendemos sua situação. Se precisar de ajuda no futuro, estaremos à disposição. " \
               "Por favor, entre em contato conosco quando possível. Tenha um bom dia!"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def armazenar_previsao(data):
    try:
        # Verifica se a data está no formato correto
        dia, mes, ano = map(int, data.split('/'))
        # Armazena a previsão no banco de dados fictício
        previsoes_db[data] = {
            "status": "pendente",
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        return True
    except:
        return False

def processar_data_previsao(data):
    if armazenar_previsao(data):
        return f"Previsão de pagamento para o dia {data} registrada com sucesso! " \
               "Agradecemos a informação. Se precisar de mais alguma coisa, estaremos à disposição. Tenha um bom dia!"
    else:
        return "Desculpe, não consegui entender a data. Por favor, tente novamente no formato DD/MM/AAAA."

def processar_resposta_boleto(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Perfeito! Vou gerar o(s) boleto(s) para você. " \
               "Os boletos serão enviados para o e-mail cadastrado em até 5 minutos. " \
               "Posso ajudar com mais alguma coisa?"
    elif resposta == "nao" or resposta == "não":
        resposta = "Antes de decidir, gostaria de destacar os benefícios do pagamento imediato:\n" \
                  "✅ Evita juros e multas por atraso\n" \
                  "✅ Regularização imediata da sua situação\n" \
                  "✅ Mantém seu histórico de pagamentos em dia\n\n" \
                  "Deseja reconsiderar? (sim/nao)"
        print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
        nova_resposta = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
        if normalizar_resposta(nova_resposta) == "sim":
            return "Perfeito! Vou gerar o(s) boleto(s) para você. " \
                   "Os boletos serão enviados para o e-mail cadastrado em até 5 minutos. " \
                   "Posso ajudar com mais alguma coisa?"
        else:
            return "Entendido. Você tem alguma previsão para realizar o pagamento? (sim/nao)"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def simular_transferencia():
    print(f"\n{Fore.YELLOW}Bot: Iniciando transferência para atendente humano...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Bot: Aguarde um momento enquanto conectamos você com um de nossos especialistas.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Bot: .{Style.RESET_ALL}", end="", flush=True)
    time.sleep(1)
    print(f"{Fore.YELLOW}.{Style.RESET_ALL}", end="", flush=True)
    time.sleep(1)
    print(f"{Fore.YELLOW}.{Style.RESET_ALL}")
    time.sleep(1)
    print(f"{Fore.YELLOW}Bot: Transferência concluída com sucesso!{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Atendente: Olá! Meu nome é Gabriel. Como posso ajudar você hoje?{Style.RESET_ALL}")
    exit()

def processar_opcao(opcao):
    if opcao == "1":
        numero_boletos = gerar_numero_boletos()
        valor_total, boletos = calcular_valor_total(numero_boletos)
        
        if numero_boletos == 1:
            mensagem = f"Você tem 1 boleto em aberto no valor de R$ {valor_total:.2f}. " \
                      "Gostaria de receber o boleto atualizado? (sim/nao)"
        else:
            mensagem = f"Você tem {numero_boletos} boleto(s) em aberto, totalizando R$ {valor_total:.2f}."
            
            if numero_boletos > 1:
                mensagem += f"\n\nPara ajudar na regularização da sua situação, temos uma excelente oportunidade de reparcelamento! "
                mensagem += "Com o reparcelamento, você pode:\n"
                mensagem += "✅ Reduzir o valor das parcelas\n"
                mensagem += "✅ Evitar juros e multas\n"
                mensagem += "✅ Regularizar sua situação de forma mais tranquila\n\n"
                mensagem += "Deseja conhecer as condições especiais de reparcelamento? (sim/não)"
        
        # Armazena o valor total para uso posterior
        global valor_total_boletos
        valor_total_boletos = valor_total
        
        return mensagem
    elif opcao == "2":
        return "Você escolheu a opção de Financeiro. Como posso ajudar com questões financeiras?"
    elif opcao == "3":
        simular_transferencia()
    else:
        return "Opção inválida. Por favor, escolha uma das opções disponíveis (1, 2 ou 3)."

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
    mensagens.append({"role": "assistant", "content": texto_completo})
    return mensagens

if __name__ == "__main__":
    print(f"{Fore.CYAN}Bem-vindo ao Chat de Atendimento Financeiro{Style.RESET_ALL}")
    print("\nPor favor, escolha uma das opções abaixo:")
    print(f"{Fore.YELLOW}1 - Boleto")
    print(f"{Fore.YELLOW}2 - Financeiro")
    print(f"{Fore.YELLOW}3 - Falar com humano{Style.RESET_ALL}")
    
    mensagens = []
    while True:
        in_user = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
        
        # Se for a primeira mensagem, processa como opção do menu
        if not mensagens:
            resposta = processar_opcao(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
            continue
        
        # Verifica o contexto da última mensagem do bot
        ultima_mensagem = mensagens[-1]["content"]
        
        if "Gostaria de receber o boleto atualizado" in ultima_mensagem:
            resposta = processar_resposta_boleto(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "Deseja conhecer as condições especiais de reparcelamento" in ultima_mensagem:
            resposta = processar_reparcelamento(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "Qual número de parcelas seria mais adequado" in ultima_mensagem:
            resposta = processar_quantidade_parcelas(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "Você concorda com essas condições" in ultima_mensagem:
            resposta = processar_confirmacao_reparcelamento(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "O que não ficou bom na oferta" in ultima_mensagem:
            resposta = processar_ajuste_reparcelamento(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "Gostaria de receber o(s) boleto(s) para pagamento" in ultima_mensagem:
            resposta = processar_resposta_boleto(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
        elif "Você tem alguma previsão para realizar o pagamento" in ultima_mensagem:
            resposta = processar_previsao_pagamento(in_user)
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            mensagens.append({"role": "assistant", "content": resposta})
            if "Qual seria a data prevista" in resposta:
                data = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
                resposta = processar_data_previsao(data)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                mensagens.append({"role": "assistant", "content": resposta})
        else:
            mensagens.append({"role": "user", "content": in_user})
            mensagens = geracao_texto(mensagens)