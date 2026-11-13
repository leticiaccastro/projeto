from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Avaliacao, Jogo

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


class AvaliacaoCreate(BaseModel):
    nota: int = Field(ge=1, le=5)
    comentario: str
    jogo_id: int


class AvaliacaoResponse(BaseModel):
    id: int
    nota: int
    comentario: str
    jogo_id: int
    model_config = ConfigDict(from_attributes=True)


@router.get("/jogo/{jogo_id}", response_model=list[AvaliacaoResponse])
def listar_avaliacoes_por_jogo(jogo_id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return db.query(Avaliacao).filter(Avaliacao.jogo_id == jogo_id).all()


@router.post("/", response_model=AvaliacaoResponse, status_code=201)
def registrar_avaliacao(dados: AvaliacaoCreate, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == dados.jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    avaliacao = Avaliacao(**dados.model_dump())
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao


@router.delete("/{id}", status_code=204)
def remover_avaliacao(id: int, db: Session = Depends(get_db)):
    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == id).first()
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    db.delete(avaliacao)
    db.commit()
    return Response(status_code=204)
