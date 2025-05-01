from config import Fore, Style
import time

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