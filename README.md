# Raízes do Nordeste

Projeto de backend desenvolvido em Python utilizando FastAPI e Supabase. A aplicação foi criada para gerenciar pedidos e algumas operações de uma rede de restaurantes, incluindo autenticação de usuários, consulta de produtos, pagamentos simulados e controle de estoque.

O objetivo principal foi desenvolver uma API REST que permitisse realizar o fluxo de um pedido, desde seu cadastro até a finalização, utilizando um banco de dados para armazenar as informações.

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- PostgreSQL
- Supabase e Supabase Auth
- Uvicorn
- JWT
- Swagger
- Postman

## Funcionalidades

A API permite cadastrar usuários e realizar login por meio do Supabase Auth. Após a autenticação, o usuário recebe um token JWT para acessar as rotas protegidas.

O sistema possui controle de permissões por perfil, diferenciando clientes, funcionários, gerentes e administradores.

Na parte de pedidos, é possível cadastrar um pedido com um ou mais produtos, consultar os pedidos existentes e acompanhar suas etapas. Durante o cadastro, o sistema verifica a disponibilidade dos produtos e a quantidade em estoque.

O pagamento é simulado por meio de uma rota específica. Após a aprovação, o pedido pode avançar pelas etapas de preparação, pronto e entregue.

Também foram implementadas movimentações de entrada e saída de estoque, cancelamento de pedidos e registros de auditoria para determinadas ações, como login e alteração de status.

## Estrutura do projeto

O código foi organizado separando as rotas da API, os modelos de dados, as regras de negócio e a comunicação com o banco.

A pasta `app` contém os arquivos principais da aplicação, incluindo os módulos responsáveis pela autenticação, pedidos, pagamentos e estoque.

O banco de dados utilizado é o PostgreSQL, disponibilizado pelo Supabase. Algumas operações também utilizam funções SQL para executar as regras de negócio.

Principais rotas

Método

Rota

Descrição

POST

/auth/cadastro

Cadastro de usuário

POST

/auth/login

Login

GET

/auth/me

Dados do usuário autenticado

GET

/auth/admin

Acesso administrativo

POST

/pedidos

Cadastro de pedido

GET

/pedidos

Consulta de pedidos

PATCH

/pedidos/{pedido_id}/status

Atualização do status

POST

/pedidos/{pedido_id}/cancelar

Cancelamento de pedido

POST

/pagamentos/mock

Simulação de pagamento

POST

/estoque/movimentacoes

Movimentação de estoque

As demais rotas podem ser consultadas pelo Swagger.

## Como executar

Para executar o projeto localmente, é necessário ter o Python instalado e configurar as variáveis de ambiente utilizadas na conexão com o Supabase.

Depois de instalar as dependências do projeto, o servidor pode ser iniciado pelo terminal com o comando:


python -m uvicorn app.main:app --reload


Com o servidor em execução, a documentação da API fica disponível em:

http://127.0.0.1:8000/docs

A especificação OpenAPI pode ser acessada em:

http://127.0.0.1:8000/openapi.json

## Testes

Os testes foram realizados utilizando o Swagger e o Postman.

Foram verificados os processos de autenticação, criação e consulta de pedidos, pagamento simulado, alteração de status, cancelamento e movimentações de estoque.

Também foram realizados testes com informações inválidas para verificar o retorno dos erros e o comportamento das validações.

A coleção de requisições do Postman está disponível junto aos arquivos do projeto.

## Considerações finais

O projeto permitiu trabalhar com desenvolvimento de APIs REST, autenticação, controle de acesso, integração com banco de dados e validação de regras de negócio.

O fluxo principal de pedidos foi implementado e testado, incluindo a criação do pedido, a aprovação do pagamento e a atualização das etapas de atendimento.

A aplicação ainda pode receber melhorias e novas funcionalidades, principalmente nas áreas de segurança, fidelização de clientes e gerenciamento das operações.
