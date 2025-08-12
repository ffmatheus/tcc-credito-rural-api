# Aplicação de Tokenização de Safras
=====================================

## Resumo
-----------

Essa é uma aplicação FastAPI que permite a tokenização de safras para microfinanciamento. A aplicação utiliza um blockchain para garantir a segurança e transparência das transações.

## Funcionalidades
-----------------

* Tokenização de safras
* Obtenção de estatísticas gerais do sistema de tokenização
* Verificação de status da API e conexão com o blockchain
* Criação de novas safras
* Obtenção de dados detalhados de safras específicas

## Rotas
---------

### Rota Raiz

* `/`: Rota raiz que retorna uma mensagem de boas-vindas e informações sobre a aplicação.

### Rota Blockchain

* `/blockchain`: Rota que contém várias sub-rotas relacionadas ao blockchain.
	+ `/auth/token`: Rota que retorna um token de acesso para demonstração.
	+ `/estatisticas`: Rota que retorna estatísticas gerais do sistema de tokenização.
	+ `/status`: Rota que verifica o status da API e conexão com o blockchain.

### Rota Safras

* `/safras`: Rota que contém várias sub-rotas relacionadas às safras.
	+ `/tokenizar`: Rota que tokeniza uma nova safra no blockchain.
	+ `/obter_safra`: Rota que obtém dados detalhados de uma safra específica.

## Serviços
------------

* `blockchain_service`: Serviço que interage com o blockchain e fornece funcionalidades como tokenização de safras e obtenção de estatísticas.
* `verify_token`: Serviço que verifica a autenticidade de um token de acesso.

## Modelos
------------

* `SafraCreateRequest`: Modelo que representa uma solicitação de criação de safra.
* `SafraResponse`: Modelo que representa uma resposta de obtenção de dados de safra.
* `TransactionResponse`: Modelo que representa uma resposta de transação no blockchain.

## Configurações
----------------

* `settings`: Configurações gerais da aplicação, incluindo o nome da aplicação, descrição, versão, etc.
* `blockchain_url`: URL do blockchain.
* `contract_address`: Endereço do contrato no blockchain.

## Instalação
--------------

### Pré-requisitos

* Python 3.8+
* pip
* uvicorn

### Passos

1. Clone o repositório.
2. Instale as dependências utilizando `pip install -r requirements.txt`.
3. Configure as variáveis de ambiente.
4. Execute a aplicação utilizando `uvicorn main:app --host 0.0.0.0 --port 8000`.