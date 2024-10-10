from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def verify_pwd(senha: str, hash_pwd: str) -> bool:
    """
    FUNCAO PARA VERIFICAR SE A SENHA ESTA 
    CORRETA COMPARANDO A SENHA EM TEXTO 
    COM O HASH QUE TA NO BD

    """

    return CRIPTO.verify(senha,hash_pwd)
def gerar_hash_senha(senha: str) -> str:
    """
    essa funcao cria um hash de acordo com o texto
    """
    return CRIPTO.hash(senha)