FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app-flashcards

# Cria todos os diretórios necessários em um único comando
RUN mkdir -p apostilas flashcard media study_async templates usuarios

# Copia todos os arquivos necessários
COPY apostilas/ apostilas/
COPY flashcard/ flashcard/
COPY media/ media/
COPY study_async/ study_async/
COPY templates/ templates/
COPY usuarios/ usuarios/
COPY manage.py manage.py
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt 

# Define as permissões de forma mais eficiente
RUN chmod -R a+rwx apostilas flashcard media study_async templates usuarios

# Comando para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]