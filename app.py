import warnings

import numpy as np
import pandas as pd
import plotly
import streamlit as st

from utils.etl import engajamentoETL
from utils.gerador import Gerador
from utils.plots import Plots

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Dashboard", page_icon="📊")

st.sidebar.markdown(
    """<p style="text-align: center;">
	<img src="https://i.ibb.co/qMJJ42g/tmp-626f3ef821a1e.png" alt="Logo Stone" width="150" height="150">
	</p>
	""",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """<p style="font-family:Cambria; font-size: 23px; text-align: center">
	StoneCo Data Challenge 2022
	<hr>
	</p>""",
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    label="",
    options=[
        "Problema de Negócio",
        "Análise Exploratória",
        "Modelo Sazonal",
        "Curvas de Engajamento",
        "Conclusões",
    ],
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.markdown(
    """<p style="text-align: center;">
	<a href="https://github.com/joao-vitor-souza/stone-dc-2022">
	<img src="https://i.ibb.co/B4Wvm4R/imagem-menu.png" alt="Github" width="200" height="75">
	</a>
	</p>
	""",
    unsafe_allow_html=True,
)


def ler_json(path):
    return plotly.io.read_json(path)


if page == "Problema de Negócio":

    st.header("Problema de Negócio")

    "---"

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">A <a href="https://www.stone.co/br/">Stone</a> tem como objetivo ajudar o empreendedor brasileiro a vender, gerir e crescer seu negócio através dos produtos e serviços que vão desde a maquininha de cartão de crédito a sistemas ERP para gestão. Um dos produtos que oferecemos aos nossos clientes é o crédito, voltado para facilitar a vida do lojista e impulsionar o crescimento do seu negócio. Nosso produto é diferenciado: os clientes pagam seus empréstimos através de um percentual de retenção aplicado sobre as transações realizadas pela maquininha de cartão Stone.</p>""",
        unsafe_allow_html=True,
    )
    st.image("images/imagem_introducao.jpg")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Desta forma, conseguimos promover um pagamento sustentável do empréstimo que acompanha as variações de fluxo de caixa do lojista, que não precisa se comprometer com um valor fixo que possa pesar em um mês de baixo movimento em seu negócio. Durante a pandemia, naturalmente houve um aumento de clientes inadimplentes, ou seja, com problemas no pagamento de seus contratos e, consequentemente, sentimos a necessidade de evoluir nossas ações de comunicação e acionamento para recuperação dos saldos devedores que alguns clientes deixaram em aberto. Dentro desta evolução, uma das ações tomadas internamente foi refinar nossas estratégias de comunicação com os clientes, visando recuperar clientes que apresentavam problemas no ritmo de pagamento, e um dos problemas reais que nosso negócio enfrentou foi o seguinte: <br><br><b>Qual é a curva ideal de vezes que acionamos um cliente?</b><br><br>Quando um cliente começa a apresentar dificuldade na liquidação de seus contratos, ele é para ser acionado por nossa régua de comunicação com intuito de estimular a retomada do ritmo saudável de pagamento conforme o perfil e o momento de cada cliente. As comunicações são disparadas por contrato, sendo assim, um cliente pode receber diversas comunicações com diferentes conteúdos, um para cada momento da jornada de seu respectivo contrato. Desde o envio da comunicação até o recebimento, são gerados <i>flags</i> que indicam o engajamento do cliente com as comunicações. Ocasionalmente são observados erros no processo de envio do comunicado, gerando um percentual (%) de falhas por diversos motivos (servidor indisponível, número incorreto, etc.). Após o envio bem-sucedido, observamos também que nem todos os comunicados são lidos. Além do engajamento do cliente com as comunicações, temos outra questão importante: a efetividade na recuperação dos contratos ativos. Uma comunicação eficaz é aquela que estimula e converte um cliente com problemas na liquidação do seu contrato a retomar o pagamento saudável, seja por quitação ou do retorno ao ritmo de transação esperado. Para mensurar a efetividade de uma ação, temos dois ótimos termômetros: os dias sem pagamento (DSP) e os dias sem pagamento do principal de um cliente (DSPP). Os dias sem pagamento (DSP) representam o total de dias corridos que um contrato apresenta sem realizar nenhum pagamento. Já os dias sem pagamento do principal (DSPP), representam o total de dias corridos que um contrato apresenta sem reduzir o valor do saldo principal. Neste último conceito, mesmo que o contrato apresente algum pagamento, se este montante não for suficiente para cobrir juros + impostos, valores deduzidos prioritariamente, o saldo principal do contrato permanecerá sem pagamento. Dado o problema apresentado, analisaremos os dados disponibilizados de modo a entender e explorar a curva de engajamento x quantidade de acionamentos e trazer insights sobre a efetividade destas ações em termos de pagamento.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.info(
        "Caso queira alterar o tema (light ou dark), entre nas configurações clicando nos três traços no canto superior direito, clique em Settings, vá em Theme e escolha seu tema."
    )


