# Definindo classe geradora de dados.
class Gerador:

    # Método para gerar os dados sazonais.
    # Esse método recebe os dados já limpos, o id do contrato a ser analisado e uma flag indicando se devemos usar
    # apenas os registros de quando o contrato está ativo.
    @staticmethod
    def dadosSazonalidade(dados, contrato_id, status_ativo=True):

        # Conferindo flag de status.
        if status_ativo:
            dados = dados[dados.status_contrato == "Active"]

        # Filtrando o contrato selecionado.
        dados = dados[dados.contrato_id == contrato_id]

        # Selecionando e renomeando colunas. O modelo sazonal só aceita DataFrames com esses nomes de coluna.
        dados = dados[["dt_transacao", "vlr_tpv"]]
        dados.columns = ["ds", "y"]

        return dados
