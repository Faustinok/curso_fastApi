from core.database import Session
from core.auth import settings,oauth2_schema
from typing import Generator, Optional
from fastapi import Depends,HTTPException,status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from models.usuario_model import UsuarioModel



class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()

async def get_current_user(db: Session = Depends(get_session), # type: ignore
                           token: str = Depends(oauth2_schema)
                           )-> UsuarioModel:
    
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                         detail='Nao foi possivel autenticar a credencial',
                                         headers={"www-Authenticate":"Bearer"}
                                         )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options= {"verify_aud":False}
        )

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))

        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        if usuario is None:
            raise credential_exception
        
        return usuario
