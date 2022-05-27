from prophet import Prophet
from prophet.plot import plot_components_plotly, plot_plotly


# Definindo classe de plotagem.
class Plots:

    # Método construtor que recebe os dados e inicializa os gráficos como nulos.
    def __init__(self, dados):
        self.dados = dados
        self.graficos = None

    # Treina um modelo sazonal e gera os gráficos interativos associados.
    def gerarCurvaSazonalidade(self):

        # Instanciando e treinando modelo sazonal com os dados.
        modelo = Prophet(changepoint_range=1).fit(self.dados)

        # Fazendo previsão nula. Essa etapa é feita apenas para permitir o uso das funções
        # de plotagem interativa, na prática não estamos fazendo nenhuma previsão.
        futuro = modelo.make_future_dataframe(periods=0)
        previsao = modelo.predict(futuro)

        # Recuperando a figura interativa da função de sazonalidade para uma variável local.
        fig_1 = plot_plotly(modelo, previsao)

        # Estilizando.
        fig_1.update_layout(
            xaxis_title="Tempo",
            yaxis_title="TPV (em R$)",
            title="TPV (em R$) ao Longo do Tempo",
            showlegend=True,  # Mostra a legenda do gráfico.
            font=dict(size=15),
        )

        # Renomeando curvas e setando a visibilidade apenas para curva Intervalos.
        nomes = {None: "Intervalos", "Predicted": "Tendência", "Actual": "TPV"}
        fig_1.for_each_trace(lambda trace: trace.update(name=nomes[trace.name]))
        fig_1.for_each_trace(
            lambda trace: trace.update(visible="legendonly")
            if trace.name in ["Intervalos"]
            else ()
        )

        # Recuperando a figura interativa da função de componentes para uma variável local.
        fig_2 = plot_components_plotly(modelo, previsao)

        # Estilizando.
        fig_2.update_layout(
            title="Tendência e Sazonalidade Semanal", font=dict(size=15)
        )

        # Atualizando o atributo .graficos
        self.graficos = [fig_1, fig_2]
