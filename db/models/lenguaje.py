from pydantic import BaseModel
from typing import Optional

class Lenguaje(BaseModel):
    id: Optional[str] = None
    nombre: str
    creado_por: str
    anio_creacion: int
    descripcion: str
    popularidad: str