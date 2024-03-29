import tempfile

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from weasyprint import HTML

from ..forms.clientes_forms import ClienteForm
from ..forms.endereco_forms import EnderecoClienteForm
from ..entidades import cliente, endereco
from ..services import cliente_service, endereco_service, pet_service, consulta_service

# site do pacote https://www.npmjs.com/package/loadtest
# instala o pagode npm install -g loadtest
# loadtest -n 100 -k http://127.0.0.1:8000/app/listar_clientes
@login_required()
@cache_page(60)
def listar_clientes(request):
    clientes = cliente_service.Listar_clientes()
    return render(request, "clientes/lista_clientes.html", {"clientes": clientes})


@login_required()
def listar_cliente_id(request, id):
    cliente = cliente_service.Listar_clientes_id(id)
    pets = pet_service.listar_pets(id)
    consultas = consulta_service.listar_consultas_pets(id)
    return render(request, "clientes/lista_cliente.html", {"cliente": cliente, "pets": pets, "consultas": consultas})


@login_required()
def cadastrar_cliente(request):
    if request.method == "POST":
        form_cliente = ClienteForm(request.POST)
        form_endereco = EnderecoClienteForm(request.POST)
        if form_cliente.is_valid():
            nome = form_cliente.cleaned_data["nome"]
            email = form_cliente.cleaned_data["email"]
            cpf = form_cliente.cleaned_data["cpf"]
            data_nascimento = form_cliente.cleaned_data["data_nascimento"]
            profissao = form_cliente.cleaned_data["profissao"]
            if form_endereco.is_valid():
                rua = form_endereco.cleaned_data["rua"]
                cidade = form_endereco.cleaned_data["cidade"]
                estado = form_endereco.cleaned_data["estado"]
                endereco_novo = endereco.Endereco(rua=rua, cidade=cidade, estado=estado)
                endereco_db = endereco_service.Cadastrar_endereco(endereco_novo)
                cliente_novo = cliente.Cliente(nome=nome, email=email, data_nascimento=data_nascimento,
                                               profissao=profissao, cpf=cpf, endereco=endereco_db)
                cliente_service.Cadastrar_cliente(cliente_novo)
                return redirect("listar_clientes")
    else:
        form_cliente = ClienteForm()
        form_endereco = EnderecoClienteForm()
        return render(request, 'clientes/form_cliente.html',
                      {"form_cliente": form_cliente, "form_endereco": form_endereco})


@login_required()
def editar_cliente(request, id):
    cliente_editar = cliente_service.Listar_clientes_id(id)
    cliente_editar.data_nascimento = cliente_editar.data_nascimento.strftime(
        '%Y-%m-%d')  # conversão da data para sair no html
    form_cliente = ClienteForm(request.POST or None, instance=cliente_editar)
    endereco_editar = endereco_service.Listar_endereco_id(cliente_editar.endereco.id)
    form_endereco = EnderecoClienteForm(request.POST or None, instance=endereco_editar)
    if form_cliente.is_valid():
        nome = form_cliente.cleaned_data["nome"]
        email = form_cliente.cleaned_data["email"]
        cpf = form_cliente.cleaned_data["cpf"]
        data_nascimento = form_cliente.cleaned_data["data_nascimento"]
        profissao = form_cliente.cleaned_data["profissao"]
        if form_endereco.is_valid():
            rua = form_endereco.cleaned_data["rua"]
            cidade = form_endereco.cleaned_data["cidade"]
            estado = form_endereco.cleaned_data["estado"]
            endereco_novo = endereco.Endereco(rua=rua, cidade=cidade, estado=estado)
            endereco_editado = endereco_service.Editar_endereco(endereco_editar, endereco_novo)
            cliente_novo = cliente.Cliente(nome=nome, email=email, data_nascimento=data_nascimento, profissao=profissao,
                                           cpf=cpf, endereco=endereco_editado)
            cliente_service.Editar_cliente(cliente_editar, cliente_novo)
            return redirect("listar_clientes")
    return render(request, "clientes/form_cliente.html", {"form_cliente": form_cliente, "form_endereco": form_endereco})


@login_required()
def remover_cliente(request, id):
    cliente = cliente_service.Listar_clientes_id(id)
    endereco = endereco_service.Listar_endereco_id(cliente.endereco.id)
    if request.method == "POST":
        cliente_service.Remover_cliente(cliente)
        endereco_service.Remover_endereco(endereco)
        return redirect("listar_clientes")
    return render(request, "clientes/confirma_exclusao.html", {"cliente": cliente})


def gerar_pdf_clientes(request):
    clientes = cliente_service.Listar_clientes()
    html_string = render_to_string("clientes/pdf.html", {"clientes": clientes})
    html = HTML(string=html_string)
    resultado_pdf = html.write_pdf()

    resposta = HttpResponse(content_type="application/pdf;")
    resposta["Content-Disposition"] = "inline; filename=lista_clientes.pdf"
    resposta["Content-Transfer-Enconding"] = "binary"
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultado_pdf)
        output.flush()
        output.seek(0)
        #output = open(output.name, 'rb')
        resposta.write(output.read())

    return resposta
