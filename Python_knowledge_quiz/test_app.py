import pytest
from app import app, db, User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client


def test_home_redirects_to_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_user(client):
    response = client.post("/register", data={
        "email": "test@example.com",
        "password": "test123"
    }, follow_redirects=True)
    assert b"Login" in response.data
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None


def test_login_user(client):
    client.post("/register", data={
        "email": "login@test.com",
        "password": "secret"
    })
    response = client.post("/login", data={
        "email": "login@test.com",
        "password": "secret"
    }, follow_redirects=True)
    assert b"Qualification" in response.data or b"Start" in response.data


def test_duplicate_register(client):
    client.post("/register", data={"email": "dup@test.com", "password": "123"})
    response = client.post(
        "/register", data={"email": "dup@test.com", "password": "456"})
    assert b"Email already exists." in response.data or b"Login" in response.data
