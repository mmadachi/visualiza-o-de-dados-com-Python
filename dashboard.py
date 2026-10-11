import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 1. Carregar os dados (Criando dados de exemplo para o código rodar)
data = {
    'Ano': [2018, 2019, 2020, 2021, 2022, 2018, 2019, 2020, 2021, 2022],
    'Vendas_Automoveis': [5000, 4800, 3000, 3500, 4000, 2000, 1800, 1000, 1200, 1500],
    'Gastos_Publicidade': [1000, 1100, 800, 900, 950, 500, 450, 300, 350, 400],
    'Tipo_Veiculo': ['Sedan', 'Sedan', 'Sedan', 'Sedan', 'Sedan', 'SUV', 'SUV', 'SUV', 'SUV', 'SUV'],
    'Recessao': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    'PIB': [2.0, 2.1, -1.0, -0.5, 1.0, 2.0, 2.1, -1.0, -0.5, 1.0]
}
df = pd.DataFrame(data)

# 2. Inicializar o App Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Análise de Vendas XYZ Automotives"

# 3. Definir o Layout do App
app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1("Análise de Impacto da Recessão nas Vendas", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Selecione o Tipo de Estatística:"),
        dcc.Dropdown(
            id='dropdown-estatistica',
            options=[
                {'label': 'Estatísticas do Período de Recessão', 'value': 'recessao'},
                {'label': 'Estatísticas do Relatório Anual', 'value': 'anual'}
            ],
            value='recessao',
            clearable=False
        )
    ], style={'width': '50%', 'margin': '0 auto', 'paddingBottom': '20px'}),
    
    html.Div(id='container-graficos')
])

# 4. Criar a Função de Callback
@app.callback(
    Output('container-graficos', 'children'),
    Input('dropdown-estatistica', 'value')
)
def atualizar_graficos(tipo_estatistica):
    
    if tipo_estatistica == 'recessao':
        df_filtrado = df[df['Recessao'] == 1]
        fig1 = px.bar(df_filtrado, x='Tipo_Veiculo', y='Vendas_Automoveis', title='Vendas por Tipo de Veículo durante a Recessão')
        fig2 = px.line(df_filtrado, x='Ano', y='Gastos_Publicidade', title='Gastos com Publicidade na Recessão')
        return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]
        
    elif tipo_estatistica == 'anual':
        fig1 = px.line(df, x='Ano', y='Vendas_Automoveis', color='Tipo_Veiculo', title='Vendas Anuais por Tipo de Veículo')
        fig2 = px.scatter(df, x='Ano', y='PIB', title='Variação do PIB Anual')
        return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

# 5. Executar o App
if __name__ == '__main__':
    app.run(debug=True)