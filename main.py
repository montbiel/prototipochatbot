import openai
from config import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE, Fore, Style
from boleto_handler import processar_consulta_boletos, processar_resposta_boleto
from reparcelamento_handler import (
    processar_reparcelamento,
    processar_quantidade_parcelas,
    processar_confirmacao_reparcelamento,
    processar_ajuste_reparcelamento
)
from database import armazenar_previsao, gerar_numero_boletos, calcular_valor_total
from utils import normalizar_resposta, simular_transferencia
from intent_handler import detectar_intencao_reparcelamento, detectar_voltar_menu
import time
from datetime import datetime, timedelta

# Configuração do cliente OpenAI
client = openai.Client(api_key=OPENAI_API_KEY)

def mostrar_menu_principal():
    print(f"\n{Fore.CYAN}Menu Principal{Style.RESET_ALL}")
    print("Por favor, escolha uma das opções abaixo:")
    print(f"{Fore.YELLOW}1 - Boleto")
    print(f"{Fore.YELLOW}2 - Financeiro")
    print(f"{Fore.YELLOW}3 - Falar com humano")
    print(f"{Fore.YELLOW}0 - Sair{Style.RESET_ALL}")

def mostrar_menu_boleto():
    print(f"\n{Fore.CYAN}Menu de Boletos{Style.RESET_ALL}")
    print("Por favor, escolha uma das opções abaixo:")
    print(f"{Fore.YELLOW}1 - Consultar boletos em aberto")
    print(f"{Fore.YELLOW}2 - Solicitar reparcelamento")
    print(f"{Fore.YELLOW}0 - Voltar ao menu principal{Style.RESET_ALL}")

def processar_previsao_pagamento(resposta):
    resposta = normalizar_resposta(resposta)
    if resposta == "sim":
        return "Ótimo! Qual seria a data prevista para o pagamento? (Por favor, informe no formato DD/MM/AAAA)"
    elif resposta == "nao" or resposta == "não":
        return "Entendido. Compreendemos sua situação. Se precisar de ajuda no futuro, estaremos à disposição. " \
               "Por favor, entre em contato conosco quando possível. Tenha um bom dia!"
    else:
        return "Por favor, responda apenas com 'sim' ou 'nao'."

def processar_data_previsao(data):
    if armazenar_previsao(data):
        return f"Previsão de pagamento para o dia {data} registrada com sucesso! " \
               "Agradecemos a informação. Se precisar de mais alguma coisa, estaremos à disposição. Tenha um bom dia!"
    else:
        return "Desculpe, não consegui entender a data. Por favor, tente novamente no formato DD/MM/AAAA."

def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
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

def processar_opcao(opcao):
    if opcao == "1":
        mostrar_menu_boleto()
        return None, None, "boleto"
    elif opcao == "2":
        return "Você escolheu a opção de Financeiro. Como posso ajudar com questões financeiras?", None, "principal"
    elif opcao == "3":
        mensagem_inicial = "Conectando você com um de nossos atendentes...\n\nOlá! Sou o assistente virtual do IBFT. Como posso ajudar com suas questões financeiras hoje?"
        mensagens = [{"role": "system", "content": "Você é um atendente virtual de um banco, ajudando um cliente com questões financeiras. Seja cordial e profissional."}]
        mensagens.append({"role": "assistant", "content": mensagem_inicial})
        return mensagem_inicial, None, "humano"
    elif opcao == "0":
        print(f"{Fore.CYAN}O financeiro agradece seu contato, Até logo!{Style.RESET_ALL}")
        exit()
    else:
        return "Opção inválida. Por favor, escolha uma das opções disponíveis (1, 2 ou 3).", None, "principal"

