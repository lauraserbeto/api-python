from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, Usuario, Perfil

app = FastAPI()

class PerfilModel(BaseModel):
    id: int
    perfil_nome: str

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil_nome: str

class UsuarioModel(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: Optional[PerfilModel] = None

    class Config:
        from_attributes = True

@app.post("/api/usuarios", status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este email já está registado.")

    novo_perfil = Perfil(perfil_nome=dados.perfil_nome)
    db.add(novo_perfil)
    db.commit()
    db.refresh(novo_perfil)

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
        id_perfil=novo_perfil.id
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "mensagem": "Utilizador e perfil registados com sucesso!",
        "user": novo_usuario
    }

@app.get("/api/usuarios", response_model=List[UsuarioModel])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@app.put("/api/usuarios/{id_usuario}", response_model=UsuarioModel)
def atualizar_usuario(id_usuario: int, dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado.")

    usuario.nome = dados.nome
    usuario.email = dados.email
    usuario.senha = dados.senha
    
    if usuario.perfil:
        usuario.perfil.perfil_nome = dados.perfil_nome

    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete("/api/usuarios/{id_usuario}")
def deletar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado.")

    perfil = db.query(Perfil).filter(Perfil.id == usuario.id_perfil).first()
    
    db.delete(usuario)
    if perfil:
        db.delete(perfil)
        
    db.commit()
    return {"mensagem": "Utilizador e perfil removidos com sucesso!"}