# Chatbot Financeiro

Um chatbot inteligente para atendimento financeiro, capaz de lidar com boletos, reparcelamentos e previsões de pagamento.

## Funcionalidades

### Menu Principal
- Boleto
- Financeiro
- Falar com humano
- Sair

### Menu de Boletos
- Consultar boletos em aberto
- Solicitar reparcelamento
- Voltar ao menu principal

### Processamento de Boletos
- Consulta de boletos em aberto
- Visualização de boletos
- Geração de novos boletos
- Registro de previsão de pagamento

### Reparcelamento
- Simulação de novas condições
- Ajuste de número de parcelas (1-12)
- Confirmação de condições
- Ajuste de propostas
- Geração de novos boletos após confirmação

### Atendimento Personalizado
- Detecção de intenção de reparcelamento
- Detecção de intenção de voltar ao menu
- Respostas personalizadas baseadas em IA
- Transferência para atendente humano

## Requisitos

- Python 3.8 ou superior
- Conta na OpenAI com API key
- Banco de dados SQLite

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto com sua API key:
```
OPENAI_API_KEY=sua_chave_api_aqui
```

## Uso

Execute o chatbot:
```bash
python main.py
```

## Estrutura do Projeto

- `main.py`: Arquivo principal que orquestra o chatbot e gerencia o fluxo de estados
- `config.py`: Configurações e variáveis de ambiente
- `database.py`: Banco de dados e funções relacionadas
- `utils.py`: Funções utilitárias e normalização de respostas
- `boleto_handler.py`: Lógica de processamento de boletos
- `reparcelamento_handler.py`: Lógica de reparcelamento
- `intent_handler.py`: Detecção de intenções do usuário

## Estados do Chatbot

O chatbot opera em diferentes estados para melhor gerenciamento do fluxo:
- `principal`: Menu principal
- `boleto`: Menu de boletos
- `consulta_boletos`: Consulta e visualização de boletos
- `reparcelamento`: Processo de reparcelamento
- `humano`: Atendimento com humano
