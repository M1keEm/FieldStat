import pytest
from backendFlask.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Crop Yield API" in response.data

def test_crop_yield(client):
    response = client.get('/crop_yield?commodity=CORN&year=2022')
    assert response.status_code == 200
    assert "data" in response.get_json()

def test_weather(client):
    response = client.get('/weather?state=Iowa&year=2022')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "state" in json_data
    assert "avg_temp_C" in json_data
    assert "total_precip_mm" in json_data

def test_plot(client):
    response = client.get('/plot?commodity=CORN&year=2022')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert "path" in json_data