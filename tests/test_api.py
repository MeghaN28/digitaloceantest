from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_event_ingestion_and_usage():
    payload = {
        'app_id': 'app-123',
        'plan_id': 'starter',
        'no_of_req': 150,
        'quota': 'basic',
        'resource_type': 'requests',
        'client_event_id': 'evt-001',
        'version': 1,
    }

    create = client.post('/api/v1/events', json=payload)
    assert create.status_code == 201
    body = create.json()
    assert 'event_id' in body

    usage = client.get('/api/v1/usage', params={'app_id': 'app-123'})
    assert usage.status_code == 200
    data = usage.json()
    assert data['app_id'] == 'app-123'
    assert data['usage_month_total'] == 150
    assert data['quota_plan'] == 'basic'
    assert data['quota_rps'] == 5000


def test_duplicate_client_event_is_idempotent():
    payload = {
        'app_id': 'app-456',
        'plan_id': 'pro',
        'no_of_req': 75,
        'quota': 'pro',
        'resource_type': 'requests',
        'client_event_id': 'evt-dup',
        'version': 1,
    }

    first = client.post('/api/v1/events', json=payload)
    second = client.post('/api/v1/events', json=payload)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()['event_id'] == second.json()['event_id']


def test_quota_plan_endpoint():
    response = client.get('/api/v1/quota-plan')
    assert response.status_code == 200
    assert response.json()['basic']['rps'] == 5000
    assert response.json()['pro']['rps'] == 12000
