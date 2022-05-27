import pandas as pd

# --------------------------------- Geração de Dados Orientada a Objetos --------------------------------- #

# Definindo classe geradora de dados.
class Gerador:

    # Método para limpar os dados.
    def dadosLimpos(self):

        # --------------------------------- Leitura --------------------------------- #

        geral = pd.read_parquet("data/raw/portfolio_geral.parquet")
        clientes = pd.read_parquet("data/raw/portfolio_clientes.parquet")
        comunicados = pd.read_parquet("data/raw/portfolio_comunicados.parquet")
        tpv = pd.read_parquet("data/raw/portfolio_tpv.parquet")

        # ---------------------------- Conversão de Tipo ---------------------------- #

        geral.dt_ref_portfolio = pd.to_datetime(geral.dt_ref_portfolio)
        comunicados.dt_ref_portfolio = pd.to_datetime(comunicados.dt_ref_portfolio)
        tpv.dt_transacao = pd.to_datetime(tpv.dt_transacao, format="%Y%m%d")

        # ---------------------------------- Joins ---------------------------------- #

        # Entre as tabelas portfolio_geral e porfolio_clientes, usando a chave nr_documento.
        geralClientes = geral.merge(clientes, on="nr_documento")

        # Entre o join anterior e a tabela portfolio_comunicados, usando as chaves contrato_id e dt_ref_portfolio.
        geralClientesComunicados = geralClientes.merge(
            comunicados, on=["contrato_id", "dt_ref_portfolio"]
        )

        # E entre as tabelas portfolio_geral e portfolio_tpv, usando as chaves dt_ref_portfolio (que foi renomeada) e nr_documento.
        geralTpv = geral.rename({"dt_ref_portfolio": "dt_transacao"}, axis=1).merge(
            tpv, on=["nr_documento", "dt_transacao"]
        )

        # --------------------------------- Limpeza --------------------------------- #

        geralClientesLimpo = self.__limparDados(geralClientes, "geralClientes")
        geralClientesComunicadosLimpo = self.__limparDados(
            geralClientesComunicados, "geralClientesComunicados"
        )
        geralTpvLimpo = self.__limparDados(geralTpv, "geralTpv")

        # --------------------------- Seleção de Atributos -------------------------- #

        geralClientesLimpo = geralClientesLimpo[
            [
                "contrato_id",
                "status_contrato",
                "dt_vencimento",
                "dt_contrato",
                "dt_desembolso",
                "vlr_desembolsado",
                "vlr_pgto_realizado",
                "juros_mes",
                "flag_transacao",
                "perc_retencao",
                "tipo_empresa",
                "estado",
                "subsegmento",
                "segmento",
            ]
        ]

        geralClientesComunicadosLimpo = geralClientesComunicadosLimpo[
            [
                "status_contrato",
                "dsp",
                "dspp",
                "tipo_empresa",
                "estado",
                "segmento",
                "tipo_acao",
                "status",
            ]
        ]

        geralTpvLimpo = geralTpvLimpo[
            ["status_contrato", "contrato_id", "dt_transacao", "vlr_tpv"]
        ]

        # ------------------------------- Pós-limpeza ----------------------------- #

        # Editando as colunas de datas usando um formatador.
        for dt in ["dt_vencimento", "dt_contrato", "dt_desembolso"]:
            geralClientesLimpo[dt] = geralClientesLimpo[dt].map(lambda x: x[:7])

        # Como essa tabela será usada para segmentar os clientes, precisaremos filtrar os valores ND da coluna estado, evitando assim que o
        # cliente seja atribuído a um estado inexistente. Os valores identificados serão salvos na pasta logs.
        geralClientesComunicadosLimpo[
            geralClientesComunicadosLimpo.estado == "ND"
        ].to_parquet("logs/dadosND/geralClientesComunicadosLimpoND.parquet")
        geralClientesComunicadosLimpo = geralClientesComunicadosLimpo[
            geralClientesComunicadosLimpo.estado != "ND"
        ]

        # ------------------------------ Carregamento ----------------------------- #

        self.__carregarDados(
            geralClientesLimpo, "data/processed/geralClientesLimpo.parquet"
        )
        self.__carregarDados(
            geralClientesComunicadosLimpo,
            "data/processed/geralClientesComunicadosLimpo.parquet",
        )
        self.__carregarDados(geralTpvLimpo, "data/processed/geralTpvLimpo.parquet")

    # Método de limpeza intermediário.
    def __limparDados(self, dados, conjuntoNome):

        # Checando por valores nulos.
        if dados.isnull().sum().sum():
            # Se houver valores nulos eles serão salvos localmente no diretório logs e em seguida removidos.
            dadosNulos = dados[dados.isnull()]
            dadosNulos.to_parquet(f"logs/dadosNulos/{conjuntoNome}.parquet")
            dados.dropna(inplace=True)

        # Faremos o mesmo procedimento para dados duplicados.
        if dados.duplicated().sum():
            dadosDuplicados = dados[dados.duplicated()]
            dadosDuplicados.to_parquet(f"logs/dadosDuplicados/{conjuntoNome}.parquet")
            dados.drop_duplicates(inplace=True)

        return dados

    # Método para gerar os dados de comparação.
    # Esse método recebe os dois conjuntos de dados a serem comparados e o status de comparação.
    @staticmethod
    def dadosComparacao(dadosEmail, dadosHsm, status):

        # Filtrando pelo status escolhido.
        dadosEmailComparacao = dadosEmail[dadosEmail.status == status]
        dadosHsmComparacao = dadosHsm[dadosHsm.status == status]

        # Concatenando ao longo do eixo das linhas.
        dadosComparacao = pd.concat([dadosHsmComparacao, dadosEmailComparacao])

        return dadosComparacao

    # Método privado para carregar os dados.
    def __carregarDados(self, dados, path):
        dados.to_parquet(path)
