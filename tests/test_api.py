import httpx
# from pytest import fixture, mark

API_URL = 'http://127.0.0.1:5000'

def test_verificacao_healthy():
    response = httpx.get(
        f'{API_URL}/'
    )
        
    assert response.status_code == 200
