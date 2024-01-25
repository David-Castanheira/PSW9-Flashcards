# Sobre o projeto
Projeto desenvolvido durante o curso Pystack Week 9.0, um evento online e gratuito que ensina como criar aplicações Web com Python e Django. Ainda está em processo de melhora e inclusão de novas funcionalidades, assim como correção de bugs.

## Objetivo 
O objetivo do projeto é criar um site de perguntas e respostas, onde os usuários podem se cadastrar, fazer e responder perguntas, votar nas melhores respostas e ganhar pontos de reputação.

### Ambiente virtual
Durante este, foi-se criado um ambiente virtual, o que garante o desenvolvimento estável e consistente sem interferir em outros projetos ou no ambiente global, neste caso, do Python. **É importante que esse passo seja feito antes mesmo da instalação do Django! Para que o mesmo seja usado no próprio ambiente** Para criá-lo e ativá-lo, execute os seguintes comandos:

```
$ python -m venv nome_ambiente

$ venv\Scripts\Activate
```

## Ferramentas 
A linguagem back-end responsável pelas regras de negócio e lógica da aplicação em questão é o **[Python](https://docs.python.org/pt-br/3/tutorial/)**:
* O framework web utilizado é **[Django](https://docs.djangoproject.com/en/5.0/)** que facilita o desenvolvimento de aplicações web de alto desempenho, escaláveis e seguras. Django segue o padrão model-template-view (MTV), que separa a lógica de negócio, a apresentação e o controle da aplicação. Django também oferece diversos recursos prontos para uso, como autenticação, administração, roteamento, ORM, migrações, formulários, testes, entre outros;
* Além disso, foi-se utilizado também uma biblioteca/pacote que, por sua vez, possui funções responsáveis pela manipulação de imagens em diversos formatos e o **[ORM](https://www.ufsm.br/pet/sistemas-de-informacao/2022/05/23/orm)** aplicado ao **[SQLite](https://www.sqlite.org/docs.html)** para o armazenamento de informações no banco de dados. 
Para instalá-los, basta seguir os passos abaixo com o uso de um pacote de instalação chamado 'pip' no terminal do Windows:

```
$ pip install pillow
```

Para verificar se a instalação foi feita corretamente, rode o seguinte comando:
```
$ pip show pillow
```

Após isso, rode o comando de instalação do Django no terminal:
```
$ pip install django 
```
Após isso, acesse "http://localhost:8000" -> onde 8000 é a porta que o Django usa por padrão. Caso exiba uma tela interativa significa que a instalação ocorreu de maneira esperada! Parabéns!

[![Imagem 1 - Tela de instalação bem-sucedida (Mozilla MDN)]](https://developer.mozilla.org/es/docs/Learn/Server-side/Django/development_environment/django_skeleton_app_homepage_django_4_0.png "Imagem 1 - Tela de instalação bem-sucedida (Mozilla MDN)")

## Iniciando um projeto
```
$ django-admin startproject nome_projeto
```

## Criando um app
```
$ python manage.py startapp nome_app
```

## Migrações 
Para a instalação das migrações e executálas, utilize os seguintes comandos:

```
$ python manage.py makemigrations

$ python manage.py migrate
```
Obs:. Perceba que nelas há a passagem do arquivo 'manage.py' respnsável justamente por esse gerenciamento da aplicação

### Superusuário
Para criar um superusuário (informe e-mail e senha para ter acesso ao painel de admin) na sua aplicação, execute o comando abaixo:

```
$ python manage.py createsuperuser
```

Após isso, acesse "http://localhost:8000/admin"

### Execução
```
$ python manage.py runserver
```
