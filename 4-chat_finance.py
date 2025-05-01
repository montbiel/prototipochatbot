import yfinance as yf
import openai
import json

client = openai.Client()

def retorna_cotacao(ticker, periodo="1mo"):
    ticker_obj = yf.Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period=periodo)["Close"]
    hist.index = hist.index.strftime("%d/%m/%Y")
    hist = round(hist, 2)

    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]

    return hist.to_json()
tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao",
            "description": "Retorna a cotação de ações da ibovespa",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "O ticker da ação. ex: BBAS3, BBDC4, etc."
                    },
                    "periodo": {
                        "type": "string",
                        "description": "O período da cotação. ex: '1d'equivale a um dia, '5d'equivale a cinco dias, '1mo'equivale a um mês, '6mo'equivale a seis meses, '1y'equivale a um ano, '5y'equivale a cinco anos, 'max'equivale a todos os dados",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"]
                    }
                }
            }
        }
    }
]

funcao_disponivel = { "retorna_cotacao": retorna_cotacao }

mensagens = [{"role": "user", "content": "Qual a cotação da ação do gerdau no período de 1 ano?"}]

resposta = client.chat.completions.create(
    messages=mensagens,
    model="gpt-3.5-turbo-0125",
    tools=tools,
    tool_choice="auto"
)

tool_calls = resposta.choices[0].message.tool_calls
#print(tool_calls)

if tool_calls:
    mensagens.append(resposta.choices[0].message)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = funcao_disponivel[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)

        mensagens.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response
        })

    segunda_resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125"
    )
    
    print(segunda_resposta.choices[0].message.content)
            
