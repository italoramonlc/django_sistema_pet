from ..models import EnderecoCliente


def Cadastrar_endereco(endereco):
    return EnderecoCliente.objects.create(rua=endereco.rua,cidade=endereco.cidade,estado=endereco.estado)


def Listar_endereco_id(id):
    return EnderecoCliente.objects.get(id=id)

def Editar_endereco(endereco_antigo,endereco_novo):
    endereco_antigo.rua = endereco_novo.rua
    endereco_antigo.cidade = endereco_novo.cidade
    endereco_antigo.estado = endereco_novo.estado
    endereco_antigo.save(force_update=True)
    return endereco_antigo

def Remover_endereco(endereco):
    endereco.delete()