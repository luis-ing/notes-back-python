from fastapi import FastAPI, Depends
from app.routes import user_routes, note_router, login_routes
from app.core.security import validate_token

# Creamos la instancia de la aplicación
app = FastAPI()

# las rutas de login NO requieren token: ya están libres de dependencias.
# los routers de usuarios y notas ya traen la dependencia `validate_token`
# definida dentro de su archivo (ver app/core/security.py).
# también podríamos aplicar la verificación aquí al incluir los routers:
#
#   from app.core.security import validate_token
#   app.include_router(user_routes.router, dependencies=[Depends(validate_token)])
#   app.include_router(note_router.router, dependencies=[Depends(validate_token)])
#
# ambas alternativas son equivalentes; usamos la primera para que el
# comportamiento viaje con el router si se reutiliza en otro lugar.

app.include_router(login_routes.router)
app.include_router(user_routes.router, dependencies=[Depends(validate_token)])
app.include_router(note_router.router, dependencies=[Depends(validate_token)])

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}