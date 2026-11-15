def signup_and_login(client, email="asha@example.com"):
    client.post("/auth/register", data={"name": "Asha Devi", "email": email, "password": "secret123"})
    client.post("/auth/login", data={"email": email, "password": "secret123"})
