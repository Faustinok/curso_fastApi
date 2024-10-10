from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel as UsrModel

from core.configs import settings
from core.security import verify_pwd

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V_STR}/usuarios/login')

async def autenticar(email: EmailStr,pwd: str,db: AsyncSession)-> Optional[UsrModel]:
    async with db as session:        
        query = select(UsrModel).filter(UsrModel.email == email)
        result = await session.execute(query)
        usuario: UsrModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        if not verify_pwd(pwd,usuario.senha):
            return None
        return usuario 
    
def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz = sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.ALGORITHM)


def criar_token_acesso(sub:str) -> str:
    return _criar_token(
        tipo_token='acess_token',
        tempo_vida= timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub = sub
    )