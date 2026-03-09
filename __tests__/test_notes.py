# ── Crear nota ────────────────────────────────

def test_create_note_success(auth_client):
    client, headers, user_id = auth_client
    response = client.post("/notes/create", headers=headers, json={  # 👈 headers
        "title": "Mi primera nota",
        "content": "Contenido de prueba",
        "userCreated": user_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Nota creada exitosamente"
    assert data["note"]["title"] == "Mi primera nota"


def test_create_note_missing_fields(auth_client):
    client, headers, user_id = auth_client
    response = client.post("/notes/create", headers=headers, json={  # 👈 headers
        "title": "Solo título"
    })
    assert response.status_code == 422


# ── Listar notas ──────────────────────────────

def test_list_notes_empty(auth_client):
    client, headers, user_id = auth_client
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_notes_with_data(auth_client):
    client, headers, user_id = auth_client
    client.post("/notes/create", headers=headers, json={
        "title": "Nota listado",
        "content": "Contenido",
        "userCreated": user_id
    })
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_notes_requires_token(client):
    """Sin token debe retornar 401."""
    response = client.get("/notes/")
    assert response.status_code == 401  # 👈 corregido: HTTPBearer retorna 401


def test_list_notes_invalid_token(client):
    """Token inválido debe retornar 401."""
    response = client.get("/notes/", headers={"Authorization": "Bearer token_invalido"})
    assert response.status_code == 401


# ── Obtener nota por ID ───────────────────────

def test_get_note_by_id_success(auth_client):
    client, headers, user_id = auth_client
    created = client.post("/notes/create", headers=headers, json={
        "title": "Nota por ID",
        "content": "Detalle",
        "userCreated": user_id
    })
    note_id = created.json()["note"]["id"]

    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == note_id


def test_get_note_by_id_not_found(auth_client):
    client, headers, user_id = auth_client
    response = client.get("/notes/99999", headers=headers)
    assert response.status_code == 404


def test_get_note_requires_token(client):
    """Sin token debe retornar 401."""
    response = client.get("/notes/1")
    assert response.status_code == 401  # 👈 corregido


# ── Actualizar nota ───────────────────────────

def test_update_note_success(auth_client):
    client, headers, user_id = auth_client
    created = client.post("/notes/create", headers=headers, json={
        "title": "Antes",
        "content": "Contenido viejo",
        "userCreated": user_id
    })
    note_id = created.json()["note"]["id"]

    response = client.put(f"/notes/update/{note_id}", headers=headers, json={
        "title": "Después",
        "content": "Contenido nuevo",
        "userCreated": user_id
    })
    assert response.status_code == 200
    assert response.json()["note"]["title"] == "Después"


def test_update_note_not_found(auth_client):
    client, headers, user_id = auth_client
    response = client.put("/notes/update/99999", headers=headers, json={
        "title": "X",
        "content": "X",
        "userCreated": user_id
    })
    assert response.status_code == 404