- ### Guia de instalação do modelo de sazonalidades [Prophet](https://facebook.github.io/prophet/):

> 1. Instale o [Anaconda](https://www.anaconda.com/);
>
> 2. Em seguida, instale o [GIT](https://git-scm.com/);
>
> 3. Abra o Anaconda Prompt e navegue até a pasta que você quer fazer o clone do repositório usando o comando `cd`;
>
> 4. Uma vez dentro dessa pasta, digite o seguinte comando:
```
git clone https://github.com/joao-vitor-souza/stone-dc-2022
```
> 5. Agora, ainda no terminal, entre na pasta `stone-dc-2022/models`:
```
cd stone-dc-2022/models
```
> 6. Agora crie um ambiente virtual com a versão 3.8.13 do Python, para isso digite:
```
conda create -n nome_seu_ambiente python=3.8.13
```
> 7. Substitua `nome_seu_ambiente` pelo nome que você quer dar ao seu ambiente. Agora ative o ambiente:
```
conda activate nome_seu_ambiente
```
> 8. Uma vez ativado, instale as dependências do modelo com o seguinte comando:
```
pip install pandas plotly streamlit
```
> 9. Quando terminar de instalar as dependências você instalará o modelo propriamente dito:
```
conda install -c conda-forge prophet
```
> 10. Por último, execute o comando:
```
streamlit run modelo_app.py
```
> Se tudo ocorreu como esperado, então uma aba abrirá no seu navegador com a aplicação rodando, pronta para ser usada em análises de tendência. Parte da aplicação se parece com a seguinte imagem:

<div align="center"><img src="https://i.ibb.co/n3kkWvL/modelo.png" alt="Exemplo do modelo de sazonalidade"></div>
