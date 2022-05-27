download:

	@echo --------------------------------------
	@echo Baixando portfolio_comunicados.parquet
	@echo --------------------------------------

	@cd data/raw && curl -O https://stone-dc-2022.s3.sa-east-1.amazonaws.com/portfolio_comunicados.parquet

	@echo --------------------------------------
	@echo Baixando portfolio_tpv.parquet
	@echo --------------------------------------

	@cd data/raw && curl -O  https://stone-dc-2022.s3.sa-east-1.amazonaws.com/portfolio_tpv.parquet

	@echo --------------------------------------
	@echo Baixando portfolio_clientes.parquet
	@echo --------------------------------------

	@cd data/raw && curl -O https://stone-dc-2022.s3.sa-east-1.amazonaws.com/portfolio_clientes.parquet

	@echo --------------------------------------
	@echo Baixando portfolio_geral.parquet
	@echo --------------------------------------

	@cd data/raw && curl -O https://stone-dc-2022.s3.sa-east-1.amazonaws.com/portfolio_geral.parquet

install: 

	@echo --------------------------------------
	@echo Instalando dependencias...
	@echo --------------------------------------
	
	@poetry install
	@poetry run pre-commit install

clean:

	@echo -----------------------------------------------------
	@echo Pre-processando os dados, essa etapa pode demorar.
	@echo -----------------------------------------------------

	@python utils/limpeza.py

activate:

	@echo --------------------------------------------------------
	@echo Ativando ambiente virtual
	@echo --------------------------------------------------------

	@poetry shell

run:

	@echo --------------------------------------------------------
	@echo Rodando localmente, uma aba vai abrir no seu navegador.
	@echo --------------------------------------------------------

	@streamlit run app.py

setup: download install clean activate run