def processar_opcao_menu_boleto(opcao):
    if opcao == "1":
        mensagem, valor_total, contexto = processar_consulta_boletos()
        return mensagem, valor_total, "consulta_boletos"
    elif opcao == "2":
        # Consulta os boletos antes de oferecer reparcelamento
        numero_boletos = gerar_numero_boletos()
        valor_total, boletos = calcular_valor_total(numero_boletos)
        
        if numero_boletos == 1:
            mensagem = f"Você tem apenas 1 boleto em aberto no valor de R$ {valor_total:.2f}. Não é possível realizar o reparcelamento para um único boleto. Deseja receber este boleto atualizado? (sim/não)"
            return mensagem, valor_total, "consulta_boletos"
        else:
            mensagem = f"Você tem {numero_boletos} boletos em aberto, totalizando R$ {valor_total:.2f}.\n\nÓtimo! Vamos encontrar a melhor solução para você. Qual número de parcelas seria mais adequado para sua situação? (Por favor, informe um número entre 2 e 12)"
            return mensagem, valor_total, "reparcelamento"
    elif opcao == "0":
        mostrar_menu_principal()
        return None, None, "principal"
    else:
        return "Opção inválida. Por favor, escolha uma das opções disponíveis.", None, "boleto"

if __name__ == "__main__":
    print(f"{Fore.CYAN}Bem-vindo ao Chat de Atendimento Financeiro{Style.RESET_ALL}")
    mostrar_menu_principal()
    
    mensagens = []
    valor_total_boletos = None
    estado_atual = "principal"
    ultima_mensagem = ""  # Adicionando variável para armazenar a última mensagem
    
    while True:
        in_user = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
        
        # Verifica se o usuário quer voltar ao menu
        if detectar_voltar_menu(in_user):
            if estado_atual != "principal":
                mostrar_menu_principal()
                estado_atual = "principal"
                continue
            else:
                mostrar_menu_principal()
                continue
        
        # Verifica se o usuário quer reparcelamento em qualquer parte da conversa
        if detectar_intencao_reparcelamento(in_user):
            if estado_atual == "principal":
                mostrar_menu_boleto()
                estado_atual = "boleto"
                continue
            else:
                # Consulta os boletos antes de oferecer reparcelamento
                numero_boletos = gerar_numero_boletos()
                valor_total, boletos = calcular_valor_total(numero_boletos)
                
                if numero_boletos == 1:
                    resposta = f"Você tem apenas 1 boleto em aberto no valor de R$ {valor_total:.2f}. Não é possível realizar o reparcelamento para um único boleto. Deseja receber este boleto atualizado? (sim/não)"
                    print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                    ultima_mensagem = resposta
                    estado_atual = "consulta_boletos"
                else:
                    resposta = f"Você tem {numero_boletos} boletos em aberto, totalizando R$ {valor_total:.2f}.\n\nÓtimo! Vamos encontrar a melhor solução para você. Qual número de parcelas seria mais adequado para sua situação? (Por favor, informe um número entre 2 e 12)"
                    print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                    ultima_mensagem = resposta
                    estado_atual = "reparcelamento"
                    valor_total_boletos = valor_total
                continue
        
        # Se estiver no menu principal
        if estado_atual == "principal":
            resposta, valor_total_boletos, novo_estado = processar_opcao(in_user)
            estado_atual = novo_estado
            if resposta:
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
                if estado_atual == "humano":
                    mensagens = [{"role": "system", "content": "Você é um atendente humano de um banco, ajudando um cliente com questões financeiras."}]
                    mensagens.append({"role": "assistant", "content": resposta})
            continue
        
        # Se estiver no estado de consulta de boletos
        if estado_atual == "consulta_boletos":
            if "Deseja conhecer as condições especiais de reparcelamento" in ultima_mensagem:
                resposta = processar_resposta_boleto(in_user, "reparcelamento")
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
                if "Qual número de parcelas seria mais adequado" in resposta:
                    estado_atual = "reparcelamento"
                elif "Gostaria de receber os boletos atualizados" in resposta:
                    estado_atual = "consulta_boletos"  # Mantém no mesmo estado para processar a próxima resposta
            elif "Gostaria de receber os boletos atualizados" in ultima_mensagem:
                resposta = processar_resposta_boleto(in_user, "boleto")
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
                if "Você tem alguma previsão" in resposta:
                    estado_atual = "previsao"
                elif "Posso ajudar com mais alguma coisa" in resposta:
                    mostrar_menu_boleto()
                    estado_atual = "boleto"
            continue
        
        # Se estiver no estado de previsão
        if estado_atual == "previsao":
            resposta = processar_resposta_boleto(in_user, "previsao")
            print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
            ultima_mensagem = resposta
            if "Qual seria a data prevista" in resposta:
                data = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
                resposta = processar_data_previsao(data)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
                mostrar_menu_boleto()
                estado_atual = "boleto"
            elif "Tenha um bom dia" in resposta:
                print(f"{Fore.CYAN}O financeiro agradece seu contato, Até logo!{Style.RESET_ALL}")
                exit()
            continue
        
        # Se estiver no estado de reparcelamento
        if estado_atual == "reparcelamento":
            if "Qual número de parcelas seria mais adequado" in ultima_mensagem:
                resposta = processar_quantidade_parcelas(in_user, valor_total_boletos)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
            elif "Você concorda com essas condições" in ultima_mensagem:
                resposta = processar_confirmacao_reparcelamento(in_user)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
                if "Posso ajudar com mais alguma coisa" in resposta:
                    # Inicia o timer para fechar o programa
                    tempo_inicio = datetime.now()
                    while True:
                        try:
                            # Aguarda 60 segundos por uma resposta
                            in_user = input(f"{Fore.GREEN}user:{Style.RESET_ALL}")
                            if normalizar_resposta(in_user) == "nao" or normalizar_resposta(in_user) == "não":
                                print(f"{Fore.CYAN}Obrigado por utilizar nosso serviço. Até logo!{Style.RESET_ALL}")
                                exit()
                            else:
                                print(f"{Fore.YELLOW}Bot: Desculpe, não entendi. Por favor, responda apenas com 'sim' ou 'nao'.{Style.RESET_ALL}")
                                continue
                        except KeyboardInterrupt:
                            print(f"{Fore.CYAN}Obrigado por utilizar nosso serviço. Até logo!{Style.RESET_ALL}")
                            exit()
                        
                        # Verifica se passou 1 minuto
                        if (datetime.now() - tempo_inicio).total_seconds() >= 60:
                            print(f"{Fore.CYAN}Obrigado por utilizar nosso serviço. Até logo!{Style.RESET_ALL}")
                            exit()
            elif "O que não ficou bom na oferta" in ultima_mensagem:
                resposta = processar_ajuste_reparcelamento(in_user)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
            elif "Quantas parcelas você gostaria" in ultima_mensagem:
                resposta = processar_quantidade_parcelas(in_user, valor_total_boletos)
                print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                ultima_mensagem = resposta
            continue
        
        # Se estiver no estado de falar com humano (ChatGPT)
        if estado_atual == "humano":
            if not mensagens:  # Se for a primeira interação
                mensagens = [{"role": "system", "content": "Você é um atendente virtual de um banco, ajudando um cliente com questões financeiras. Seja cordial e profissional."}]
                mensagem_inicial = "Olá! Sou o assistente virtual do banco. Como posso ajudar com suas questões financeiras hoje?"
                mensagens.append({"role": "assistant", "content": mensagem_inicial})
                print(f"{Fore.YELLOW}Bot: {mensagem_inicial}{Style.RESET_ALL}")
                continue
            
            mensagens.append({"role": "user", "content": in_user})
            mensagens = geracao_texto(mensagens)
            ultima_mensagem = mensagens[-1]["content"]
            continue
        
        # Se estiver no menu de boletos
        if estado_atual == "boleto":
            if in_user in ["1", "2", "0"]:  # Verifica se é uma opção válida do menu
                resposta, valor_total_boletos, novo_estado = processar_opcao_menu_boleto(in_user)
                estado_atual = novo_estado
                if resposta:
                    print(f"{Fore.YELLOW}Bot: {resposta}{Style.RESET_ALL}")
                    ultima_mensagem = resposta
            else:
                print(f"{Fore.YELLOW}Bot: Opção inválida. Por favor, escolha uma das opções disponíveis.{Style.RESET_ALL}")
            continue 