# ImobiliariaAPI
Repositório para a API relacionada a um CRUD de reservas de Imóveis.
---
Nesse repositório utiliza-se um padrão arquitetural MVT, onde a camada de Template é substituída pelo processo de serialização e formatação dos dados adequados para a API.

Para o desenvolvimento também foi utilizado a metodologia [TDD](https://www.devmedia.com.br/test-driven-development-tdd-simples-e-pratico/18533) (Test-Driven Development), onde os testes foram desenvolvidos anteriores às Views ou camadas de serialização, para assim, ter uma melhor modelagem do funcionamento antes de "sair codando", dessa forma, tendo uma melhor qualidade de código e diminuindo as chances de bugs.

Para segurança da API, foi implementado a autenticação com token [JWT](https://www.devmedia.com.br/como-o-jwt-funciona/40265).

Por fim, utilizando a biblioteca [`drf-yasg`](https://drf-yasg.readthedocs.io/en/stable/), foi implementada uma documentação automática, que disponibiliza 2 interfaces, sendo elas `swagger` e `redoc`.

---

# Execução do ambiente

## Para usuários Windows
Usuários de Windows é recomendado utilizar um subsistema Ubuntu, para isso pode-se utilizar o `wsl`.

Para isso siga os passos abaixo:

1.  Primeiro abra o PowerShell como ADM.

2.  Execute o comando para instalar a distro do Ubuntu:
    
```sh
    wsl --install -d Ubuntu
```
3. Configure o username e password.
4. No próprio powershelll verifique se a versão  da distro que o Ubuntu está utilizando do WSL é a 2 executando o comando abaixo:

```sh
    wsl -l -v
```
- Caso não seja, atualize o WSL para a versão 2 com o comando abaixo:
```sh
    wsl --set-version Ubuntu 2
```

- Caso ao abrir o Ubuntu dê erro por falta de suporte, execute o comando abaixo no PowerShell como ADM e reinicie o computador.
```sh
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

- Ao utilizar o VS Code é importante ter a extensão WSL instalada.

---
## Com o Ubuntu já aberto

Caso não tenha o Python configurado, pode utilizar o Pyenv para gerenciar as versões do python da sua distro, podendo alternar entre elas conforme necessidade.

Para isso disponibilizei um [tutorial](https://like-loan-f5c.notion.site/Pyenv-082c9fdb3b82463f9535d54f5d2253bc?pvs=4) para a configuração.

- Garanta que está utilizando a versão mais atualizada do Python.

- Caso ainda não tenha, [instale](https://like-loan-f5c.notion.site/Poetry-12df841db7ec48b8a75a1ddce7af4ea9?pvs=4) o `Poetry` para criar um ambiente virtual e gerenciar as dependências do projeto.

- Caso ainda não tenha iniciado ou instalado, [inicie](https://like-loan-f5c.notion.site/MySQL-Server-dfcd6c53a5dc4218a8e6ba7633aa2f9c?pvs=4) o MySQL Server.
---

## Criando o schema para utilizar
1. Entre no ambiente mysql
```sh
    sudo mysql
```

2. Crie o `schema` que irá utilizar
```sql
    CREATE SCHEMA imobiliaria;
```

3. Saia do ambiente mysql
```sh
    exit
```

---

## Abrindo o projeto

1. Clone o projeto em sua pasta de preferência, pode por exemplo clonar dentro de uma pasta chamada `repositorios`:
#
Crie a pasta repositorios
```sh
    mkdir repositorios
```
Entre na pasta repositorios
```sh
    cd repositorios
```
Clone o repositório
```sh
    git clone <link>
```
---
2. Entre na pasta do projeto:
```sh
    cd ImobiliariaAPI
```
3. Abra o projeto
```sh
    code .
```
---

## Iniciando ambiente virtual e instalando as dependências
1. Abra um novo terminal no VS Code.


2. Inicie um novo ambiente virtual com o poetry:
```sh
    poetry shell
```
3. Instale as dependências
```sh
    poetry install
```
4. Crie um arquivo `.env` conforme o arquivo `.env.example` e configure as variáveis de ambiente conforme seu MySQL Server, atribuindo a `DB_NAME` o valor 'imobiliaria', conforme o schema que criamos. Também atribua os dados para seu usuário da API. O conteúdo do arquivo deve ficar algo como:
```sh
    DB_NAME='imobiliaria'
    DB_USER='user'
    DB_PASSWORD='123'
    DB_HOST='localhost'
    DB_PORT='3306'
    SUPERUSER_NAME='meu_usuario'
    SUPERUSER_PASSWORD='minha_senha'
```

---
## Iniciando a API
1. Entre na pasta raiz do projeto Django:
```sh
    cd imobiliaria
```
1. Com as variáveis de ambiente já configuradas, faça a migração dos models para seu schema:
```sh
    python manage.py migrate
```
2. Carregue o dump dos dados de exemplo disponibilizados:
```sh
    python manage.py loaddata fixtures/*
```
3. Ligue a API:
```sh
    python manage.py runserver
```
---
## Obtendo token de autenticação
1. Abra um novo terminal e entre na pasta raiz do projeto Django:
```sh
    cd imobiliaria
```
- Garanta ter configurado corretamente as variáveis de ambiente de `SUPERUSER`
2. Obtenha o token no terminal:
```sh
    python obter_token.py
```
---

## Executando os testes unitários

Você pode executar o teste de cada app individualmente através dos seguintes comandos:
```sh
    python manage.py test apps.imoveis.tests.ImovelApiTest
```
```sh
    python manage.py test apps.anuncios.tests.AnuncioApiTest
```
```sh
    python manage.py test apps.reservas.tests.ReservaApiTest
```

Se não forem feitas alterações no código, espera-se que todos testes passem :)

---
## Fazendo requisições
Com a API ligada é possível fazer requisições através de programas como [Postman](https://www.postman.com) e [Insomnia](https://insomnia.rest).

A documentação para as requisições fica disponível em duas interfaces, sendo elas [Swagger](http://localhost:8000/swagger/) e [Redoc](http://localhost:8000/redoc/). Utilize a de sua preferência para consultar os endpoints disponíveis :)

---
## Voilà! [:)](https://www.linkedin.com/in/felipecorreals/)