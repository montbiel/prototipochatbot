from utils import normalizar_resposta, mostrar_beneficios_reparcelamento
from config import Fore, Style

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

def processar_quantidade_parcelas(mensagem, valor_total):
    """Processa a quantidade de parcelas escolhida pelo usuário e faz uma nova simulação"""
    try:
        # Extrai o número de parcelas da mensagem
        parcelas = int(mensagem)
        
        # Valida o número de parcelas
        if parcelas < 1 or parcelas > 12:
            return "Desculpe, o número de parcelas deve estar entre 1 e 12. Por favor, escolha um número válido."
        
        # Calcula o valor da parcela
        valor_parcela = valor_total / parcelas
        
        # Formata a mensagem com a nova simulação
        mensagem = f"""
        Nova simulação de reparcelamento:
        
        Valor total: R$ {valor_total:.2f}
        Número de parcelas: {parcelas}
        Valor de cada parcela: R$ {valor_parcela:.2f}
        
        Você concorda com essas condições?
        """
        
        return mensagem
        
    except ValueError:
        return "Desculpe, não entendi o número de parcelas. Por favor, digite apenas o número (por exemplo: 6)."

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