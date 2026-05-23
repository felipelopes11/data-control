# Dashboard - Posto de Combustível

Este é um projeto desenvolvido com o objetivo de demonstrar como utilizar ferramentas modernas de visualização de dados em Python. A aplicação faz uso de Streamlit, Plotly e Pandas para criar uma interface interativa que permite a exploração de um conjunto de dados fictício sobre as vendas de um Posto de Combustível.

O estilo, os nomes das variáveis e as bibliotecas seguem a mesma estrutura do projeto `exemplo-streamlit`.

## Objetivos
- Demonstrar o uso de bibliotecas de visualização e análise de dados em Python.
- Prover uma interface gráfica interativa que permita a visualização e análise de dados filtrados sobre um posto de combustível.
- Criar 5 gráficos interativos abordando diferentes aspectos do negócio.

## Ferramentas Utilizadas
- **Python**: Linguagem de programação utilizada para manipulação de dados e lógica da aplicação.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Plotly**: Biblioteca para criar gráficos interativos.
- **Streamlit**: Framework para criar aplicativos web interativos de forma rápida e simples.

## Funcionalidades e Gráficos
- **Filtragem de dados por Frentista**: Selecione as vendas feitas por um funcionário específico.
- **Filtragem por Tipo de Pagamento**: Visualize resultados filtrados por Dinheiro, Cartão, Pix, etc.
- **Filtragem por Combustível**: Visualize apenas os tipos de combustíveis desejados (Gasolina, Etanol, Diesel).

Visualizações:
1. **Gráfico de barras**: Litros Vendidos por Combustível.
2. **Gráfico de pizza**: Valor Total por Tipo de Pagamento.
3. **Gráfico de linha**: Evolução do Valor Arrecadado ao Longo do Tempo (por dia).
4. **Gráfico de barras horizontal**: Desempenho de Vendas por Frentista (Valor Total).
5. **Gráfico de barras/colunas**: Frequência (Quantidade de Abastecimentos) por Combustível.

## Como Executar o Projeto
1. Instale as dependências necessárias:
```bash
pip install streamlit pandas plotly
```

2. Certifique-se de que o arquivo `dados_posto_combustivel.csv` esteja na mesma pasta raiz que o arquivo `main.py`.

3. Execute a aplicação utilizando o Streamlit:
```bash
streamlit run main.py
```

## Estrutura do projeto
```
posto-combustivel-streamlit
│
├── dados_posto_combustivel.csv    # Arquivo de dados CSV utilizado no projeto (Coloque-o aqui)
├── main.py                        # Script principal com a aplicação Streamlit
├── gerar_dados_teste.py           # (Opcional) Script para gerar um CSV de exemplo
└── README.md                      # Arquivo de documentação do projeto
```
