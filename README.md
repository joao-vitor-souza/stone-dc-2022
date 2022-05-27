![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

<img src="https://img.shields.io/github/license/joao-vitor-souza/stone-dc-2022?style=flat-square">  <img src="https://img.shields.io/github/last-commit/joao-vitor-souza/stone-dc-2022?style=flat-square"> <img src="https://img.shields.io/github/languages/count/joao-vitor-souza/stone-dc-2022?style=flat-square">
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)


## Stone Data Challenge 2022

### Aplicação Final: https://share.streamlit.io/joao-vitor-souza/stone-dc-2022/main/app.py

- ### Links úteis:

> - Arquivos brutos csv zipados: [One Drive](https://1drv.ms/u/s!AsxwoC2pEK2lgwRrm4CeJwtGEcBc?e=aQuPlA)
> - Arquivos processados csv zipados: [One Drive](https://1drv.ms/u/s!AsxwoC2pEK2lgwWGiv9ochTxVmmf?e=Fk9jBt)
> - Descrição do evento: [One Drive](https://1drv.ms/u/s!AsxwoC2pEK2lgxCw4HCXSCcsEIam?e=wFUWNH)


- ### Descrição dos arquivos e diretórios:

> `data`: Conterá todos os dados utilizados;
> 
>> `data/raw`: Dados brutos no formato parquet que serão baixados do AWS S3. Para baixar use o comando `make download`;
>>
>> `data/processed`: Dados processados após a chamada do comando `make clean`;
>>  
>> `data/curated`: Dados prontos para consumo;
>
> `images`: Imagens usadas na aplicação web;
>
> `logs`: Contém os registros filtrados nas operações de limpeza;
> 
>> `logs/dadosDuplicados`: Registros duplicados identificados;
>>
>> `logs/dadosND`: Registros com o atributo `estado` não definido (ND);
>
> `models`: Diretório do modelo de sazonalidade
>>
>> `models/utils`: Funções de utilidade do modelo, análogas às da aplicação principal em `utils`;
>>
>> `models/modelo_app.py`: Aplicação do modelo de sazonalidade;
>>
>> `models/README.md`: Guia de instalação do modelo;
>
> `notebooks`: Notebook explicando a lógica por traz das sumarizações e gráficos feitos;
>>
>> `frequencias.ipynb`: Frequências calculadas de cada campanha; 
>>
>> `gerarGraficos.ipynb`: Funções que geraram os gráficos usados na aplicação web;
>
> `utils`: Contém os scripts de utilidades usados na aplicação principal;
>
>> `utils/etl.py`: Funções que usam os dados em `data/processed` e os deixam prontos para serem usados nas curvas de engajamento;
>>
>> `utils/gerador.py`: Classe que gera os dados limpos e os dados de comparação;
>>
>> `utils/limpeza.py`: Script para limpar os dados. Ele importa o `gerador.py` e é chamado pelo comando `make clean`;
>>
>> `utils/plots.py`: Define a classe de plotagem das curvas de engajamento;
>>
>> `utils/to_parquet.py`: Script para transformar os dados brutos de csv para parquet;
>
> `app.py`: Aplicação (Dashboard) final na web;
>
> `Makefile`: Arquivo para automatizar todos os processos de instalação, limpeza e execução;
>
> `poetry.lock` e `pyproject.toml`: Dependências da aplicação `app.py`.