if page == "Análise Exploratória":

    st.header("Análise Exploratória")

    "---"

    st.subheader("Overview")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Com os dados já limpos, primeiramente daremos uma olhada em alguns registros da base de dados para termos uma noção de como são os dados:<br><br></p>""",
        unsafe_allow_html=True,
    )

    head = pd.read_csv("data/curated/head.csv")
    st.dataframe(head)

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify"><br>Muitas das colunas já são auto-explicativas, mas para um maior entendimento de todos os atributos, deixo aqui o <a href="https://onedrive.live.com/view.aspx?cid=a5ad10a92da070cc&page=view&resid=A5AD10A92DA070CC!398&parId=A5AD10A92DA070CC!388&authkey=!AHJWu4Bs81am76E&app=Excel">dicionário</a> que explica cada um deles. Em resumo, temos o ID do contrato, seu <i>status</i>, datas e valores associados, além das informações gerais dos clientes. Uma descrição sumarizada dos dados retorna o seguinte resultado: <br><br></p>""",
        unsafe_allow_html=True,
    )

    describe = pd.read_csv("data/curated/describe.csv", index_col=0)
    st.dataframe(describe)

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px"><br>Algumas observações que já podem ser feitas:<br><br>- Há 14756 contratos na base de dados;<br>- A maioria dos contratos está ativa;<br>- O maior segmento e subsegmento de contratos são de Alimentação e Alimentação Rápida, respectivamente;<br>- São Paulo lidera como o estado com mais contratos;<br>- A maioria das empresas são Pessoas Jurídicas (PJs).</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Correlações")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Plotaremos as correlações entre alguns valores numéricos usando um mapa de calor, dessa forma facilitamos a identificação de variáveis que se relacionam de alguma forma.</p>""",
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        ler_json("data/curated/correlacoes.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px">Desse gráfico podemos tirar as seguintes conclusões:<br><br>- Quanto maiores os juros mensais, menor tende a ser o valor desembolsado pela Stone a seus clientes;<br>- Quanto maior o percentual de retenção, menor tende a ser o número de transações;<br>- Quanto maior é o valor desembolsado pela Stone, maior é a tendência de transações nas máquinas de cartão dos clientes;<br>- E quanto menor forem os juros mensais, maior será a tendência do número de transações.<br><br>Intuitivamente, os valores dos juros mensais e percentual de retenção jogam contra o aumento do número de transações. No entanto, é possível identificar o impacto positivo que os empréstimos feitos pela Stone têm sobre as vendas dos clientes. Podem não ser causais, mas já estão correlacionados.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Vencimento dos Contratos")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Analisemos agora a curva do vencimento dos contratos e a nossa posição atual na curva:</p>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ler_json("data/curated/qtd_contratos_venc.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Após passar por um período de baixa entre o final de 2020 e o meio de 2021, estamos agora em um momento onde há muito contratos vencendo, isso é um bom sinal de que estávamos vindo fechando cada vez mais contratos. Percebe-se também que estamos caminhando para o topo histórico da série de dados, que ocorrerá até o final desse mês. Além disso, o gráfico apresenta uma forte queda após o topo histórico, mas isso se deve ao fato de que os dados usados contabilizam os contratos feitos somente até o começo de junho de 2021, como veremos a seguir.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Contratos Feitos")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Em consonância com o gráfico anterior, observemos a curva da quantidade de contratos feitos:</p>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ler_json("data/curated/qtd_contratos_novos.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">A explicação da alta dos contratos vencendo pode ser facilmente deduzida agora. Estivemos praticamente o ano todo de 2021 acima da média de contratos realizados. Note o crescimento entre abril e setembro daquele ano, provavelmente devido à pandemia de Covid-19 e suas consequências. Vejamos esse crescimento em termos monetários.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Valor Desembolsado")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">O gráfico a seguir converte os contratos feitos (apresentados no gráfico anterior) para o montante final desembolsado pela Stone.</p>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ler_json("data/curated/qtd_vlr_des.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Obviamente os dois gráficos (valores e contratos) estão fortemente correlacionados. Uma coisa interessante a se notar é que o aspecto da curva está muito parecido com um padrão gráfico bastante conhecido chamado <a href="https://www.nelogica.com.br/conhecimento/tutoriais/introtec/ombro-cabeza-ombro">Ombro-Cabeça-Ombro (OCO)</a>. Será que poderíamos ter previsto a queda na quantidade de contratos feitos? <br><br>Analisemos agora como está distribuída os valores e a quantidade de contratos ativos por estado.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Distribuição Geoespacial dos Valores e Contrato Ativos")
    st.plotly_chart(
        ler_json("data/curated/qtds_mapa.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">A maioria dos contratos está concentrada nas regiões Sul e Sudeste do país, em especial, o estado de São Paulo, como já havíamos identificado. Isso mostra quais regiões devem receber mais atenção da empresa. Por exemplo, se quisermos ganhar mercado nas regiões onde nossa presença não é muito forte, podemos começar pela região Norte ou Nordeste. Já se quisermos nos consolidar onde temos muitos clientes, podemos focar ainda mais nas regiões Sul e Sudeste. Não só é interessante saber as distribuições geoespaciais, mas podemos também investigar como são as distribuições por segmentos e subsegmentos.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    st.subheader("Distribuição por Segmentos e Subsegmentos")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">É importante termos em mente como estão distribuídos nossos clientes, dessa forma podemos investir em <i>marketing</i> e direcionar mais recursos para aqueles que mais participam de todo o processo de contratação de crédito.</p>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ler_json("data/curated/qtd_vlr_pgt.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Como se pode ver, o segmento de Alimentação segue como líder absoluto. Em seguida vem o segmento de Bens Duráveis, que por mais que contribua mais que o de Varejo, provavelmente por ser um segmento de alto valor agregado (carros, construção, saúde...), ele não tem mais contratos feitos que o de Varejo, como podemos observar na Distribuição de Frequências por Subsegmento a seguir.</p>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ler_json("data/curated/qtd_sub_count.json"),
        use_container_width=True,
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify"><br>É possível ver a força que o subsegmento de Vestuário tem dentro do Varejo, assim como que, talvez contra-intuitivamente, o subsegmento de Alimentação Rápida é extremamente maior que o de Supermercados dentro do segmento de Alimentação. O setor automotivo também se destaca em dois segmentos, tanto na venda (Bens Duráveis), quanto na manutenção (Serviços).<br><br>Visto que temos agora uma boa noção de como os dados se comportam, encerra-se aqui a Análise Exploratória.</p>""",
        unsafe_allow_html=True,
    )

    "---"

