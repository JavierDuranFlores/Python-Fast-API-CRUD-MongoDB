
def lenguaje_schema(lenguaje) -> dict:
    return {"id": str(lenguaje["_id"]),
            "nombre": lenguaje["nombre"],
            "creado_por": lenguaje["creado_por"],
            "anio_creacion": lenguaje["anio_creacion"],
            "descripcion": lenguaje["descripcion"],
            "popularidad": lenguaje["popularidad"]}
    
def lenguajes_schema(lenguajes) -> list:
    return [lenguaje_schema(lenguaje) for lenguaje in lenguajes]