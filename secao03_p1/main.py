from fastapi import FastAPI, HTTPException, status, Response, Path, Query
from fastapi import Header, Depends
from models import Curso
from time import sleep
from typing import Any


def fake_db():
    try:
        print('abrindo conexao com o banco de dados...')
        sleep(1)
    finally:
        print('fechando conexao com o banco de dados...')


app = FastAPI(
    title="faustinok Api",
    version='1.0.0',
    description="uma api para estudo do fast api",

    )

cursos = {
    1: {
        "titulo": "python basic",
        "aulas": 712,
        "horas": 144
    },
    2: {
        "titulo": "html e css",
        "aulas": 40,
        "horas": 70

    }
}


@app.get('/cursos', description='Retorna todos os cursos',
         summary='esse e um resumo',
         # response_model=list[Curso],
         response_description='Cursos encontrados com sucesso'
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


# query parameters e pra limitar coisas e deixar como
# defauls coisas que estao no path

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID do curso',
                                         description='deve ser entre 1 e 2',
                                         gt=0, lt=3)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Curso nao encontrado.')


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    if curso.id not in cursos:
        if curso.id is None:
            
            id_curso = len(cursos) + 1
            curso.id = id_curso
        cursos[curso.id] = curso  # type: ignore

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Curso ja existe')
    return cursos


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso  # type: ignore
        return cursos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ID do Curso nao existe: id {curso_id}')


@app.delete('/cursos/{curso_id}')
async def del_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Id do Curso nao existe: id {curso_id}')

# query parameters e pra limitar coisas
# e deixar como defauls em coisas que nao estao
# no path como ?a=1&b=2


@app.get('/calculadora')
async def calcular(a: int = Query(default=0, gt=1),
                   b: int = Query(default=1, lt=5), c: int = 3,
                   x_geek: str = Header(default=None)):
    resultado = a + b + c
    print("#"*80)
    # na requisicao ele entende _ como -    pq? nao sei
    print(x_geek)
    return {"resultado": resultado}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1",
                port=8000, reload=True)
