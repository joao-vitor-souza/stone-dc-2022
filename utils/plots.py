# Biblioteca de plotagem interativa.
import plotly.express as px


# Definindo classe de plotagem.
class Plots:

    # Método construtor que recebe os dados.
    def __init__(self, dados):
        self.dados = dados

    # Método privado que constrói um grafico base para as outras plotagens.
    def __graficoBase(self, hue, titulo):

        # Condicional para checar qual régua de acionamento está sendo usada.
        if self.dados.dsp_flag.iloc[0]:
            # Definindo os parâmetros estruturais da plotagem.
            ticks_texto = [
                "Observação",
                "Parcelamento",
                "Boleto Quitado",
                "Pré-negativação",
                "Negativação",
                "Boleto Quitado",
            ]
            ticks_vals = list(range(5, 91, int((90 - 5) / (len(ticks_texto) - 1))))
            ticks_dados = dict(zip([5, 10, 15, 30, 60, 90], ticks_vals))
            ticks_campanha = dict(zip([5, 10, 15, 30, 60, 90], ticks_texto))
            xlim = [0, 95]

        else:
            ticks_texto = ["Observação", "Parcelamento", "Boleto Quitado"]
            ticks_vals = list(range(15, 46, int((45 - 15) / (len(ticks_texto) - 1))))
            ticks_dados = dict(zip([15, 30, 45], ticks_vals))
            ticks_campanha = dict(zip([15, 30, 45], ticks_texto))
            xlim = [10, 50]

        # Fazendo cópia dos dados para modificação.
        dados = self.dados.copy()

        # Adicionando coluna de rótulos posicionais.
        dados["ticks"] = dados.campanha.map(ticks_dados)

        # Adicionando coluna com os nomes das campanhas.
        dados["nomes_campanha"] = dados.campanha.map(ticks_campanha)

        # Acentuando uma das entradas do campo status.
        dados.replace({"NAO ENTREGUE": "Não Entregue"}, inplace=True)

        # Capitalizando todos os status.
        dados.status = dados.status.str.title()

        # Renomeando colunas.
        dados.rename(
            {
                "frequencia_relativa": "Frequência Relativa",
                "frequencia": "Frequência Absoluta",
                "meio_comunicacao": "Meio de comunicação",
                "status": "Status",
            },
            axis=1,
            inplace=True,
        )

        # Instanciando plotagem interativa.
        fig = px.line(
            dados,  # Dados.
            x="ticks",  # Eixo x.
            y="Frequência Relativa",  # Eixo y.
            color=hue,  # Coluna de cores.
            markers=True,  # Adicionando marcadores.
            hover_name="nomes_campanha",  # Nome da coluna que terá efeito hover.
            hover_data={
                "ticks": False,
                hue: True,
                "Frequência Relativa": True,
                "Frequência Absoluta": True,
            },  # Colunas que serão apresentadas no hover.
        )

        # Estilizando a instância.
        fig.update_layout(
            xaxis=dict(
                ticktext=ticks_texto,  # Adicionando os nomes das campanhas.
                tickvals=ticks_vals,  # Adicionando as posições numéricas no eixo.
                title="Campanha",  # Título do eixo.
                range=xlim,
            ),  # Intervalo do eixo.
            yaxis_tickformat=".2%",  # Formatação dos valores no eixo y.
            title=titulo,  # Título do gráfico.
            font=dict(size=13),  # Fonte geral.
        )

        # Inicializando as curvas de Não Entregue e Entregue como invisíveis.
        fig.for_each_trace(
            lambda trace: trace.update(visible="legendonly")
            if trace.name in ["Não Entregue", "Entregue"]
            else ()
        )

        return fig

    # Método para gerar curva de engajamento.
    def gerarCurvaEngajamento(self):

        # Se houver erro de indexação, não geraremos nenhum gráfico.
        try:
            # Definindo os parâmetros para o gráfico base.
            hue = "Status"
            titulo = f"Curvas de Engajamento por {self.dados.meio_comunicacao.iloc[0]} x Quantidade de Acionamentos por Campanha"

            # Passando argumentos.
            return self.__graficoBase(hue, titulo)
        except IndexError:
            return None

    # Faz a mesma coisa que o método anterior, mas agora irá gerar curvas de comparação.
    def gerarCurvaComparacao(self):

        try:
            hue = "Meio de comunicação"
            titulo = f"Comparação para o Status {self.dados.status.iloc[0].title()}"

            return self.__graficoBase(hue, titulo)
        except IndexError:
            return None
