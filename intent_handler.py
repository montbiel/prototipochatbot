from utils import normalizar_resposta

def detectar_intencao_reparcelamento(texto):
    texto = normalizar_resposta(texto)
    palavras_chave = [
        "reparcelar",
        "parcelar",
        "dividir",
        "parcela",
        "parcelas",
        "renegociar",
        "negociar",
        "renegociação",
        "negociação",
        "quero parcelar",
        "quero reparcelar",
        "quero dividir",
        "quero negociar"
    ]
    
    for palavra in palavras_chave:
        if palavra in texto:
            return True
    return False

def detectar_voltar_menu(texto):
    texto = normalizar_resposta(texto)
    opcoes_voltar = [
        "voltar",
        "menu",
        "menu principal",
        "menu anterior",
        "voltar ao menu",
        "voltar para o menu",
        "voltar ao menu principal",
        "voltar para o menu principal",
        "voltar ao menu anterior",
        "voltar para o menu anterior"
    ]
    
    for opcao in opcoes_voltar:
        if opcao in texto:
            return True
    return False 