

def test_login_success(client):
    # primero creamos usuario
    client.post("/login/create", json={
        "name": "Luis",
        "mail": "luis2@test.com",
        "pass_": "123456"
    })

    response = client.post("/login", json={
        "mail": "luis2@test.com",
        "pass_": "123456"
    })

    assert response.status_code == 200
    assert "token" in response.json()