import pytest
from unittest.mock import patch, MagicMock
import hashlib
import jwt
import datetime
from meiari_v1.services import EmailService, get_gemini_response, sample_gemini_response, users_encode_token, decode_token, generate_filename
from meiari_v1.models import OTPTable, User
from django.core.mail import send_mail
from django.conf import settings

# Test encrypt_password function
@pytest.mark.parametrize(
    "raw_password, expected_hash",
    [
        ("password123", "expected_hash_value_1"),  # Replace with actual expected hash
        ("anotherpassword", "expected_hash_value_2"),
    ]
)
def test_encrypt_password(raw_password, expected_hash):
    salt = hashlib.sha256()
    salt.update(raw_password.encode('utf-8'))
    salt_bytes = salt.digest()

    hashed_password = hashlib.sha256()
    hashed_password.update(raw_password.encode('utf-8') + salt_bytes)
    hashed_password_bytes = hashed_password.digest()

    assert hashed_password_bytes.hex() == expected_hash

# Test send_otp_email function
@pytest.fixture
def mock_user():
    return MagicMock(spec=User, cug_email_address="user@example.com")

@pytest.mark.django_db
@patch("meiari_v1.services.send_mail")
def test_send_otp_email(mock_send_mail, mock_user):
    email_service = EmailService()
    email_service.send_otp_email(mock_user)

    # Assert OTP email is sent
    otp_code = mock_send_mail.call_args[1]['message'].split()[-1]
    mock_send_mail.assert_called_once_with(
        "Your OTP Code",
        f"Your OTP code is {otp_code}. Please use this to verify your account.",
        settings.EMAIL_HOST_USER,  # Using the actual sender email from settings
        ["user@example.com"]
    )

# Test users_encode_token and decode_token
@pytest.mark.parametrize(
    "user_id, role",
    [("123", "admin"), ("456", "user")]
)
def test_users_encode_token(user_id, role):
    token = users_encode_token(user_id, role)
    payload = jwt.decode(token, "user_key", algorithms=["HS256"])
    
    assert payload["id"] == user_id
    assert payload["role"] == role

def test_decode_token():
    token = users_encode_token("123", "admin")
    decoded_value = decode_token(token)
    
    assert decoded_value["id"] == "123"
    assert decoded_value["role"] == "admin"

# Test generate_filename function
def test_generate_filename():
    base_name = "report"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = generate_filename(base_name)
    assert filename.startswith(base_name)
    assert filename.endswith(timestamp)

# Test get_gemini_response and sample_gemini_response functions
@patch("meiari_v1.services.genai.GenerativeModel")
def test_get_gemini_response(mock_model):
    mock_model.return_value.generate_content.return_value.text = "Sample report generated."
    
    prompt = "Sample prompt"
    response = get_gemini_response(prompt)
    
    assert response == "Sample report generated."

@patch("meiari_v1.services.get_gemini_response")
def test_sample_gemini_response(mock_get_gemini_response):
    mock_get_gemini_response.return_value = "Generated report content."

    sender = "Sender"
    receiver = "Receiver"
    content_body_1 = "Content part 1"
    content_body_2 = "Content part 2"
    
    response = sample_gemini_response(sender, receiver, content_body_1, content_body_2)
    
    assert response == "Generated report content."