if page == "Modelo Sazonal":

    st.header("Modelo Sazonal")

    "---"

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Um modelo sazonal é um algoritmo de <i>Machine Learning</i> extremamente robusto usado para análises de tendência e sazonalidade, logo se espera que seu desempenho será afetado se tentarmos rodá-lo por uma aplicação <i>web</i> sem usar processamento em nuvem adequado. Por isso deixo aqui o <a href="https://github.com/joao-vitor-souza/stone-dc-2022/blob/main/models">link do GitHub</a> com um arquivo escrito por mim que explica, passo a passo e em pouquíssimos comandos, como você pode fazer para instalar um modelo sazonal <i><a href="https://facebook.github.io/prophet/">Prophet</a></i> do Facebook® e rodá-lo localmente.<br><br> Para demonstrar como o modelo funciona, no entanto, vamos plotar os resultados para o TPV de um dos contratos (6fad93...) da base de dados:</p>""",
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        ler_json("data/curated/sazonalidade.json"),
        use_container_width=True,
    )

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Acima está o gráfico de dispersão com a curva que caracteriza a sazonalidade, chamada Tendência. Talvez não fique muito claro qual é a direção da tendência dos dados ou ainda como a sazonalidade se comporta semanalmente. Felizmente podemos dividir esse gráfico em duas componentes, e elas estão mostradas a seguir:</p>""",
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        ler_json("data/curated/sazonalidadeComponentes.json"),
        use_container_width=True,
    )

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Agora está muito mais claro como a tendência se comporta e qual é a curva de sazonalidade. Esse contrato, por exemplo, vem tendo uma tendência de queda na TPV ao longo do período analisado,  além disso, podemos ver que normalmente as vendas começam a alavancar a partir das Terças, e cai depois dos Sábados, talvez porque o comércio fica fechado aos Domingos. Com isso em mente podemos esperar receber mais transações associadas a esse contrato a partir das Terças, e uma queda entre os Domingos e Segundas. Baixas vendas nos Sábados, por exemplo, podem levantar um alerta de que o cliente está evitando usar a máquina da Stone para não pagar o empréstimo. <br><br> Esse foi só um exemplo de como analisamos os gráficos dessa categoria de modelos. Com ele instalado pode-se avaliar qualquer um dos mais de 14000 contratos da base de dados.</p>""",
        unsafe_allow_html=True,
    )

    "---"

if page == "Curvas de Engajamento":

    "---"

    st.header("Curvas de Engajamento")
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Relembremos qual era o problema que estamos tentando resolver da seção introdutória:<br><br><b>Qual é a curva ideal de vezes que acionamos um cliente?</b><br><br>Como já vimos na Análise Exploratória, os clientes podem ser classificados pelos seus segmentos de atuação e se seus contratos estão ativos, mas não só isso, nos dados processados há informações suficientes para classificá-los conforme o tipo (PJ, PF e MEI) e a Unidade Federativa da empresa. Há outras informações também como a cidade da empresa, mas um critério como esse acaba por diminuir a generalização dos dados e isso retira muita informação associada ao comportamento de um grupo maior, como a Unidade Federativa.<br><br>Foi falado na introdução do problema que existem duas réguas de acionamento para um determinado cliente que não vem pagando seu empréstimo, DSP e DSPP (já explicados naquela seção). Podemos então deduzir que precisaremos analisar o impacto de cada régua separadamente. Não só isso, existem dois meios de comunicação com os clientes, WhatsApp e <i>E-mail</i>, e também teremos que avaliá-los separadamente. Além disso, como os clientes podem ser segmentados, teremos que criar condições que efetuem essa tarefa. Um exemplo de cliente segmentado seria: O contrato do cliente está ativo, ele é da Bahia e trabalha como MEI no segmento de Varejo.<br><br>Plotando os gráficos de engajamento da régua DSP de todos os clientes, isto é, não usando nenhuma segmentação, temos os seguintes resultados:</p>""",
        unsafe_allow_html=True,
    )

    dadosEngajamento = pd.read_parquet(
        "data/processed/geralClientesComunicadosLimpo.parquet"
    )

    condicoes = np.ones(dadosEngajamento.shape[0], dtype=bool)

    dadosEmail, dadosHsm = engajamentoETL(dadosEngajamento, condicoes)

    curvaEngajamento = Plots(dadosEmail)
    fig = curvaEngajamento.gerarCurvaEngajamento()
    st.plotly_chart(fig)

    curvaEngajamento = Plots(dadosHsm)
    fig = curvaEngajamento.gerarCurvaEngajamento()
    st.plotly_chart(fig)

    st.info(
        "As curvas de engajamento para o status Entregue e Não Entregue podem ser ativadas clicando em seus nomes na legenda de cada gráfico."
    )
    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Poderíamos facilmente dizer que a campanha Observação em valores absolutos (note que o eixo y representa a Frequência Relativa) é a campanha que mais traz retornos, dada o seu engajamento, mas isso desconsidera a Frequência Relativa da quantidade de acionamentos feitos nessa campanha. Ora, para o cliente ser acionado em qualquer outra campanha, ele precisa necessariamente passar pela campanha Obervação, e por consequência, em valores absolutos, essa será a campanha com mais engajamento. Em um cenário onde os clientes não fizessem mais nenhum pagamento a partir da campanha Observação teríamos curvas com o valor de Frequência constante, já que o mesmo cliente seria acionado em todas as campanhas. No entanto, não é isso que se vê. <br><br><b>Geralmente a frequência absoluta de acionamentos diminui ao longo das campanhas, logo a maioria dos clientes acionados nas campanhas iniciais costumam fazer transações em suas maquininhas de cartão nos dias posteriores</b>.<br><br>Percebe-se também que praticamente metade dos acionamentos não são entregues ao longo das campanhas, enquanto normalmente apenas cerca de 15% a 25% serão lidos, e se temos certeza de algo é que se o cliente sequer recebe o acionamento então a campanha não o afeta de forma alguma. Percebe-se então que também há outro problema a se responder:<br><br><b> Como melhoramos a forma que acionamos os clientes, visando aumentar a frequência de acionamentos entregues?</b><br><br>Poderíamos supor um método de validação do <i>e-mail</i> e do celular do cliente para termos certeza que ambos existem e funcionam, talvez tentar uma conexão direta por ligação telefônica, ou ainda, requerer que os clientes forneçam referências de outras pessoas para entrarmos em contato. Existem diversas maneiras.<br><br>Mas agora, dentro dos meios de comunicação que já vem sendo utilizados, qual deles é melhor? Gerando quatro comparações, uma para cada <i>status</i> das <i>flags</i>, temos os seguintes gráficos:</p>""",
        unsafe_allow_html=True,
    )

    gerador = Gerador()

    lido = gerador.dadosComparacao(dadosEmail, dadosHsm, "LIDO")
    respondido = gerador.dadosComparacao(dadosEmail, dadosHsm, "RESPONDIDO")
    entregue = gerador.dadosComparacao(dadosEmail, dadosHsm, "ENTREGUE")
    n_entregue = gerador.dadosComparacao(dadosEmail, dadosHsm, "NAO ENTREGUE")

    for dados in [respondido, lido, entregue, n_entregue]:

        curvaComparacao = Plots(dados)
        fig = curvaComparacao.gerarCurvaComparacao()
        st.plotly_chart(fig)

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px">Cabe uma análise de cada comparação:<br><br>- <i>Status</i> Respondido: Os clientes, no geral, tendem a responder mais pelo <i>e-mail</i> em todas as campanhas;<br>- <i>Status</i> Lido: Os clientes apenas leem mais no WhatsApp;<br>- <i>Status</i> Entregue: Após a campanha Boleto Quitado, o <i>e-mail</i> tem uma maior taxa de entrega dos acionamentos;<br>- <i>Status</i> Não Entregue: Ambos apresentam valores altos entre cerca de 46% e 49%. O ideal seria que diminuíssemos esses valores.</p>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify"><br>Agora podemos avaliar o engajamento de qualquer segmento de cliente usando as opções abaixo. Perceba que algumas combinações podem não gerar resultados, nesses casos aparecerá um aviso na tela.</p>""",
        unsafe_allow_html=True,
    )

    "---"

    col_1, col_2 = st.columns(2)

    status_contrato = col_1.selectbox(
        "Status do Contrato",
        ["Todos"] + list(dadosEngajamento.status_contrato.unique()),
        index=0,
    )
    tipo_empresa = col_2.selectbox(
        "Tipo da Empresa",
        ["Todos"] + list(dadosEngajamento.tipo_empresa.unique()),
        index=0,
    )
    estado = col_1.selectbox(
        "Estado da Empresa",
        ["Todos"] + list(sorted(dadosEngajamento.estado.unique())),
        index=0,
    )
    segmento = col_2.selectbox(
        "Segmento da Empresa",
        ["Todos"] + list(dadosEngajamento.segmento.unique()),
        index=0,
    )
    dsp = col_1.radio("Régua de Acionamento", ["DSPP", "DSP"])

    chamada = col_2.button("Gerar Curvas de Engajamento")

    if chamada:

        condicoes = np.ones(dadosEngajamento.shape[0], dtype=bool)

        for condicao, condicao_nome in zip(
            [status_contrato, tipo_empresa, estado, segmento],
            ["status_contrato", "tipo_empresa", "estado", "segmento"],
        ):
            if condicao == "Todos":
                continue
            else:
                condicoes = np.logical_and(
                    condicoes, dadosEngajamento[condicao_nome] == condicao
                )

        dsp = True if dsp == "DSP" else False

        dadosEmail, dadosHsm = engajamentoETL(dadosEngajamento, condicoes, dsp)

        curvaEngajamento = Plots(dadosEmail)
        fig = curvaEngajamento.gerarCurvaEngajamento()
        if fig != None:
            st.subheader("Curvas de Engajamento")
            st.plotly_chart(fig)
        else:
            st.warning(
                "Não há dados segmentados para as condições escolhidas, escolha outros valores!"
            )

        curvaEngajamento = Plots(dadosHsm)
        fig = curvaEngajamento.gerarCurvaEngajamento()
        if fig != None:
            st.plotly_chart(fig)
            st.subheader("Curvas de Comparação")

        gerador = Gerador()

        lido = gerador.dadosComparacao(dadosEmail, dadosHsm, "LIDO")
        respondido = gerador.dadosComparacao(dadosEmail, dadosHsm, "RESPONDIDO")
        entregue = gerador.dadosComparacao(dadosEmail, dadosHsm, "ENTREGUE")
        n_entregue = gerador.dadosComparacao(dadosEmail, dadosHsm, "NAO ENTREGUE")

        for dados in [respondido, lido, entregue, n_entregue]:

            curvaComparacao = Plots(dados)
            fig = curvaComparacao.gerarCurvaComparacao()
            if fig != None:
                st.plotly_chart(fig)

    "---"

