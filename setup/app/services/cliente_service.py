from ..models import Cliente


def Cadastrar_cliente(cliente):
    Cliente.objects.create(nome=cliente.nome,email=cliente.email,endereco=cliente.endereco,
                           cpf=cliente.cpf,data_nascimento=cliente.data_nascimento,profissao=cliente.profissao)


def Listar_clientes():
    return Cliente.objects.all()


def Listar_clientes_id(id):
    return Cliente.objects.get(id=id)

def Editar_cliente(cliente,cliente_novo):
    cliente.nome = cliente_novo.nome
    cliente.cpf = cliente_novo.cpf
    cliente.email = cliente_novo.email
    cliente.data_nascimento = cliente_novo.data_nascimento
    cliente.profissao = cliente_novo.profissao
    cliente.endereco = cliente_novo.endereco
    cliente.save(force_update=True)


def Remover_cliente(cliente):
    cliente.delete()