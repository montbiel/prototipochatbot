import random
from datetime import datetime

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