if page == "Conclusões":

    st.header("Conclusões")

    st.subheader("... da Análise Exploratória e Sazonal")

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify"><br>- Quanto maiores os juros mensais e o percentual de retenção, menor tende a ser o número de transações;<br><br>- Estamos caminhando para o pico histórico de contratos que vencerão;<br><br>- Foi durante os piores momentos da pandemia (06/2020 - 05-2021) que mais houve empréstimo por parte da Stone;<br><br>- A maioria dos contratos, valores desembolsados e valores pagos estão concentrados nas regiões Sul e Sudeste, em especial no estado de São Paulo;<br><br>- O segmento de Alimentação é disparado o maior contratante de crédito;<br><br>- O maior grupo de clientes por subsegmento são os clientes PJ's que trabalham com Alimentação Rápida;<br><br>- É possível identificar as sazonalidades e tendência de todos os contratos da base de dados, auxiliando na descoberta de quais são os dias prováveis que cada cliente fará transações na maquininha de cartão.</p>""",
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("... das Curvas de Engajamento")

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify"><br>- Para as duas réguas de acionamento, a taxa de acionamentos Respondidos nunca foi muito maior que 1% em todas as campanhas;<br><br>- A taxa de acionamentos Lidos ficou em torno de 17% em todas as campanhas para as duas réguas;<br><br>- Em todos os casos, a taxa de acionamentos Não Entregues sempre ficou próxima a 50%, o que é um valor relativamente alto;<br><br>- Já a taxa de acionamentos que receberam apenas o <i>status</i> de Entregue sempre ficou próxima a 1/3 do total enviado;<br><br>- Os clientes respondem mais pelo <i>e-mail</i> e costumam apenas visualizar mais pelo WhatsApp;<br><br>- Os acionamentos tendem a serem mais entregues pelo WhatsApp nas campanhas iniciais (Observação, Parcelamento e Boleto Quitado p/ DSP, e Observação p/ DSPP) e pelo <i>e-mail</i> nas campanhas restantes;<br><br>- Em valores relativos, as duas réguas de acionamento são muito parecidas ao longo de todas as campanhas para todas as <i>flags</i>. Já em valores absolutos, os clientes se engajam mais nas campanhas iniciais.</b></p>""",
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Qual é a Curva Ideal de Vezes que Acionamos um Cliente?")

    st.markdown(
        """<p style="font-family:Cambria; font-size: 20px; text-align: justify">Em valores absolutos, a curva ideal de acionamento de clientes que gerará mais engajamento (acionamentos lidos e/ou respondidos) e possivelmente a quitação das dívidas ocorre para os acionamentos nos primeiros 15 dias após a detecção de não pagamento. Em valores relativos, nesse mesmo período, para a régua DSP (3 acionamentos), teremos valores altos na taxa de acionamentos lidos (17,85% no Parcelamento e 18,19% no Boleto Quitado) e respondidos (0,96% no Boleto Quitado), já para a régua DSPP (1 acionamento), teremos as maiores taxas de acionamentos lidos (17,82% na Observação).</b></p>""",
        unsafe_allow_html=True,
    )
