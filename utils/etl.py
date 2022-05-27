# ---------------------- ETL Procedural p/ Gerar os Dados das Curvas de Engajamento ---------------------- #

# (E)TL: Extract

# Essa função recebe os dados, uma condição e a flag da régua de acionamento.
def __extrairDados(dados, condicao, dsp):

    # Condicional para verificar qual é a régua de acionamento.
    if dsp:
        df = dados[condicao][["dsp", "status"]]
        df = df[df.dsp.isin([5, 10, 15, 30, 60, 90])]
    else:
        df = dados[condicao][["dspp", "status"]]
        df = df[df.dspp.isin([15, 30, 45])]

    # Renomeando colunas para um nome comum.
    df.rename({"dsp": "campanha", "dspp": "campanha"}, axis=1, inplace=True)

    # Filtragem e criação de duas colunas extras.
    df_email = df[dados.tipo_acao == "EMAIL"]
    df_email["meio_comunicacao"] = "E-mail"
    df_email["dsp_flag"] = dsp

    df_hsm = df[dados.tipo_acao == "HSM"]
    df_hsm["meio_comunicacao"] = "Whatsapp"
    df_hsm["dsp_flag"] = dsp

    return df_email, df_hsm


# E(T)L: Transform

# Essa função transforma os dados recebidos por parâmetro.
def __transformarDados(dados):

    # Agrupa os dados, calculando a frequência relativa.
    df = __agruparDados(dados)
    # Agrupa os dados, calculando a frequência absoluta.
    df["frequencia"] = __agruparDados(dados, False)[[0]]

    # Renomeando coluna.
    df.rename({0: "frequencia_relativa"}, axis=1, inplace=True)

    # Ordernando registros de forma decrescente para a frequencia e crescente para a campanha.
    df.sort_values(by=["campanha", "frequencia"], ascending=[True, False], inplace=True)

    return df


# Função que agrupa os dados e substitui valores nulos por zero.
def __agruparDados(dados, normalize=True):
    return (
        dados.groupby("campanha")
        .value_counts(normalize=normalize)
        .unstack(level="status", fill_value=0)
        .stack()
        .reset_index()
    )


# Execução do ETL completo.


def engajamentoETL(dados, condicao, dsp=True):

    # Extração.
    df_email, df_hsm = __extrairDados(dados, condicao, dsp)

    # Transformação.
    df_email_processed = __transformarDados(df_email)
    df_hsm_processed = __transformarDados(df_hsm)

    # Carregamento.
    return df_email_processed, df_hsm_processed
