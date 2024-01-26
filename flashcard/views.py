from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.http import HttpResponse, Http404
from django.contrib.messages import constants 
from django.contrib import messages 

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == "GET":
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user = request.user)
        
        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            # Por 'categoria' ser FK de outra tabela, é necessário passar o parâmetro 'categoria__id'
            flashcards = flashcards.filter(categoria__id = categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade = dificuldade_filtrar)
        
        return render(request, 'novo_flashcard.html', {'categorias': categorias, 
                                                       'dificuldades': dificuldades,
                                                       'flashcards': flashcards})

    elif request.method == "POST":
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        # Função extra para adicionar o '?' caso o usuário não o coloque
        # def verificar_pergunta(request):
        #     if request.method == "POST":
        #         texto = request.POST['texto']
        #         texto = verificar_pergunta(texto)
        #         pergunta = Flashcard(texto = texto)
        #         pergunta.save()

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            # Não deixa o usuário cadastrar a pergunta
            messages.add_message(request, constants.ERROR, "Preencha os campos abaixo")
            return redirect('/flashcard/novo_flashcard/')

        flashcard = Flashcard(
            user = request.user, 
            pergunta = pergunta,
            resposta = resposta,
            categoria_id = categoria,
            dificuldade = dificuldade
        )

        flashcard.save()

        messages.add_message(request, constants.SUCCESS, "Flashcard cadastrado com sucesso!")
        return redirect('/flashcard/novo_flashcard')
    
def deletar_flashcard(request, id):
    # Fazer a validação de segurança (verificar se o que foi feito abaixo está certo)
    # dica: request.auth

    flashcard = Flashcard.objects.get(id = id)

    if not flashcard.user == request.user:
        raise Http404   
    
    flashcard.delete()
    messages.add_message(request, constants.SUCCESS, "Flashcard deletado com sucesso!")
    return redirect('/flashcard/novo_flashcard')
    

def iniciar_desafio(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(request, 'iniciar_desafio.html', {'categorias': categorias, 
                                                        'dificuldades': dificuldades})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user = request.user,
            titulo = titulo,
            dificuldade = dificuldade,
            quantidade_perguntas = qtd_perguntas
        )

        desafio.save()

        # Forma 1 - Loop For
        # for categoria in categorias:
        #     desafio.categoria.add(categoria)

        # Forma 2
        desafio.categoria.add(*categorias)

        flashcards = (Flashcard.objects.filter(user = request.user)
                    .filter(dificuldade = dificuldade)
                    .filter(categoria_id__in = categorias)
                    .order_by('?')
        )

        # Se tiver menos flashcards do que qtd_perguntas vai dar erro
        if flashcards.count() < int(qtd_perguntas):
            # Tratar para o usuário conseguir escolher posteriormente
            return redirect('/flashcard/iniciar_desafio')
        
        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                # Colunas da tabela cadastrada no banco de dados
                # Não é necessário adicionar as outras colunas, já que
                # estão definidos por padrão como "Falso"
                flashcard = f
            )

            flashcard_desafio.save()

            desafio.flashcards.add(flashcard_desafio)

        desafio.save()

        return redirect('/flashcard/listar_desafio.html')
    
def listar_desafio(request):
    desafios = Desafio.objects.filter(user = request.user)
    # TODO: Desenvolver os status
    # TODO: Desenvolver os filtros
    return render(request, 'listar_desafio.html', {'desafios': desafios})

def desafio(request, id):
    # Pega elementos do banco, no caso por id
    desafio = Desafio.objects.get(id = id)
    if not desafio.user == request.user:
        raise Http404
    print(desafio)
    if request.method == "GET":
        acertos = desafio.flashcards.filter(respondido = True).filter(acertou = True).count()
        erros = desafio.flashcards.filter(respondido = True).filter(acertou = False).count()
        faltantes = desafio.flashcards.filter(respondido = False).count()
        return render(request, 'desafio.html', {'desafio': desafio, 'acertos': acertos, 'erros': erros, 'faltantes': faltantes})

def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id = id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404
    
    flashcard_desafio.respondido = True

    # Forma primária
    # if acertou == '1':
    #     flashcard_desafio.acertou = True
    # elif acertou == '0':
    #     flashcard_desafio.acertou = False

    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()

    return redirect(f'/flashcard/desafio/{desafio_id}')

def relatorio(request, id):
    desafio = Desafio.objects.get(id = id)
    acertos = desafio.flashcards.filter(acertou = True).count()
    erros = desafio.flashcards.filter(acertou = False).count()

    dados = [acertos, erros]

    categorias = desafio.categoria.all()
    name_categoria = [i.nome for i in categorias]

    dados_categorias = []
    for categoria in categorias:
        # Filtrar por campo na tabela. Apenas as que acertei
        dados_categorias.append(desafio.flashcards.filter(flashcard__categoria = categoria).filter(acertou = True).count())
    
    # Exibindo as categorias no 2° gráfico - Forma primária
    # name_categoria = []
    # for i in categorias:
    #     name_categoria.append(i.nome)
        
    #TODO: Fazer o ranking

    return render(request, 'relatorio.html', {'desafio': desafio, 'dados': dados, 'categoria': name_categoria, 'dados_categorias': dados_categorias})