from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import get_db
from models import Plataforma

router = APIRouter(prefix="/plataformas", tags=["Plataformas"])


class PlataformaCreate(BaseModel):
    nome: str


class PlataformaResponse(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[PlataformaResponse])
def listar_plataformas(db: Session = Depends(get_db)):
    return db.query(Plataforma).all()


@router.post("/", response_model=PlataformaResponse, status_code=201)
def cadastrar_plataforma(dados: PlataformaCreate, db: Session = Depends(get_db)):
    existente = db.query(Plataforma).filter(Plataforma.nome == dados.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Essa plataforma já está cadastrada.")

    plataforma = Plataforma(nome=dados.nome)
    db.add(plataforma)
    db.commit()
    db.refresh(plataforma)
    return plataforma
