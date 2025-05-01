from database import gerar_numero_boletos, calcular_valor_total
from utils import normalizar_resposta
from config import Fore, Style

def processar_resposta_boleto(resposta, contexto="boleto"):
    resposta = normalizar_resposta(resposta)
    
    if contexto == "reparcelamento":
        if resposta == "sim":
            return "Perfeito! Vou encaminhar você para o reparcelamento. " \
                   "Qual número de parcelas seria mais adequado para sua situação? " \
                   "(Por favor, informe um número entre 2 e 12)"
        elif resposta == "nao" or resposta == "não":
            return "Entendido. Gostaria de receber os boletos atualizados? (sim/nao)"
        else:
            return "Por favor, responda apenas com 'sim' ou 'nao'."
    
    elif contexto == "boleto":
        if resposta == "sim":
            return "Perfeito! Vou gerar o(s) boleto(s) para você. " \
                   "Os boletos serão enviados para o e-mail cadastrado em até 5 minutos. " \
                   "Posso ajudar com mais alguma coisa?"
        elif resposta == "nao" or resposta == "não":
            return "Entendido. Você tem alguma previsão para realizar o pagamento? (sim/nao)"
        else:
            return "Por favor, responda apenas com 'sim' ou 'nao'."
    
    elif contexto == "previsao":
        if resposta == "sim":
            return "Ótimo! Qual seria a data prevista para o pagamento? (Por favor, informe no formato DD/MM/AAAA)"
        elif resposta == "nao" or resposta == "não":
            return "Entendido. Compreendemos sua situação. Se precisar de ajuda no futuro, estaremos à disposição. " \
                   "Por favor, entre em contato conosco quando possível. Tenha um bom dia!"
        else:
            return "Por favor, responda apenas com 'sim' ou 'nao'."

def processar_consulta_boletos():
    numero_boletos = gerar_numero_boletos()
    valor_total, boletos = calcular_valor_total(numero_boletos)
    
    if numero_boletos == 1:
        mensagem = f"Você tem 1 boleto em aberto no valor de R$ {valor_total:.2f}.\n\n"
    else:
        mensagem = f"Você tem {numero_boletos} boleto(s) em aberto, totalizando R$ {valor_total:.2f}.\n\n"
    
    # Adiciona a oferta de reparcelamento
    mensagem += "Para ajudar na regularização da sua situação, temos uma excelente oportunidade de reparcelamento! " \
                "Com o reparcelamento, você pode:\n" \
                "✅ Reduzir o valor das parcelas\n" \
                "✅ Evitar juros e multas\n" \
                "✅ Regularizar sua situação de forma mais tranquila\n\n" \
                "Deseja conhecer as condições especiais de reparcelamento? (sim/não)"
    
    return mensagem, valor_total, "reparcelamento" 