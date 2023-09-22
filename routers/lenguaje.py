from fastapi import APIRouter, status, HTTPException
from db.models.lenguaje import Lenguaje
from db.client import db_cliente
from db.schemas.lenguaje import lenguaje_schema, lenguajes_schema
from typing import List
from bson import ObjectId

lenguaje = APIRouter(prefix="/lenguaje", 
                     tags=["lenguaje"], 
                     responses={status.HTTP_404_NOT_FOUND: {"description": "No encontrado"}})

@lenguaje.get("/", response_model=List[Lenguaje], status_code=status.HTTP_200_OK)
async def leer_lenguajes():
    return lenguajes_schema(db_cliente.lenguaje.lenguajes.find())
  
@lenguaje.get("/{id}")
async def leer_lenguaje_por_id(id: str):
    return buscar_lenguaje("_id", ObjectId(id)) 

@lenguaje.post("/", response_model=Lenguaje, status_code=status.HTTP_201_CREATED)
async def create_lenguaje(lenguaje: Lenguaje):
    
    if type(buscar_lenguaje("nombre", lenguaje.nombre)) == Lenguaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El lenguaje ya existe")
    
    lenguaje_dict = dict(lenguaje)
    del lenguaje_dict["id"]
    
    id = db_cliente.lenguaje.lenguajes.insert_one(lenguaje_dict).inserted_id
    
    new_lenguaje = lenguaje_schema(db_cliente.lenguaje.lenguajes.find_one({"_id":id}))
    
    return Lenguaje(**new_lenguaje)



@lenguaje.put("/",response_model=Lenguaje)
async def actualizar_lenguaje(lenguaje: Lenguaje):
    lenguaje_dict = dict(lenguaje)
    del lenguaje_dict["id"]
    try:
        db_cliente.lenguaje.lenguajes.find_one_and_replace({"_id": ObjectId(lenguaje.id)}, lenguaje_dict)
    except:
        return {"error": "No se puedo actualizar el lenguaje"}

    return buscar_lenguaje("_id", ObjectId(lenguaje.id))



@lenguaje.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_lenguaje(id: str):
    encontrado = db_cliente.lenguaje.lenguajes.find_one_and_delete({"_id": ObjectId(id)})
    
    if not encontrado:
        return {"error": "No se ha eliminado el lenguaje"}



def buscar_lenguaje(field: str, key):
    try:
        lenguaje = db_cliente.lenguaje.lenguajes.find_one({field:key})
        return Lenguaje(**lenguaje_schema(lenguaje))
    except:
        return {"error": "No se ha encontrado el lenguaje"}