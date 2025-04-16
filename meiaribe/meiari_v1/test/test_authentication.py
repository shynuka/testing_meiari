import pytest
from rest_framework.test import APIClient
from rest_framework.exceptions import AuthenticationFailed
from meiari_v1.models import UserDetails
from unittest.mock import patch
import jwt


@pytest.fixture
def create_user():
    # Creating a test user in the database
    user = UserDetails.objects.create(id="1", username="test_user", password="password123", role="admin")
    return user


@pytest.fixture
def valid_token(create_user):
    # Creating a valid JWT token for the created user
    payload = {"id": create_user.id, "role": create_user.role}
    token = jwt.encode(payload, "user_key", algorithm="HS256")
    return token


@pytest.fixture
def invalid_token():
    # Creating an invalid JWT token
    token = "invalid.token.string"
    return token


@pytest.fixture
def client():
    # Creating an API client to simulate requests
    return APIClient()


@pytest.mark.django_db
def test_valid_token_authentication(client, create_user, valid_token):
    # Sending a request with a valid token in the Authorization header
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {valid_token}")
    response = client.get("/some-protected-endpoint/")
    assert response.status_code == 200  # Assuming status code 200 indicates success


@pytest.mark.django_db
def test_invalid_token_authentication(client, invalid_token):
    # Sending a request with an invalid token in the Authorization header
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {invalid_token}")
    response = client.get("/some-protected-endpoint/")
    assert response.status_code == 401  # Unauthorized error


@pytest.mark.django_db
def test_missing_token(client):
    # Sending a request with no Authorization header
    response = client.get("/some-protected-endpoint/")
    assert response.status_code == 401  # Unauthorized error


@pytest.mark.django_db
def test_expired_token(client, create_user):
    # Sending a request with an expired token (manually setting an expired token)
    expired_payload = {"id": create_user.id, "role": create_user.role, "exp": 0}
    expired_token = jwt.encode(expired_payload, "user_key", algorithm="HS256")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_token}")
    response = client.get("/some-protected-endpoint/")
    assert response.status_code == 401  # Unauthorized error due to expired token


@pytest.mark.django_db
def test_authentication_failed(client, create_user):
    # Simulate AuthenticationFailed exception raised by the custom authentication class
    with patch("meiaribe.meiari_v1.authentication.UserTokenAuthentication.authenticate") as mock_authenticate:
        mock_authenticate.side_effect = AuthenticationFailed("Token authentication failed.")
        client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = client.get("/some-protected-endpoint/")
        assert response.status_code == 401  # Unauthorized error due to failed authentication


@pytest.mark.django_db
def test_user_not_found(client, create_user):
    # Sending a request with a valid token but a non-existing user
    payload = {"id": "non_existing_id", "role": create_user.role}
    token = jwt.encode(payload, "user_key", algorithm="HS256")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get("/some-protected-endpoint/")
    assert response.status_code == 401  # Unauthorized error for non-existing user
