from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Jogo, Plataforma

router = APIRouter(prefix="/jogos", tags=["Jogos"])


class JogoCreate(BaseModel):
    titulo: str
    genero: str
    preco: float = Field(ge=0)
    plataforma_id: int


class JogoResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    preco: float
    plataforma_id: int
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[JogoResponse])
def listar_jogos(db: Session = Depends(get_db)):
    return db.query(Jogo).all()


@router.get("/{id}", response_model=JogoResponse)
def buscar_jogo(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo


@router.post("/", response_model=JogoResponse, status_code=201)
def cadastrar_jogo(dados: JogoCreate, db: Session = Depends(get_db)):
    plataforma = db.query(Plataforma).filter(
        Plataforma.id == dados.plataforma_id
    ).first()
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")

    jogo = Jogo(**dados.model_dump())
    db.add(jogo)
    db.commit()
    db.refresh(jogo)
    return jogo


@router.put("/{id}", response_model=JogoResponse)
def atualizar_jogo(id: int, dados: JogoCreate, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    plataforma = db.query(Plataforma).filter(
        Plataforma.id == dados.plataforma_id
    ).first()
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")

    for campo, valor in dados.model_dump().items():
        setattr(jogo, campo, valor)

    db.commit()
    db.refresh(jogo)
    return jogo


@router.delete("/{id}", status_code=204)
def remover_jogo(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    db.delete(jogo)
    db.commit()
    return Response(status_code=204)
